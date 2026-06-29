# -*- coding: utf-8 -*-
"""
Blinx Guest Generator - API Handler
Flask-based web API that wraps the core generation logic from app.py
"""

from flask import Flask, request, jsonify, session, send_from_directory
import asyncio
import aiohttp
import threading
import json
import os
import time
import sys
import hmac
import hashlib
import base64
import random
import string
from datetime import datetime, timedelta
from functools import wraps
import warnings
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─── Flask App ─────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder='../static', static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY', 'Blinx-Slvffy')

app.config.update(
    SESSION_COOKIE_SECURE=True if os.environ.get('VERCEL') == '1' else False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

@app.before_request
def make_session_permanent():
    session.permanent = True


# ─── Admin Password ────────────────────────────────────────────────────────
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'BLINXANDSLVFFY')

# ─── Generation State ──────────────────────────────────────────────────────
generation_sessions = {}  # session_id -> {status, accounts, ...}
generation_lock = threading.Lock()

# ─── Constants from app.py ────────────────────────────────────────────────
HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
API_KEY = bytes.fromhex(HEX_KEY)
REGISTER_URL = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
TOKEN_URL = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
MAJOR_REGISTER_URL = "https://loginbp.ggpolarbear.com/MajorRegister"
MAJOR_LOGIN_URL = "https://loginbp.ggpolarbear.com/MajorLogin"

ALL_REGIONS = ["ID", "IND", "TH", "VN", "ME", "BD", "PK", "TW", "EU", "CIS", "NA", "SAC", "BR"]
REGION_NAMES = {
    "IND": "India", "ID": "Indonesia", "TH": "Thailand", "VN": "Vietnam",
    "ME": "Middle East", "BD": "Bangladesh", "PK": "Pakistan", "TW": "Taiwan",
    "EU": "Europe", "CIS": "Russia/CIS", "NA": "North America", "SAC": "South America",
    "BR": "Brazil"
}
REGION_FLAGS = {
    "IND": "🇮🇳", "ID": "🇮🇩", "TH": "🇹🇭", "VN": "🇻🇳",
    "ME": "🌍", "BD": "🇧🇩", "PK": "🇵🇰", "TW": "🇹🇼",
    "EU": "🇪🇺", "CIS": "🇷🇺", "NA": "🇺🇸", "SAC": "🇧🇷", "BR": "🇧🇷"
}
REGION_LANG = {
    "ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th",
    "BD": "bn", "PK": "ur", "TW": "zh", "EU": "en", "CIS": "ru",
    "NA": "en", "SAC": "es", "BR": "pt"
}

# ─── Proxy Rotator ─────────────────────────────────────────────────────────
class IPRotator:
    PROXIES = []
    _proxy_index = 0
    _proxy_lock = threading.Lock()

    @classmethod
    def load_proxies(cls):
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        proxy_paths = [
            os.path.join(parent_dir, "proxy.txt"),
            os.path.join(parent_dir, "proxies.txt"),
            "proxy.txt",
            "proxies.txt"
        ]
        for path in proxy_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                    if lines:
                        cls.PROXIES = lines
                        break
                except:
                    pass

    @classmethod
    def get_rotating_proxy(cls):
        if not cls.PROXIES:
            return None
        with cls._proxy_lock:
            proxy = cls.PROXIES[cls._proxy_index % len(cls.PROXIES)]
            cls._proxy_index += 1
            if not proxy.startswith("http://") and not proxy.startswith("https://") and not proxy.startswith("socks"):
                proxy = f"http://{proxy}"
            return proxy

IPRotator.load_proxies()

# ─── Crypto helpers ────────────────────────────────────────────────────────
AES_AVAILABLE = False
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    AES_AVAILABLE = True
except ImportError:
    pass

def decode_proto(data):
    res = {}
    i = 0
    l = len(data)
    while i < l:
        val = 0
        shift = 0
        while True:
            if i >= l: break
            b = data[i]
            i += 1
            val |= (b & 0x7F) << shift
            if not (b & 0x80): break
            shift += 7
        if i >= l and val == 0: break
        tag = val >> 3
        wire_type = val & 0x07
        if wire_type == 0:
            varint_val = 0
            shift = 0
            while True:
                if i >= l: break
                b = data[i]
                i += 1
                varint_val |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
            res[tag] = varint_val
        elif wire_type == 2:
            length = 0
            shift = 0
            while True:
                if i >= l: break
                b = data[i]
                i += 1
                length |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
            if i + length > l: break
            val_bytes = data[i:i+length]
            i += length
            res[tag] = val_bytes
        elif wire_type == 1:
            if i + 8 > l: break
            res[tag] = data[i:i+8]
            i += 8
        elif wire_type == 5:
            if i + 4 > l: break
            res[tag] = data[i:i+4]
            i += 4
        else:
            break
    return res

PROTO_AVAILABLE = True


def decode_jwt_token(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += '=' * padding
            decoded = base64.urlsafe_b64decode(payload_part)
            data = json.loads(decoded)
            account_id = data.get('account_id') or data.get('external_id')
            if account_id:
                return str(account_id)
    except:
        pass
    return "N/A"

def generate_password():
    return "Blinx_" + ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

def get_spoof_ip(region):
    region_ips = {
        "ID": ["36.69.", "103.10.", "114.120.", "180.252."],
        "IND": ["1.6.", "14.96.", "27.56.", "103.21."],
        "TH": ["49.228.", "101.109.", "171.96.", "203.156."],
        "VN": ["14.232.", "27.72.", "103.7.", "116.96."],
        "ME": ["37.10.", "77.83.", "94.56.", "185.20."],
        "BD": ["103.108.", "114.130.", "119.30.", "123.49."],
        "PK": ["39.32.", "58.27.", "103.255.", "119.152."],
        "EU": ["185.10.", "91.108.", "46.227.", "31.13."],
        "NA": ["8.8.", "104.16.", "172.217.", "198.41."],
        "BR": ["177.75.", "189.1.", "200.98.", "201.20."],
    }
    prefixes = region_ips.get(region, ["10.0."])
    prefix = random.choice(prefixes)
    return prefix + str(random.randint(1,254)) + "." + str(random.randint(1,254))

def get_spoof_headers(base_headers, region):
    ip = get_spoof_ip(region)
    base_headers["X-Forwarded-For"] = ip
    base_headers["X-Real-IP"] = ip
    base_headers["CF-Connecting-IP"] = ip
    return base_headers

# ─── Async Protobuf helpers ────────────────────────────────────────────────
async def enc_varint(n):
    if n < 0: return b''
    H = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n: b |= 0x80
        H.append(b)
        if not n: break
    return bytes(H)

async def create_field_varint(fn, val):
    return await enc_varint((fn << 3) | 0) + await enc_varint(val)

async def create_field_len(fn, val):
    h = await enc_varint((fn << 3) | 2)
    e = val.encode() if isinstance(val, str) else val
    return h + await enc_varint(len(e)) + e

async def create_proto(fields):
    p = bytearray()
    for f, v in fields.items():
        if isinstance(v, dict):
            p.extend(await create_field_len(f, await create_proto(v)))
        elif isinstance(v, int):
            p.extend(await create_field_varint(f, v))
        elif isinstance(v, (str, bytes)):
            p.extend(await create_field_len(f, v))
    return p

def encrypt_aes(hex_str):
    if not AES_AVAILABLE:
        return bytes.fromhex(hex_str)
    raw = bytes.fromhex(hex_str)
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(raw, AES.block_size))

async def build_major_login_payload_proto(open_id, access_token):
    if not PROTO_AVAILABLE or not AES_AVAILABLE:
        return None
    try:
        fields = {
            3: str(datetime.now())[:-7],
            4: "free fire",
            5: 1,
            7: "1.126.2",
            8: "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)",
            9: "Handheld",
            10: "Verizon",
            11: "WIFI",
            12: 1920,
            13: 1080,
            14: "280",
            15: "ARM64 FP ASIMD AES VMH | 2865 | 4",
            16: 3003,
            17: "Adreno (TM) 640",
            18: "OpenGL ES 3.1 v1.46",
            19: "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57",
            20: "223.191.51.89",
            21: "en",
            22: open_id,
            23: "4",
            24: "Handheld",
            25: {
                6: 55,
                8: 81
            },
            29: access_token,
            30: 1,
            41: "Verizon",
            42: "WIFI",
            57: "7428b253defc164018c604a1ebbfebdf",
            60: 36235,
            61: 31335,
            62: 2519,
            63: 703,
            64: 25010,
            65: 26628,
            66: 32992,
            67: 36235,
            73: 3,
            74: "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64",
            76: 1,
            77: "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk",
            78: 3,
            79: 2,
            81: "64",
            83: "2019118695",
            86: "OpenGLES2",
            87: 16383,
            88: 4,
            89: b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg==",
            92: 13564,
            93: "android",
            94: "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY=",
            95: 110009,
            97: 1,
            98: 1,
            99: "4",
            100: "4"
        }
        serialized = await create_proto(fields)
        key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
        iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(serialized, AES.block_size))
    except:
        return None

def get_next_proxy():
    """Get next proxy from rotation pool without pre-validation.
    Pre-validation floods the target servers with test requests and causes
    rate limiting. Instead, use the proxy directly and let the actual request
    handle failures via retry logic."""
    return IPRotator.get_rotating_proxy()

# ─── Core async account creator ───────────────────────────────────────────
async def create_single_account(session_obj, region, name_prefix, account_index):
    proxy = get_next_proxy()
    password = generate_password()
    # Ensure nickname length does not exceed Garena's 12-character limit
    suffix = f"_{account_index}_{random.randint(100, 999)}"
    max_prefix_len = 12 - len(suffix)
    safe_prefix = name_prefix[:max_prefix_len] if max_prefix_len > 0 else "B"
    name = safe_prefix + suffix
    timestamp = str(int(time.time() * 1000))
    headers_base = {
        "User-Agent": "GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Host": "100067.connect.garena.com",
        "X-Garena-Timestamp": timestamp,
    }
    headers_base = get_spoof_headers(headers_base, region)

    try:
        # Step 1: Register
        payload_reg = json.dumps({
            "app_id": 100067, "client_type": 2,
            "password": password, "source": 2
        }, separators=(',', ':'))
        sig_reg = hmac.new(API_KEY, payload_reg.encode(), hashlib.sha256).hexdigest()
        headers_reg = {**headers_base, "Authorization": f"Signature {sig_reg}"}

        async with session_obj.post(
            REGISTER_URL, data=payload_reg, headers=headers_reg,
            ssl=False, timeout=aiohttp.ClientTimeout(total=15), proxy=proxy
        ) as resp:
            if resp.status != 200:
                print(f"[{account_index}] Step 1 HTTP Failure: status={resp.status}, proxy={proxy}", file=sys.stderr)
                return None
            reg_json = await resp.json()
            if reg_json.get("code") != 0:
                print(f"[{account_index}] Step 1 Code Failure: json={reg_json}, proxy={proxy}", file=sys.stderr)
                return None
            uid = reg_json['data']['uid']

        # Step 2: Token
        payload_tok = json.dumps({
            "client_id": 100067, "client_secret": HEX_KEY,
            "client_type": 2, "password": password,
            "response_type": "token", "uid": uid,
        }, separators=(',', ':'))
        sig_tok = hmac.new(API_KEY, payload_tok.encode(), hashlib.sha256).hexdigest()
        headers_tok = {**headers_base, "Authorization": f"Signature {sig_tok}"}

        async with session_obj.post(
            TOKEN_URL, data=payload_tok, headers=headers_tok,
            ssl=False, timeout=aiohttp.ClientTimeout(total=15), proxy=proxy
        ) as resp:
            if resp.status != 200:
                print(f"[{account_index}] Step 2 HTTP Failure: status={resp.status}, proxy={proxy}", file=sys.stderr)
                return None
            tok_json = await resp.json()
            if tok_json.get("code") != 0:
                print(f"[{account_index}] Step 2 Code Failure: json={tok_json}, proxy={proxy}", file=sys.stderr)
                return None
            access_token = tok_json['data']['access_token']
            open_id = tok_json['data']['open_id']

        # Step 3: Major Register
        lang_code = REGION_LANG.get(region.upper(), "en")
        keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,
                     0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,
                     0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
        encoded_open_id = ""
        for i, ch in enumerate(open_id):
            encoded_open_id += chr(ord(ch) ^ keystream[i % len(keystream)])
        field14 = encoded_open_id.encode('latin1')

        payload_fields = {
            1: name, 2: access_token, 3: open_id,
            5: 102000007, 6: 4, 7: 1, 13: 1,
            14: field14, 15: lang_code, 16: 1, 17: 1
        }
        proto_bytes = await create_proto(payload_fields)
        encrypted_payload = encrypt_aes(bytes(proto_bytes).hex())

        headers_mreg = {
            "Accept-Encoding": "gzip", "Authorization": "Bearer",
            "Connection": "close", "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue", "Host": "loginbp.ggpolarbear.com",
            "ReleaseVersion": "OB54",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1", "X-Unity-Version": "1.126.2",
        }
        headers_mreg = get_spoof_headers(headers_mreg, region)

        async with session_obj.post(
            MAJOR_REGISTER_URL, data=encrypted_payload, headers=headers_mreg,
            ssl=False, timeout=aiohttp.ClientTimeout(total=15), proxy=proxy
        ) as resp:
            if resp.status != 200:
                body = await resp.read()
                print(f"[{account_index}] Step 3 HTTP Failure: status={resp.status}, proxy={proxy}, body={body}", file=sys.stderr)
                return None

        # Step 4: Major Login
        final_payload = await build_major_login_payload_proto(open_id, access_token)
        if final_payload is None:
            print(f"[{account_index}] Step 4 Build Payload Failure (proto/AES unavailable), proxy={proxy}", file=sys.stderr)
            return None

        headers_ml = {
            "Accept-Encoding": "gzip", "Authorization": "Bearer",
            "Connection": "close", "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue", "Host": "loginbp.ggpolarbear.com",
            "ReleaseVersion": "OB54",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1",
        }
        headers_ml = get_spoof_headers(headers_ml, region)

        async with session_obj.post(
            MAJOR_LOGIN_URL, data=final_payload, headers=headers_ml,
            ssl=False, timeout=aiohttp.ClientTimeout(total=15), proxy=proxy
        ) as resp:
            if resp.status != 200:
                body = await resp.read()
                print(f"[{account_index}] Step 4 HTTP Failure: status={resp.status}, proxy={proxy}, body={body}", file=sys.stderr)
                return None
            content = await resp.read()
            account_id = "N/A"
            jwt_token = ""
            if PROTO_AVAILABLE:
                try:
                    parsed = decode_proto(content)
                    token = parsed.get(8, b'').decode('utf-8', errors='ignore')
                    if token:
                        account_uid = parsed.get(1)
                        account_id = str(account_uid) if account_uid else decode_jwt_token(token)
                        jwt_token = token
                except:
                    pass
            if account_id == "N/A":
                text = content.decode('utf-8', errors='ignore')
                jwt_start = text.find("eyJ")
                if jwt_start != -1:
                    jt = text[jwt_start:]
                    second_dot = jt.find(".", jt.find(".") + 1)
                    if second_dot != -1:
                        jwt_token = jt[:second_dot + 44]
                        account_id = decode_jwt_token(jwt_token)

            if account_id == "N/A":
                print(f"[{account_index}] Step 4 Account ID not found in response, proxy={proxy}", file=sys.stderr)
                return None

            return {
                "uid": str(uid),
                "password": password,
                "account_id": account_id,
                "name": name,
                "region": region,
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "is_rare": check_rarity(account_id)
            }

    except Exception as e:
        import traceback
        print(f"Error creating account {account_index}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None

def check_rarity(account_id):
    """Check if account ID has special patterns"""
    import re
    patterns = [
        r"(\d)\1{3,}",                 # 4+ repeated digits
        r"(12345|23456|34567|45678)",   # sequential 5
        r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)",  # quad
        r"(69|420|1337|007)",           # special combos
    ]
    for p in patterns:
        if re.search(p, str(account_id)):
            return True
    if str(account_id).isdigit() and int(account_id) < 1000000:
        return True
    return False

# ─── Generation runner (threaded) ─────────────────────────────────────────
def run_generation(session_id, count, region, name_prefix):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def _run():
        generation_sessions[session_id]['status'] = 'running'
        generation_sessions[session_id]['total'] = count
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as http_session:
            semaphore = asyncio.Semaphore(min(50, count))
            tasks_done = 0
            
            async def worker(idx):
                nonlocal tasks_done
                async with semaphore:
                    for attempt in range(5):
                        if attempt > 0:
                            # Small back-off on retries, rotating proxy handled inside create_single_account
                            await asyncio.sleep(random.uniform(0.5, 1.5))
                        result = await create_single_account(http_session, region, name_prefix, idx)
                        if result:
                            with generation_lock:
                                generation_sessions[session_id]['accounts'].append(result)
                                generation_sessions[session_id]['success'] += 1
                            break
                with generation_lock:
                    tasks_done += 1
                    generation_sessions[session_id]['done'] = tasks_done

            tasks = [worker(i + 1) for i in range(count)]
            await asyncio.gather(*tasks)
        
        generation_sessions[session_id]['status'] = 'done'
    
    try:
        loop.run_until_complete(_run())
    except Exception as e:
        generation_sessions[session_id]['status'] = 'error'
        generation_sessions[session_id]['error'] = str(e)
    finally:
        loop.close()

# ─── Auth decorator ───────────────────────────────────────────────────────
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# ─── Routes ───────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    password = data.get('password', '')
    if password == ADMIN_PASSWORD:
        session['authenticated'] = True
        return jsonify({'success': True, 'message': 'Login berhasil'})
    return jsonify({'success': False, 'message': 'Password salah'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/regions', methods=['GET'])
@require_auth
def get_regions():
    regions = []
    for code in ALL_REGIONS:
        regions.append({
            'code': code,
            'name': REGION_NAMES.get(code, code),
            'flag': REGION_FLAGS.get(code, '🌐'),
            'default': code == 'ID'
        })
    return jsonify({'regions': regions})

@app.route('/api/generate', methods=['POST'])
@require_auth
def start_generate():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    count = int(data.get('count', 1))
    region = data.get('region', 'ID').upper()
    name_prefix = data.get('name_prefix', 'Blinx').strip() or 'Blinx'

    if count < 1 or count > 500:
        return jsonify({'error': 'Jumlah akun harus antara 1-500'}), 400
    if region not in ALL_REGIONS:
        return jsonify({'error': 'Region tidak valid'}), 400

    session_id = f"gen_{int(time.time()*1000)}_{random.randint(1000,9999)}"
    with generation_lock:
        generation_sessions[session_id] = {
            'status': 'starting',
            'accounts': [],
            'success': 0,
            'done': 0,
            'total': count,
            'region': region,
            'name_prefix': name_prefix,
            'started_at': datetime.now().isoformat(),
            'error': None
        }

    t = threading.Thread(
        target=run_generation,
        args=(session_id, count, region, name_prefix),
        daemon=True
    )
    t.start()

    return jsonify({'session_id': session_id, 'message': 'Generation dimulai'})

@app.route('/api/status/<session_id>', methods=['GET'])
@require_auth
def get_status(session_id):
    with generation_lock:
        data = generation_sessions.get(session_id)
    if not data:
        return jsonify({'error': 'Session tidak ditemukan'}), 404
    return jsonify({
        'status': data['status'],
        'success': data['success'],
        'done': data['done'],
        'total': data['total'],
        'accounts': data['accounts'],
        'region': data['region'],
        'error': data['error']
    })

@app.route('/api/check_auth', methods=['GET'])
def check_auth():
    return jsonify({'authenticated': bool(session.get('authenticated'))})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
