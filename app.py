#!/usr/bin/env python3

# =============================================================================

import hmac
import hashlib
import aiohttp
import asyncio
import string
import random
import json
import time
from datetime import datetime
import os
import sys
import base64
import threading
import re
import subprocess
import importlib
import logging
import warnings
import urllib3
import shutil
import platform
import getpass
import socket
import ssl
from collections import deque
from typing import Optional, Dict, Any
import requests
import ipaddress

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# Thread-safe atomic counter for sequential account IDs
_name_counter = 0
_counter_lock = threading.Lock()

# =============================================================================
# 🛡️ ULTIMATE ANTI-CREDIT & FILENAME PROTECTION SYSTEM
# =============================================================================

class SecurityShield:
    """Ultimate protection system - Cannot be bypassed"""

    REQUIRED_FILENAME = "app.py"

    CREDIT_SIGNATURES = [
        "Blinx", "BLINX", "Blinx", "Blinx",
    ]

    WATERMARKS = [
        "ULTIMATE_PROTECTION_v12", "TEAM_GEN_2026", "PROTECTED_BY_Team",
        "SINGLE_USER_MODE"
    ]

    @classmethod
    def verify_filename(cls):
        current = os.path.basename(__file__)
        return current == cls.REQUIRED_FILENAME

    @classmethod
    def verify_credits(cls):
        try:
            with open(__file__, 'r', encoding='utf-8') as f:
                content = f.read()
            for sig in cls.CREDIT_SIGNATURES:
                if sig not in content:
                    return False, f"MISSING: {sig}"
            for mark in cls.WATERMARKS:
                if mark not in content:
                    return False, "WATERMARK MISSING"
            return True, "✓ INTEGRITY VERIFIED"
        except:
            return False, "VERIFICATION FAILED"

    @classmethod
    def show_breach(cls, reason):
        print(f"\n{VISUAL.COLORS['error']}{VISUAL.COLORS['bold']}")
        print(VISUAL.center_text("╔" + "═" * 60 + "╗"))
        print(VISUAL.center_text("║" + " " * 18 + "🚨 SECURITY BREACH 🚨" + " " * 18 + "║"))
        print(VISUAL.center_text("╠" + "═" * 60 + "╣"))
        print(VISUAL.center_text(f"║  {reason:<56} ║"))
        print(VISUAL.center_text("╠" + "═" * 60 + "╣"))
        print(VISUAL.center_text("║  THIS TOOL IS PROTECTED BY Blinx                    ║"))
        print(VISUAL.center_text("║  DO NOT ATTEMPT TO MODIFY CREDITS                      ║"))
        print(VISUAL.center_text("║  OR CHANGE FILENAME!                                   ║"))
        print(VISUAL.center_text("╚" + "═" * 60 + "╝"))
        print(f"{VISUAL.COLORS['reset']}")
        time.sleep(10)
        sys.exit(1)

# =============================================================================
# 🎨 ULTIMATE VISUAL MASTER - DARK GOLD THEME
# =============================================================================

class VisualMaster:
    """Professional visual design system - Dark Gold Cinema UI"""

    COLORS = {
        'primary':   '\033[38;5;51m',
        'secondary': '\033[38;5;45m',
        'success':   '\033[38;5;50m',
        'error':     '\033[38;5;196m',
        'warning':   '\033[38;5;226m',
        'rare':      '\033[38;5;46m',
        'couple':    '\033[38;5;46m',
        'info':      '\033[38;5;87m',
        'highlight': '\033[38;5;123m',
        'dim':       '\033[38;5;37m',
        'owner':     '\033[38;5;51m',
        'admin':     '\033[38;5;45m',
        'user':      '\033[38;5;50m',
        'border':    '\033[38;5;51m',
        'accent':    '\033[38;5;159m',
        'reset':     '\033[0m',
        'bold':      '\033[1m',
        'italic':    '\033[3m',
        'bg_dark':   '\033[48;5;16m',
        'box_red':   '\033[38;5;203m',
        'box_yellow':'\033[38;5;220m',
        'box_green': '\033[38;5;82m',
        'box_blue':  '\033[38;5;39m',
        'box_white': '\033[38;5;255m',
        'box_purple':'\033[38;5;141m',
        'c1':        '\033[38;5;51m',
        'c2':        '\033[38;5;45m',
        'c3':        '\033[38;5;44m',
        'c4':        '\033[38;5;38m',
        'c5':        '\033[38;5;37m',
        'c6':        '\033[38;5;36m',
    }

    ICONS = {
        'success': '✅', 'error': '❌', 'warning': '⚠️',  'info': 'ℹ️',
        'rare': '💎',    'couple': '💑', 'fire': '🔥',    'rocket': '🚀',
        'lock': '🔒',    'key': '🔑',   'shield': '🛡️',  'user': '👤',
        'id': '🆔',      'pass': '🔐',  'time': '⏱️',    'speed': '⚡',
        'target': '🎯',  'folder': '📁','stats': '📊',   'globe': '🌍',
        'thread': '🧵',  'crown': '👑', 'star': '⭐',    'heart': '❤️',
        'admin': '👑',   'owner': '💎', 'user_icon': '👤','edit': '✏️',
        'save': '💾',    'config': '⚙️','custom': '🎨',  'credit': '📝',
        'sword': '⚔️',  'diamond': '🔷',
    }

    BOX = {
        'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝', 'h': '═', 'v': '║',
        'ml': '╠', 'mr': '╣',
    }

    @classmethod
    def center_text(cls, text, width=None):
        if width is None:
            width = shutil.get_terminal_size().columns
        return text.center(width)

    @classmethod
    def create_box(cls, title=None, width=70, height=1):
        lines = []
        C = cls.COLORS
        if title:
            top = f"{C['border']}{cls.BOX['tl']}{cls.BOX['h'] * 2} {C['primary']}{C['bold']}{title}{C['reset']}{C['border']} {cls.BOX['h'] * 2}{cls.BOX['tr']}{C['reset']}"
        else:
            top = f"{C['border']}{cls.BOX['tl']}{cls.BOX['h'] * (width-2)}{cls.BOX['tr']}{C['reset']}"
        lines.append(top)
        for _ in range(height - 1):
            lines.append(f"{C['border']}{cls.BOX['v']}{' ' * (width-2)}{cls.BOX['v']}{C['reset']}")
        bottom = f"{C['border']}{cls.BOX['bl']}{cls.BOX['h'] * (width-2)}{cls.BOX['br']}{C['reset']}"
        lines.append(bottom)
        return lines

    @classmethod
    def create_panel(cls, title, content, width=None, color='primary'):
        if width is None:
            width = shutil.get_terminal_size().columns - 4
        C = cls.COLORS
        lines_content = content.split('\n')
        result = []
        result.append(f"{C['border']}{cls.BOX['tl']}{cls.BOX['h'] * 2} {C[color]}{C['bold']}{title}{C['reset']}{C['border']} {cls.BOX['h'] * max(0, width - len(title) - 6)}{cls.BOX['tr']}{C['reset']}")
        result.append(f"{C['border']}{cls.BOX['v']}{C['reset']}{' ' * (width - 2)}{C['border']}{cls.BOX['v']}{C['reset']}")
        for line in lines_content:
            visible_line = re.sub(r'\033\[[0-9;]*m', '', line)
            pad = max(0, width - len(visible_line) - 4)
            result.append(f"{C['border']}{cls.BOX['v']}{C['reset']}  {C['accent']}{line}{C['reset']}{' ' * pad}  {C['border']}{cls.BOX['v']}{C['reset']}")
        result.append(f"{C['border']}{cls.BOX['v']}{C['reset']}{' ' * (width - 2)}{C['border']}{cls.BOX['v']}{C['reset']}")
        result.append(f"{C['border']}{cls.BOX['bl']}{cls.BOX['h'] * (width - 2)}{cls.BOX['br']}{C['reset']}")
        return '\n'.join(result)

    @classmethod
    def create_progress_bar(cls, current, total, width=50):
        C = cls.COLORS
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = f"{C['primary']}{'█' * filled}{C['dim']}{'░' * (width - filled)}{C['reset']}"
        return f"{bar} {C['bold']}{C['warning']}{percent*100:5.1f}%{C['reset']}"

    @classmethod
    def clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    _header_shown = False

    @classmethod
    def show_header(cls, user_level="USER"):
        if not cls._header_shown:
            cls.clear()
            cls.animate_header(user_level)
            cls._header_shown = True

    @classmethod
    def animate_header(cls, user_level="USER"):
        import sys, time, shutil as _sh
        W   = _sh.get_terminal_size().columns
        C   = cls.COLORS
        R   = C['reset'];  B = C['bold']
        SH = [C['c1'],C['c2'],C['c3'],C['c4'],C['c5'],C['c6'],
              C['c5'],C['c4'],C['c3'],C['c2'],C['c1']]
        rand_chars = list("▓▒░│┼╬╪╫╬▓▒░╔═╗║╚╝╠╣╦╩╬")
        for frame in range(18):
            line = "".join(random.choice(rand_chars) for _ in range(W-2))
            shade = SH[frame % len(SH)]
            sys.stdout.write(f"\r{shade}{B}{line}{R}")
            sys.stdout.flush()
            time.sleep(0.035)
        print()
        for i in range(0, W-2, 6):
            bar = "═" * min(i, W-2)
            sys.stdout.write(f"\r{C['c1']}{B}╔{bar}>{R}")
            sys.stdout.flush()
            time.sleep(0.018)
        sys.stdout.write(f"\r{C['c1']}{B}╔{'═'*(W-2)}╗{R}\n")
        sys.stdout.flush()
        BLINX_ART = [
            "██████╗  ██╗     ██╗ ███╗   ██╗ ██╗  ██╗",
            "██╔══██╗ ██║     ██║ ████╗  ██║ ╚██╗██╔╝",
            "██████╔╝ ██║     ██║ ██╔██╗ ██║  ╚███╔╝ ",
            "██╔══██╗ ██║     ██║ ██║╚██╗██║  ██╔██╗ ",
            "██████╔╝ ███████╗██║ ██║ ╚████║ ██╔╝ ██╗",
        ]
        for i, line in enumerate(BLINX_ART):
            shade = SH[i % len(SH)]
            for end in range(1, len(line)+1, 4):
                sys.stdout.write(f"\r{shade}{B}{line[:end].center(W)}{R}")
                sys.stdout.flush()
                time.sleep(0.006)
            sys.stdout.write(f"\r{shade}{B}{line.center(W)}{R}\n")
            sys.stdout.flush()
        waves = ["≋"*(W-4), "〰"*((W-4)//2), "━"*(W-4), "═"*(W-4)]
        for w in waves:
            sys.stdout.write(f"\r{C['c2']}{B}  {w}  {R}")
            sys.stdout.flush()
            time.sleep(0.05)
        print()

        spin = ["◐","◓","◑","◒","◐","◓","◑","◒","●","○","●"]
        for s in spin:
            sys.stdout.write(f"\r{C['c1']}{B}  {s}  BLINX CODEX  {s}  {R}")
            sys.stdout.flush()
            time.sleep(0.07)
        print()
        lv = f"👤 USER MODE"
        lc = C['c3']
        info = f"◈  OB54 READY  ·  {lv}  ·  v12 PRO  ◈"
        print(f"{lc}{B}{info.center(W)}{R}")
        feat = "⚡ PRO GENERATOR   💎 RARE FINDER   💑 COUPLES   🔥 AUTO ACTIVATOR"
        print(f"{C['c4']}{feat.center(W)}{R}")
        cred = "📱 Blinx  |  Blinx  |  🐙 github.com/generator"
        print(f"{C['c5']}{cred.center(W)}{R}")
        sys.stdout.write(f"\r{C['c1']}{B}╚{'═'*(W-2)}╝{R}\n\n")
        sys.stdout.flush()
        bar_w = min(50, W-20)
        for i in range(bar_w+1):
            filled = "█" * i
            empty  = "░" * (bar_w - i)
            pct    = int(i / bar_w * 100)
            shade  = SH[i % len(SH)]
            sys.stdout.write(f"\r  {C['c2']}LAUNCHING {shade}{B}[{filled}{C['dim']}{empty}{shade}] {pct:3d}%{R}  ")
            sys.stdout.flush()
            time.sleep(0.022)
        print(f"\n  {C['c1']}{B}✔  BLINX PRO CODEX READY!{R}\n")

VISUAL = VisualMaster()

# =============================================================================
# ⚡ FAST REQUIREMENTS INSTALLER
# =============================================================================

def install_requirements():
    required = ['requests', 'pycryptodome', 'colorama', 'psutil', 'protobuf', 'aiohttp']
    print(f"{VISUAL.COLORS['info']}🔧 Checking requirements...{VISUAL.COLORS['reset']}")
    for pkg in required:
        try:
            if pkg == 'pycryptodome':
                import Crypto
            elif pkg == 'requests':
                import requests
            elif pkg == 'aiohttp':
                import aiohttp
            elif pkg == 'colorama':
                from colorama import Fore, Style, init
            elif pkg == 'psutil':
                import psutil
            elif pkg == 'protobuf':
                import google.protobuf
            print(f"{VISUAL.COLORS['success']}✅ {pkg} already installed{VISUAL.COLORS['reset']}")
        except ImportError:
            print(f"{VISUAL.COLORS['info']}📦 Installing {pkg}...{VISUAL.COLORS['reset']}")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', pkg, '-q'], check=True)
                print(f"{VISUAL.COLORS['success']}✅ {pkg} installed{VISUAL.COLORS['reset']}")
            except:
                print(f"{VISUAL.COLORS['warning']}⚠️ {pkg} install failed, continuing...{VISUAL.COLORS['reset']}")
            time.sleep(1)
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
    except:
        pass
    time.sleep(1)

install_requirements()

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    AES_AVAILABLE = True
except:
    AES_AVAILABLE = False
    def aes_encrypt(data): return data.encode() if isinstance(data, str) else data

def enc_varint_sync(n):
    if n < 0: return b''
    H = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n: b |= 0x80
        H.append(b)
        if not n: break
    return bytes(H)

def create_field_varint_sync(fn, val):
    return enc_varint_sync((fn << 3) | 0) + enc_varint_sync(val)

def create_field_len_sync(fn, val):
    h = enc_varint_sync((fn << 3) | 2)
    e = val.encode() if isinstance(val, str) else val
    return h + enc_varint_sync(len(e)) + e

def create_proto_sync(fields):
    p = bytearray()
    for f, v in fields.items():
        if isinstance(v, dict):
            p.extend(create_field_len_sync(f, create_proto_sync(v)))
        elif isinstance(v, int):
            p.extend(create_field_varint_sync(f, v))
        elif isinstance(v, (str, bytes)):
            p.extend(create_field_len_sync(f, v))
    return p

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

NEW_PROTO_AVAILABLE = True

# =============================================================================
# ⚙️ CONFIGURATION
# =============================================================================

class Config:
    VERSION = "12.0 SINGLE OWNER"
    MAX_THREADS = 50
    USER_LEVEL = "OWNER"
    SUCCESS = 0; RARE = 0; COUPLES = 0; ACTIVATED = 0; FAILED = 0; ATTEMPTS = 0
    LOCK = asyncio.Lock()
    EXIT = False
    AUTO_ACT = True
    MAX_RETRIES = 5
    CUSTOM_NAME_PREFIX = "BLINX"
    CUSTOM_PASS_PREFIX = "BLINX"
    RARITY_THRESHOLD = 8
    CUSTOM_TARGET = 999999999
    CURRENT_JSON_BASE = "accounts"
    CURRENT_ACTIVATED_BASE = "accounts-activated"
    
    # All 13 regions with language mapping
    ALL_REGIONS = ["IND", "ID", "TH", "VN", "ME", "BD", "PK", "TW", "EU", "CIS", "NA", "SAC", "BR"]
    REGION_NAMES = {
        "IND": "🇮🇳 India", "ID": "🇮🇩 Indonesia", "TH": "🇹🇭 Thailand", "VN": "🇻🇳 Vietnam",
        "ME": "🌍 Middle East", "BD": "🇧🇩 Bangladesh", "PK": "🇵🇰 Pakistan", "TW": "🇹🇼 Taiwan",
        "EU": "🇪🇺 Europe", "CIS": "🇷🇺 Russia/CIS", "NA": "🇺🇸 North America", "SAC": "🇧🇷 South America",
        "BR": "🇧🇷 Brazil"
    }
    REGION_LANG = {
        "ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th",
        "BD": "bn", "PK": "ur", "TW": "zh", "EU": "en", "CIS": "ru",
        "NA": "en", "SAC": "es", "BR": "pt"
    }
    ACTIVATION_REGIONS = {
        'IND': {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
                'get_login_data_url': 'https://client.ind.freefiremobile.com/GetLoginData',
                'client_host': 'client.ind.freefiremobile.com'},
        'BD':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'PK':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'ID':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'TH':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.common.ggbluefox.com/GetLoginData',
                'client_host': 'clientbp.common.ggbluefox.com'},
        'VN':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'ME':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
        'BR':  {'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
                'major_login_url': 'https://loginbp.ggpolarbear.com/MajorLogin',
                'get_login_data_url': 'https://clientbp.ggpolarbear.com/GetLoginData',
                'client_host': 'clientbp.ggpolarbear.com'},
    }
    HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
    API_KEY  = bytes.fromhex(HEX_KEY)
    REGISTER_URL      = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
    TOKEN_URL         = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
    MAJOR_REGISTER_URL = "https://loginbp.ggpolarbear.com/MajorRegister"
    MAJOR_LOGIN_URL    = "https://loginbp.ggpolarbear.com/MajorLogin"
    CURRENT_DIR            = os.path.dirname(os.path.abspath(__file__))
    BASE_FOLDER            = os.path.join(CURRENT_DIR, "Blinx")
    TOKENS_FOLDER          = os.path.join(BASE_FOLDER, "TOKENS")
    ACCOUNTS_FOLDER        = os.path.join(BASE_FOLDER, "ACCOUNTS")
    RARE_ACCOUNTS_FOLDER   = os.path.join(BASE_FOLDER, "RARE_ACCOUNTS")
    COUPLES_ACCOUNTS_FOLDER= os.path.join(BASE_FOLDER, "COUPLES_ACCOUNTS")
    GHOST_FOLDER           = os.path.join(BASE_FOLDER, "GHOST")
    GHOST_ACCOUNTS_FOLDER  = os.path.join(GHOST_FOLDER, "ACCOUNTS")
    GHOST_RARE_FOLDER      = os.path.join(GHOST_FOLDER, "RARE_ACCOUNTS")
    GHOST_COUPLES_FOLDER   = os.path.join(GHOST_FOLDER, "COUPLES_ACCOUNTS")
    ACTIVATED_FOLDER       = os.path.join(BASE_FOLDER, "ACTIVATED")
    FAILED_ACTIVATION_FOLDER = os.path.join(BASE_FOLDER, "FAILED_ACTIVATION")
    CONFIG_FOLDER          = os.path.join(BASE_FOLDER, "CONFIG")
    BACKUP_FOLDER          = os.path.join(BASE_FOLDER, "BACKUP")

    @classmethod
    def create_folders(cls):
        folders = [
            cls.BASE_FOLDER, cls.TOKENS_FOLDER, cls.ACCOUNTS_FOLDER,
            cls.RARE_ACCOUNTS_FOLDER, cls.COUPLES_ACCOUNTS_FOLDER,
            cls.GHOST_FOLDER, cls.GHOST_ACCOUNTS_FOLDER, cls.GHOST_RARE_FOLDER,
            cls.GHOST_COUPLES_FOLDER, cls.ACTIVATED_FOLDER,
            cls.FAILED_ACTIVATION_FOLDER, cls.CONFIG_FOLDER, cls.BACKUP_FOLDER
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

# =============================================================================
# 🌐 IP ROTATION & PROXY ROTATOR SYSTEM (Natively Enabled)
# =============================================================================

class IPRotator:
    """Handles automatic dynamic IP spoofing and SOCKS/HTTP proxy rotation"""

    # Regional IP blocks (CIDR) to ensure authentic location spoofing per server
    REGION_IP_CIDRS = {
        "BD": [
            "27.147.128.0/17", "37.111.192.0/19", "49.0.32.0/20", "59.152.96.0/20",
            "114.130.0.0/17", "115.127.0.0/17", "119.30.32.0/20", "123.49.0.0/18",
            "103.220.220.0/22", "103.108.140.0/22", "103.242.20.0/22"
        ],
        "IND": [
            "1.6.0.0/15", "1.38.0.0/15", "14.96.0.0/15", "27.4.0.0/14", "27.56.0.0/13"
        ],
        "ID": [
            "36.64.0.0/11", "101.255.0.0/16", "103.10.60.0/22", "114.120.0.0/13"
        ],
        "TH": [
            "1.46.0.0/15", "27.55.0.0/16", "49.228.0.0/15", "101.108.0.0/15"
        ],
        "VN": [
            "1.52.0.0/14", "14.160.0.0/11", "27.64.0.0/12", "113.160.0.0/12"
        ],
        "PK": [
            "39.32.0.0/11", "111.68.96.0/19", "182.176.0.0/12"
        ],
        "ME": [
            "2.88.0.0/13", "5.100.0.0/14", "31.166.0.0/15", "37.104.0.0/13"
        ],
        "BR": [
            "177.0.0.0/13", "186.192.0.0/12", "189.0.0.0/11", "200.96.0.0/12"
        ],
        "EU": [
            "2.16.0.0/12", "5.144.0.0/14", "31.40.0.0/14", "46.16.0.0/14"
        ],
        "CIS": [
            "2.92.0.0/14", "5.136.0.0/13", "31.128.0.0/12", "46.0.0.0/12"
        ],
        "NA": [
            "3.0.0.0/9", "8.0.0.0/12", "12.0.0.0/10", "24.0.0.0/10"
        ],
        "SAC": [
            "186.0.0.0/10", "190.0.0.0/11", "200.0.0.0/11"
        ],
        "TW": [
            "1.160.0.0/12", "36.224.0.0/12", "114.24.0.0/12", "118.160.0.0/12"
        ]
    }

    PROXIES = []
    _proxy_index = 0
    _proxy_lock = threading.Lock()

    @classmethod
    def load_proxies(cls):
        proxy_paths = [
            os.path.join(Config.CONFIG_FOLDER, "proxies.txt"),
            os.path.join(Config.CURRENT_DIR, "proxies.txt"),
            "proxies.txt"
        ]
        for path in proxy_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                    if lines:
                        cls.PROXIES = lines
                        # silent load – no print
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

    @classmethod
    def get_random_ip_from_cidr(cls, cidr: str) -> str:
        """Fast mathematical IP calculation inside CIDR block"""
        try:
            net = ipaddress.IPv4Network(cidr, strict=False)
            num_addresses = net.num_addresses
            if num_addresses > 2:
                offset = random.randint(1, num_addresses - 2)
            else:
                offset = 0
            random_ip_int = int(net.network_address) + offset
            return str(ipaddress.IPv4Address(random_ip_int))
        except Exception:
            return "103.220.220.10"

    @classmethod
    def get_rotating_ip(cls, region: str) -> str:
        if not region:
            region = "BD"
        reg = region.upper()
        if reg in cls.REGION_IP_CIDRS:
            cidr = random.choice(cls.REGION_IP_CIDRS[reg])
        else:
            cidr = random.choice(random.choice(list(cls.REGION_IP_CIDRS.values())))
        return cls.get_random_ip_from_cidr(cidr)

    @classmethod
    def get_headers_with_ip_rotation(cls, base_headers: dict, region: str) -> dict:
        headers = base_headers.copy()
        ip = cls.get_rotating_ip(region)
        headers["X-Forwarded-For"] = ip
        headers["X-Real-IP"] = ip
        headers["Client-IP"] = ip
        headers["CF-Connecting-IP"] = ip
        headers["True-Client-IP"] = ip
        return headers

def safe_name(name):
    if not name or not isinstance(name, str):
        return str(name) if name else "Unknown"
    if "\\u" in name:
        try:
            name = name.encode().decode('unicode_escape')
        except:
            pass
    try:
        test = name.encode('latin-1').decode('utf-8')
        if any(ord(c) > 127 for c in test):
            name = test
    except:
        pass
    if name.startswith("b'") or name.startswith('b"'):
        try:
            name = eval(name).decode('utf-8')
        except:
            pass
    return name

# =============================================================================
# 🔑 ACCOUNT GENERATION HELPERS
# =============================================================================

def generate_sequential_name():
    """Generates sequential ID names: Name_1, Name_2, Name_3, etc."""
    global _name_counter
    base = Config.CUSTOM_NAME_PREFIX if Config.CUSTOM_NAME_PREFIX else "SK"
    with _counter_lock:
        _name_counter += 1
        current_id = _name_counter
    return f"{base}_{current_id}"

def generate_custom_password():
    """BLINX + 4 random capital letters"""
    return "Blinx_" + ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

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

def decode_jwt_noverify(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += '=' * padding
            decoded = base64.urlsafe_b64decode(payload_part)
            return json.loads(decoded)
    except:
        pass
    return {}

def encrypt_api(plain_text):
    if not AES_AVAILABLE:
        return plain_text
    Z = bytes.fromhex(plain_text)
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(Z, AES.block_size)).hex()

# =============================================================================
# 🔐 ASYNC PROTOBUF HELPERS
# =============================================================================

async def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(field_number, value):
    return await EnC_Vr((field_number << 3) | 0) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    h = await EnC_Vr((field_number << 3) | 2)
    e = value.encode() if isinstance(value, str) else value
    return h + await EnC_Vr(len(e)) + e

async def CrEaTe_ProTo(fields):
    p = bytearray()
    for f, v in fields.items():
        if isinstance(v, dict):
            p.extend(await CrEaTe_LenGTh(f, await CrEaTe_ProTo(v)))
        elif isinstance(v, int):
            p.extend(await CrEaTe_VarianT(f, v))
        elif isinstance(v, (str, bytes)):
            p.extend(await CrEaTe_LenGTh(f, v))
    return p

def E_AEs(Pc):
    if not AES_AVAILABLE:
        return bytes.fromhex(Pc)
    Z = bytes.fromhex(Pc)
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    K = AES.new(key, AES.MODE_CBC, iv)
    return K.encrypt(pad(Z, AES.block_size))

# =============================================================================
# 🔌 API CONSTANTS
# =============================================================================

class APIMaster:
    HEX_KEY  = Config.HEX_KEY
    API_KEY  = Config.API_KEY
    API_POOL = [{"id": "100067", "key": Config.API_KEY, "label": f"API {i:02d} ⚡"} for i in range(1, 8)]

    @classmethod
    def init(cls):
        return len(cls.API_POOL)

API_COUNT = APIMaster.init()

# =============================================================================
# 💾 BATCH FILE SAVER (ASYNC)
# =============================================================================

class BatchSaver:
    def __init__(self, filepath):
        self.filepath = filepath
        self.queue = deque()
        self._running = True

    def add(self, entry: Dict[str, Any]):
        self.queue.append(entry)

    async def flush(self):
        if not self.queue:
            return
        batch = []
        while self.queue:
            batch.append(self.queue.popleft())
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            
            existing = []
            if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if content.strip():
                    try:
                        existing = json.loads(content)
                        if not isinstance(existing, list):
                            existing = []
                    except json.JSONDecodeError:
                        try:
                            existing = [json.loads(line) for line in content.splitlines() if line.strip()]
                        except:
                            existing = []
            existing.extend(batch)
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            try:
                recovery_path = self.filepath + ".recovery"
                with open(recovery_path, 'a', encoding='utf-8') as rf:
                    for entry in batch:
                        rf.write(json.dumps(entry, ensure_ascii=False) + '\n')
            except:
                pass

    async def periodic_flush(self, interval=2):
        while self._running:
            await asyncio.sleep(interval)
            await self.flush()

    def stop(self):
        self._running = False

# Global batch savers (created on demand)
batch_savers = {}  # filepath -> BatchSaver

async def flush_all_savers():
    for saver in batch_savers.values():
        await saver.flush()

def get_batch_saver(filepath):
    if filepath not in batch_savers:
        batch_savers[filepath] = BatchSaver(filepath)
    return batch_savers[filepath]

# =============================================================================
# 🔄 COUPLES DETECTION
# =============================================================================

POTENTIAL_COUPLES = {}
COUPLES_LOCK = asyncio.Lock()

# =============================================================================
# 💎 RARITY DETECTION
# =============================================================================

ACCOUNT_RARITY_PATTERNS = {
    "REPEATED_DIGITS_4":       [r"(\d)\1{3,}", 3],
    "REPEATED_DIGITS_3":       [r"(\d)\1\1(\d)\2\2", 2],
    "SEQUENTIAL_5":            [r"(12345|23456|34567|45678|56789)", 4],
    "SEQUENTIAL_4":            [r"(0123|1234|2345|3456|4567|45678|5678|6789|9876|8765|7654|6543|5432|4321|3210)", 3],
    "PALINDROME_6":            [r"^(\d)(\d)(\d)\3\2\1$", 5],
    "PALINDROME_4":            [r"^(\d)(\d)\2\1$", 3],
    "SPECIAL_COMBINATIONS_HIGH":[r"(69|420|1337|007)", 4],
    "SPECIAL_COMBINATIONS_MED": [r"(100|200|300|400|500|666|777|888|999)", 2],
    "QUADRUPLE_DIGITS":        [r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)", 4],
    "MIRROR_PATTERN_HIGH":     [r"^(\d{2,3})\1$", 3],
    "MIRROR_PATTERN_MED":      [r"(\d{2})0\1", 2],
    "GOLDEN_RATIO":            [r"1618|0618", 3],
}

def check_account_rarity(account_data):
    account_id = account_data.get("account_id", "")
    if account_id == "N/A" or not account_id:
        return False, None, None, 0
    rarity_score = 0
    detected_patterns = []
    for rarity_type, pattern_data in ACCOUNT_RARITY_PATTERNS.items():
        if re.search(pattern_data[0], account_id):
            rarity_score += pattern_data[1]
            detected_patterns.append(rarity_type)
    digits = [int(d) for d in account_id if d.isdigit()]
    if len(set(digits)) == 1 and len(digits) >= 4:
        rarity_score += 5; detected_patterns.append("UNIFORM_DIGITS")
    if len(digits) >= 4:
        diffs = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        if len(set(diffs)) == 1:
            rarity_score += 4; detected_patterns.append("ARITHMETIC_SEQUENCE")
    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        rarity_score += 3; detected_patterns.append("LOW_ACCOUNT_ID")
    if rarity_score >= Config.RARITY_THRESHOLD:
        reason = f"ID {account_id} — Score: {rarity_score} — Patterns: {', '.join(detected_patterns)}"
        return True, "RARE_ACCOUNT", reason, rarity_score
    return False, None, None, rarity_score

async def check_account_couples(account_data, thread_id):
    account_id = account_data.get("account_id", "")
    if account_id == "N/A" or not account_id:
        return False, None, None
    async with COUPLES_LOCK:
        for stored_id, stored_data in list(POTENTIAL_COUPLES.items()):
            couple_found, reason = check_account_couple_patterns(account_id, stored_data.get('account_id', ''))
            if couple_found:
                partner_data = stored_data
                del POTENTIAL_COUPLES[stored_id]
                return True, reason, partner_data
        POTENTIAL_COUPLES[account_id] = {
            'uid': account_data.get('uid',''), 'account_id': account_id,
            'name': account_data.get('name',''), 'password': account_data.get('password',''),
            'region': account_data.get('region',''), 'thread_id': thread_id,
            'timestamp': datetime.now().isoformat()
        }
    return False, None, None

def check_account_couple_patterns(a1, a2):
    if a1 and a2 and abs(int(a1) - int(a2)) == 1:
        return True, f"Sequential IDs: {a1} & {a2}"
    if a1 == a2[::-1]:
        return True, f"Mirror IDs: {a1} & {a2}"
    if a1 and a2:
        s = int(a1) + int(a2)
        if s % 1000 == 0 or s % 10000 == 0:
            return True, f"Complementary sum: {a1}+{a2}={s}"
    for ln in ['520','521','1314','3344']:
        if ln in a1 and ln in a2:
            return True, f"Both contain love number: {ln}"
    return False, None

def print_rarity_found(account_data, rarity_type, reason, rarity_score):
    RED  = '\033[38;5;196m'
    RED2 = '\033[38;5;160m'
    B = VISUAL.COLORS['bold']; R = VISUAL.COLORS['reset']
    W = 54
    print(f"{RED}{B}╔{'═'*W}╗{R}")
    print(f"{RED}{B}║{'💎  RARE ACCOUNT FOUND!  💎'.center(W)}║{R}")
    print(f"{RED}{B}╠{'═'*W}╣{R}")
    def row(k, v):
        print(f"{RED}{B}║{R}  {RED2}{k}{R}: {RED}{B}{v}{R}{' '*(W-len(k)-len(str(v))-6)}{RED}{B}║{R}")
    row("🎯 Type   ", str(rarity_type))
    row("⭐ Score  ", str(rarity_score))
    name = safe_name(account_data['name'])
    row("👤 Name    ", name[:30])
    row("🆔 UID     ", str(account_data['uid']))
    row("🎮 Acct ID ", account_data.get('account_id', 'N/A'))
    row("📝 Reason ", reason[:45])
    print(f"{RED}{B}╠{'═'*W}╣{R}")
    print(f"{RED}{B}║{'🔴  SAVED TO RARE ACCOUNTS  🔴'.center(W)}║{R}")
    print(f"{RED}{B}╚{'═'*W}╝{R}\n")

def print_couples_found(account1, account2, reason):
    GRN  = '\033[38;5;46m'
    GRN2 = '\033[38;5;40m'
    GRN3 = '\033[38;5;34m'
    B = VISUAL.COLORS['bold']; R = VISUAL.COLORS['reset']
    W = 58
    print(f"{GRN}{B}╔{'═'*W}╗{R}")
    print(f"{GRN}{B}║{'💑  COUPLES ACCOUNT FOUND!  💑'.center(W)}║{R}")
    print(f"{GRN}{B}╠{'═'*W}╣{R}")
    def row(k, v):
        print(f"{GRN}{B}║{R}  {GRN3}{k}{R}: {GRN}{B}{v}{R}{' '*(W-len(k)-len(str(v))-6)}{GRN}{B}║{R}")
    row("📝 Reason  ", reason)
    print(f"{GRN}{B}╠{'─'*W}╣{R}")
    print(f"{GRN}{B}║{'  ACCOUNT  1  '.center(W)}║{R}")
    row("👤 Name    ", safe_name(account1['name'])[:30])
    row("🆔 UID     ", str(account1.get('uid','N/A')))
    row("🎮 Acct ID ", account1.get('account_id','N/A'))
    print(f"{GRN}{B}╠{'─'*W}╣{R}")
    print(f"{GRN}{B}║{'  ACCOUNT  2  '.center(W)}║{R}")
    row("👤 Name    ", safe_name(account2['name'])[:30])
    row("🆔 UID     ", str(account2.get('uid','N/A')))
    row("🎮 Acct ID ", account2.get('account_id','N/A'))
    print(f"{GRN}{B}╠{'═'*W}╣{R}")
    print(f"{GRN}{B}║{'💚  SAVED TO COUPLES FILE  💚'.center(W)}║{R}")
    print(f"{GRN}{B}╚{'═'*W}╝{R}\n")

def print_registration_status(count, total, name, uid, password, account_id, region, is_ghost=False):
    """Print account details without activation or bio status"""
    C   = VISUAL.COLORS
    R   = C['reset']; B = C['bold']
    W   = 58
    HDR_C = '\033[38;5;46m'
    LBL_C = '\033[38;5;87m'
    VAL_C = '\033[38;5;255m'
    ACC_C = '\033[38;5;226m'
    BDR_C = '\033[38;5;51m'
    hdr_txt  = f"🎉  ACCOUNT GENERATED!"
    print(f"{BDR_C}╔{'═'*W}╗{R}")
    print(f"{BDR_C}║{R} {HDR_C}{B}{hdr_txt}{R}{' '*(W-2-len(hdr_txt))} {BDR_C}║{R}")
    print(f"{BDR_C}╠{'═'*W}╣{R}")
    def row(icon, key, val, vc=VAL_C):
        label = f"{icon} {key:<12}"
        col_label = f"{LBL_C}{B}{label}{R}"
        val_s = str(val)
        space = W - 4 - len(label)
        if len(val_s) > space:
            col_val = f"{vc}{val_s[:space-3]}...{R}"
        else:
            col_val = f"{vc}{val_s}{R}"
            pad = space - len(val_s)
        print(f"{BDR_C}│{R} {col_label}{col_val}{' '*(W-4-len(label)-len(val_s))} {BDR_C}│{R}")
    row("🆔", "Sequential:", f"Id {count}")
    row("🆔", "UID:",        str(uid))
    pwd_display = str(password)[:4] + "*"*(len(password)-4)
    row("🔑", "Password:",   pwd_display)
    row("👤", "Name:",       str(name)[:20])
    row("🎮", "Account ID:", str(account_id), ACC_C)
    print(f"{BDR_C}╚{'═'*W}╝{R}\n")

# =============================================================================
# 🔥 SAFE ACTIVATION FUNCTIONS – SILENT
# =============================================================================

def build_safe_major_login_payload(open_id, access_token):
    """Build proper MajorLogin protobuf"""
    try:
        fields = {
            3: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            83: "2019116753",
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
        proto_bytes = create_proto_sync(fields)
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(proto_bytes, AES.block_size))
        return encrypted
    except Exception as e:
        return None

def parse_safe_major_login_response(response_bytes):
    try:
        parsed = decode_proto(response_bytes)
        token = parsed.get(8, b'').decode('utf-8', errors='ignore')
        key = parsed.get(22, b'')
        iv = parsed.get(23, b'')
        region = parsed.get(2, b'').decode('utf-8', errors='ignore')
        url = parsed.get(10, b'').decode('utf-8', errors='ignore')
        if token:
            return {
                'token': token,
                'key': key.hex(),
                'iv': iv.hex(),
                'region': region,
                'url': url
            }
    except Exception as e:
        pass
    return None

def major_login_safe(access_token, open_id, region=None, proxies=None):
    payload = build_safe_major_login_payload(open_id, access_token)
    if not payload:
        return None
        
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB54',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Connection': 'Keep-Alive',
    }
    headers = IPRotator.get_headers_with_ip_rotation(headers, region)
    try:
        response = requests.post(Config.MAJOR_LOGIN_URL, headers=headers, data=payload, verify=False, timeout=15, proxies=proxies)
        if response.status_code == 200 and len(response.content) > 0:
            return response.content
        else:
            return None
    except Exception as e:
        return None

def build_get_login_data_payload(jwt_token, access_token):
    try:
        token_payload_base64 = jwt_token.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
        payload_dict = json.loads(decoded_payload)
        external_id = payload_dict['external_id']
        signature_md5 = payload_dict['signature_md5']
        
        major_login.is_vpn = 1
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        
        proto_bytes = major_login.SerializeToString()
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(proto_bytes, AES.block_size))
        return encrypted
    except Exception as e:
        return None

def get_login_data_safe(jwt_token, access_token, base_url, region=None, proxies=None):
    payload = build_get_login_data_payload(jwt_token, access_token)
    if not payload:
        return False
    url = f"{base_url}/GetLoginData"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB54',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    headers = IPRotator.get_headers_with_ip_rotation(headers, region)
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False, timeout=15, proxies=proxies)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def activate_account(uid, password, region=None):
    """Activate account silently – returns True/False"""
    # Step 1: Guest token
    guest_url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    guest_headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G960F Build/PIE)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close"
    }
    guest_headers = IPRotator.get_headers_with_ip_rotation(guest_headers, region)
    
    proxy = IPRotator.get_rotating_proxy()
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    guest_data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        resp = requests.post(guest_url, headers=guest_headers, data=guest_data, verify=False, timeout=15, proxies=proxies)
        if resp.status_code != 200:
            return False
        gjson = resp.json()
        access_token = gjson.get('access_token')
        open_id = gjson.get('open_id')
        if not access_token or not open_id:
            return False
    except:
        return False
    
    # Step 2: MajorLogin safe
    major_response = major_login_safe(access_token, open_id, region, proxies)
    if not major_response:
        return False
    
    # Step 3: Parse response
    login_data = parse_safe_major_login_response(major_response)
    if not login_data:
        return False
    
    jwt_token = login_data['token']
    base_url = login_data['url']
    
    # Step 4: GetLoginData
    success = get_login_data_safe(jwt_token, access_token, base_url, region, proxies)
    return success

# =============================================================================
# 🚀 ASYNC WORKER (generate sequential account and handle save)
# =============================================================================

async def async_worker(session: aiohttp.ClientSession, region: str, total_accounts: int, thread_id: int, semaphore: asyncio.Semaphore, is_ghost: bool, counters: Dict[str, Any]):
    while not Config.EXIT:
        async with Config.LOCK:
            if counters['success'] >= total_accounts:
                break
        account_data = await create_acc_async(session, region, is_ghost, semaphore)
        if account_data is None:
            continue
        
        # Skip if account_id is N/A (do not count, save, or print)
        if account_data.get('account_id') == "N/A":
            continue
        
        # valid account: update counters
        async with Config.LOCK:
            counters['success'] += 1
            current = counters['success']
            counters['attempts'] += 1
        
        # ---- SILENT ACTIVATION ----
        activated = False
        jwt_token = account_data.get('jwt_token', '')
        
        if Config.AUTO_ACT:
            activated = await asyncio.get_event_loop().run_in_executor(
                None, activate_account, account_data['uid'], account_data['password'], region
            )
            if activated:
                async with Config.LOCK:
                    counters['activated'] += 1
                account_data['tcp_activated'] = True
                save_activated_account_async(account_data, is_ghost)
            else:
                async with Config.LOCK:
                    counters['failed'] += 1
                save_failed_activation_async(account_data, is_ghost, reason="TCP activation failed")
        
        account_data['tcp_activated'] = activated
        
        # rare check
        is_rare, rtype, rreason, rscore = check_account_rarity(account_data)
        if is_rare:
            async with Config.LOCK:
                counters['rare'] += 1
            save_rare_account_async(account_data, rtype, rreason, rscore, is_ghost)
            print_rarity_found(account_data, rtype, rreason, rscore)
        
        # couples check
        is_couple, couple_reason, partner = await check_account_couples(account_data, thread_id)
        if is_couple and partner:
            async with Config.LOCK:
                counters['couples'] += 1
            save_couples_account_async(account_data, partner, couple_reason, is_ghost)
            print_couples_found(account_data, partner, couple_reason)
        
        # save normal account
        save_normal_account_async(account_data, region, is_ghost)
        
        # print registration status (without activation/bio info)
        print_registration_status(current, total_accounts, safe_name(account_data['name']),
                                  account_data['uid'], account_data['password'],
                                  account_data['account_id'], region, is_ghost)

# Batch save wrappers (async)
def save_normal_account_async(account_data, region, is_ghost):
    name = safe_name(account_data["name"])
    if is_ghost:
        filepath = os.path.join(Config.GHOST_ACCOUNTS_FOLDER, "ghost.json")
    else:
        json_base = Config.CURRENT_JSON_BASE
        filepath = os.path.join(Config.ACCOUNTS_FOLDER, f"{json_base}.json")
    entry = {
        'uid': account_data["uid"], 'password': account_data["password"],
        'account_id': account_data.get("account_id","N/A"), 'name': name,
        'region': "SK" if is_ghost else region,
        'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'activated': account_data.get('tcp_activated', False)
    }
    saver = get_batch_saver(filepath)
    saver.add(entry)

def save_rare_account_async(account_data, rarity_type, reason, rarity_score, is_ghost):
    if rarity_score < 3:
        return
    filename = (os.path.join(Config.GHOST_RARE_FOLDER, "rare-ghost.json") if is_ghost
                else os.path.join(Config.RARE_ACCOUNTS_FOLDER, f"RARE_{account_data.get('region','UNKNOWN')}.json"))
    entry = {
        'uid': account_data["uid"], 'password': account_data["password"],
        'account_id': account_data.get("account_id","N/A"), 'name': safe_name(account_data["name"]),
        'region': "SK" if is_ghost else account_data.get('region','UNKNOWN'),
        'rarity_type': rarity_type, 'rarity_score': rarity_score, 'reason': reason,
        'date_identified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'activated': account_data.get('tcp_activated', False)
    }
    saver = get_batch_saver(filename)
    saver.add(entry)

def save_couples_account_async(account1, account2, reason, is_ghost):
    region = account1.get('region','UNKNOWN')
    filename = (os.path.join(Config.GHOST_COUPLES_FOLDER, "couples-ghost.json") if is_ghost
                else os.path.join(Config.COUPLES_ACCOUNTS_FOLDER, f"couples-{region}.json"))
    entry = {
        'couple_id': f"{account1.get('account_id','N/A')}_{account2.get('account_id','N/A')}",
        'account1': {'uid': account1["uid"], 'password': account1["password"],
                     'account_id': account1.get("account_id","N/A"), 'name': safe_name(account1["name"]),
                     'activated': account1.get('tcp_activated', False)},
        'account2': {'uid': account2["uid"], 'password': account2["password"],
                     'account_id': account2.get("account_id","N/A"), 'name': safe_name(account2["name"]),
                     'activated': account2.get('tcp_activated', False)},
        'reason': reason, 'region': "SK" if is_ghost else region,
        'date_matched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    saver = get_batch_saver(filename)
    saver.add(entry)

def save_activated_account_async(account_data, is_ghost):
    """Save successfully activated account"""
    name = safe_name(account_data["name"])
    if is_ghost:
        filepath = os.path.join(Config.GHOST_FOLDER, "activated-ghost.json")
    else:
        json_base = Config.CURRENT_ACTIVATED_BASE
        filepath = os.path.join(Config.ACTIVATED_FOLDER, f"{json_base}.json")
    entry = {
        'uid': account_data["uid"],
        'password': account_data["password"],
        'account_id': account_data.get("account_id", "N/A"),
        'name': name,
        'region': account_data.get('region', ''),
        'jwt_token': account_data.get('jwt_token', ''),
        'date_activated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    saver = get_batch_saver(filepath)
    saver.add(entry)

def save_failed_activation_async(account_data, is_ghost, reason="Unknown"):
    """Save failed activation account"""
    name = safe_name(account_data["name"])
    if is_ghost:
        filepath = os.path.join(Config.GHOST_FOLDER, "failed-ghost.json")
    else:
        filepath = os.path.join(Config.FAILED_ACTIVATION_FOLDER, f"failed_{account_data.get('region', 'UNKNOWN')}.json")
    entry = {
        'uid': account_data["uid"],
        'password': account_data["password"],
        'account_id': account_data.get("account_id", "N/A"),
        'name': name,
        'region': account_data.get('region', ''),
        'jwt_token': account_data.get('jwt_token', ''),
        'fail_reason': reason,
        'date_failed': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    saver = get_batch_saver(filepath)
    saver.add(entry)

# =============================================================================
# 🔌 ASYNC ACCOUNT CREATION (core engine)
# =============================================================================

async def create_acc_async(session: aiohttp.ClientSession, region: str, is_ghost: bool, semaphore: asyncio.Semaphore):
    async with semaphore:
        for attempt in range(Config.MAX_RETRIES):
            try:
                password = generate_custom_password()
                
                # Fetch rotating proxy configuration
                proxy = IPRotator.get_rotating_proxy()
                
                # ── STEP 1: Register ──
                payload_reg = json.dumps({
                    "app_id": 100067, 
                    "client_type": 2, 
                    "password": password, 
                    "source": 2
                }, separators=(',', ':'))
                
                signature_reg = hmac.new(
                    Config.API_KEY, 
                    payload_reg.encode(), 
                    hashlib.sha256
                ).hexdigest()
                
                timestamp = str(int(time.time() * 1000))
                
                headers_reg = {
                    "User-Agent": "GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)",
                    "Authorization": f"Signature {signature_reg}",
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                    "Connection": "Keep-Alive",
                    "Host": "100067.connect.garena.com",
                    "X-Garena-Timestamp": timestamp,
                }
                headers_reg = IPRotator.get_headers_with_ip_rotation(headers_reg, region)
                
                async with session.post(
                    Config.REGISTER_URL, 
                    data=payload_reg, 
                    headers=headers_reg, 
                    ssl=False,
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status != 200:
                        continue
                    reg_json = await resp.json()
                    if reg_json.get("code") != 0:
                        continue
                    uid = reg_json['data']['uid']
                
                # ── STEP 2: Token ──
                payload_tok = json.dumps({
                    "client_id": 100067,
                    "client_secret": Config.HEX_KEY,
                    "client_type": 2,
                    "password": password,
                    "response_type": "token",
                    "uid": uid,
                }, separators=(',', ':'))
                
                signature_tok = hmac.new(
                    Config.API_KEY, 
                    payload_tok.encode(), 
                    hashlib.sha256
                ).hexdigest()
                
                headers_tok = {
                    "User-Agent": "GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)",
                    "Authorization": f"Signature {signature_tok}",
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                    "Connection": "Keep-Alive",
                    "Host": "100067.connect.garena.com",
                    "X-Garena-Timestamp": timestamp,
                }
                headers_tok = IPRotator.get_headers_with_ip_rotation(headers_tok, region)
                
                async with session.post(
                    Config.TOKEN_URL, 
                    data=payload_tok, 
                    headers=headers_tok, 
                    ssl=False,
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status != 200:
                        continue
                    tok_json = await resp.json()
                    if tok_json.get("code") != 0:
                        continue
                    access_token = tok_json['data']['access_token']
                    open_id = tok_json['data']['open_id']
                
                # ── STEP 3: MajorRegister (Consecutive name ID) ──
                name = generate_sequential_name()
                account_data = await _major_register_and_login_async(
                    session, uid, password, access_token, open_id, name, region, is_ghost, proxy=proxy
                )
                
                if account_data and account_data.get('account_id') != "N/A":
                    return account_data
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                # silent – no debug prints
                continue
            
            await asyncio.sleep(random.uniform(0.5, 1.5))
        
        return None

async def _major_register_and_login_async(session, uid, password, access_token, open_id, name, region, is_ghost, proxy=None):
    try:
        keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
                     0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
        encoded_open_id = ""
        for i, ch in enumerate(open_id):
            encoded_open_id += chr(ord(ch) ^ keystream[i % len(keystream)])
        field14 = encoded_open_id.encode('latin1')
        lang_code = "pt" if is_ghost else Config.REGION_LANG.get(region.upper(), "en")
        payload_fields = {
            1: name, 2: access_token, 3: open_id,
            5: 102000007, 6: 4, 7: 1, 13: 1,
            14: field14, 15: lang_code, 16: 1, 17: 1
        }
        proto_bytes = await CrEaTe_ProTo(payload_fields)
        encrypted_payload = E_AEs(bytes(proto_bytes).hex())
        headers_reg = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggpolarbear.com",
            "ReleaseVersion": "OB54",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "1.126.2",
        }
        headers_reg = IPRotator.get_headers_with_ip_rotation(headers_reg, region)
        async with session.post(Config.MAJOR_REGISTER_URL, data=encrypted_payload, headers=headers_reg, ssl=False, proxy=proxy) as resp:
            if resp.status != 200:
                return None
        # MajorLogin
        login_result = await _perform_major_login_async(session, uid, password, access_token, open_id, region, is_ghost, proxy=proxy)
        if login_result is None:
            return None
        account_id = login_result.get("account_id", "N/A")
        jwt_token  = login_result.get("jwt_token", "")
        # Return account data
        return {
            "uid": uid, "password": password, "name": name,
            "region": "GHOST" if is_ghost else region,
            "status": "success", "account_id": account_id,
            "jwt_token": jwt_token, "tcp_activated": False
        }
    except Exception as e:
        return None

async def _encrypt_major_login_proto(open_id, access_token):
    if not AES_AVAILABLE:
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
        serialized = await CrEaTe_ProTo(fields)
        key_b = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
        iv_b  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
        cipher = AES.new(key_b, AES.MODE_CBC, iv_b)
        return cipher.encrypt(pad(serialized, AES.block_size))
    except Exception as e:
        return None

async def _perform_major_login_async(session, uid, password, access_token, open_id, region, is_ghost=False, proxy=None):
    url = Config.MAJOR_LOGIN_URL
    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "Host": "loginbp.ggpolarbear.com",
        "ReleaseVersion": "OB54",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1",
    }
    headers = IPRotator.get_headers_with_ip_rotation(headers, region)
    final_payload = None
    if NEW_PROTO_AVAILABLE and AES_AVAILABLE:
        final_payload = await _encrypt_major_login_proto(open_id, access_token)
    if final_payload is None:
        # fallback: use legacy binary payload (simplified for speed)
        return {"account_id": "N/A", "jwt_token": ""}
    try:
        async with session.post(url, data=final_payload, headers=headers, ssl=False, proxy=proxy) as resp:
            if resp.status == 200:
                content = await resp.read()
                if NEW_PROTO_AVAILABLE:
                    try:
                        parsed = decode_proto(content)
                        token = parsed.get(8, b'').decode('utf-8', errors='ignore')
                        if token:
                            account_uid = parsed.get(1)
                            account_id = str(account_uid) if account_uid else decode_jwt_token(token)
                            return {"account_id": account_id, "jwt_token": token}
                    except:
                        pass
                text = content.decode('utf-8', errors='ignore')
                jwt_start = text.find("eyJ")
                if jwt_start != -1:
                    jwt_token = text[jwt_start:]
                    second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                    if second_dot != -1:
                        jwt_token = jwt_token[:second_dot + 44]
                        account_id = decode_jwt_token(jwt_token)
                        return {"account_id": account_id, "jwt_token": jwt_token}
    except:
        pass
    return {"account_id": "N/A", "jwt_token": ""}

# =============================================================================
# ✍️ MAIN GENERATION ASYNC FLOW
# =============================================================================

async def generate_accounts_flow_async():
    VISUAL.show_header(Config.USER_LEVEL)
    C = VISUAL.COLORS

    # Custom name prefix
    print(VISUAL.create_panel("👤 CUSTOM ACCOUNT NAME", "Enter name prefix:"))
    custom_name = input(f"{C['primary']}👉 Name prefix (default: BLINX): {C['reset']}").strip()
    if not custom_name:
        custom_name = "BLINX"
    Config.CUSTOM_NAME_PREFIX = custom_name

    # JSON file name
    print(VISUAL.create_panel("💾 JSON FILE NAME", "Save file name (without .json):"))
    json_base_name = "accounts"
    if not json_base_name:
        json_base_name = "accounts"

    # Region selection - all 13 regions + GHOST mode
    regions_to_show = Config.ALL_REGIONS
    region_menu = ""
    for i, region in enumerate(regions_to_show, 1):
        region_menu += f"{i}) {region}  ({Config.REGION_NAMES.get(region, region)})\n"
    region_menu += f"{len(regions_to_show)+1}) 👻 GHOST Mode (BR region with ghost flag)\n00) ⬅️  BACK\n000) 🚪 EXIT"
    print(VISUAL.create_panel("🌍 SELECT REGION", region_menu))
    while True:
        choice = input(f"{C['primary']}🎯 Choose: {C['reset']}").strip().upper()
        if choice == "00":
            return
        elif choice == "000":
            sys.exit(0)
        elif choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(regions_to_show):
                selected_region = regions_to_show[n - 1]
                is_ghost = False
                break
            elif n == len(regions_to_show) + 1:
                selected_region = "BR"
                is_ghost = True
                break
        elif choice in Config.ALL_REGIONS:
            selected_region = choice
            is_ghost = False
            break
        elif choice == "GHOST":
            selected_region = "BR"
            is_ghost = True
            break
        else:
            print("Invalid option")

    VISUAL.show_header(Config.USER_LEVEL)
    account_count = Config.CUSTOM_TARGET
    Config.CURRENT_JSON_BASE = f"{json_base_name}-{selected_region.lower()}"
    Config.CURRENT_ACTIVATED_BASE = f"{json_base_name}-{selected_region.lower()}-activated"

    config_text = f"""🎯 Target      : {account_count}
⚡ Concurrency : {Config.MAX_THREADS} (async)
🔌 Auto Act     : {Config.AUTO_ACT}
🌍 Region      : {'GHOST' if is_ghost else selected_region}
👤 Acc Name    : {Config.CUSTOM_NAME_PREFIX} (Sequential Counts)
💾 JSON File   : {Config.CURRENT_JSON_BASE}.json
🌐 IP Rotation : ACTIVE (Dynamic Region Spoofing)"""
    print(VisualMaster.create_panel("🚀 GENERATION CONFIG", config_text))
    print(f"\n{C['warning']}⏳ Starting in 3 seconds...{C['reset']}")
    await asyncio.sleep(3)

    counters = {
        'success': 0,
        'rare': 0,
        'couples': 0,
        'activated': 0,
        'failed': 0,
        'attempts': 0,
    }

    semaphore = asyncio.Semaphore(Config.MAX_THREADS)
    start_time = time.time()
    
    connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300, force_close=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(Config.MAX_THREADS):
            task = asyncio.create_task(async_worker(session, selected_region, account_count, i+1, semaphore, is_ghost, counters))
            tasks.append(task)

        # Background batch saver flusher
        flusher_task = asyncio.create_task(flush_all_savers_periodically(2))
        try:
            await asyncio.gather(*tasks)
        finally:
            Config.EXIT = True
            flusher_task.cancel()
            await flush_all_savers()

    elapsed = time.time() - start_time
    total_success = counters['success']
    speed = total_success / elapsed if elapsed > 0 else 0
    final_stats = f"""📊 Generated : {total_success}/{account_count}
💎 Rare      : {counters['rare']}
💑 Couples   : {counters['couples']}
✅ Activated : {counters['activated']}
❌ Failed Act: {counters['failed']}
⏱️  Time     : {elapsed:.2f}s
⚡ Speed     : {speed:.2f} acc/s"""
    print(VISUAL.create_panel("🎉 GENERATION COMPLETE!", final_stats))
    input(f"\n{C['warning']}⏎ Press Enter...{C['reset']}")

async def flush_all_savers_periodically(interval):
    while not Config.EXIT:
        await asyncio.sleep(interval)
        await flush_all_savers()

# =============================================================================
# 📝 SYNCHRONOUS MENU WRAPPERS (call async flows)
# =============================================================================

def generate_accounts_flow():
    asyncio.run(generate_accounts_flow_async())

def view_saved_accounts():
    VISUAL.show_header(Config.USER_LEVEL)
    folders = [Config.ACCOUNTS_FOLDER, Config.ACTIVATED_FOLDER,
               Config.RARE_ACCOUNTS_FOLDER, Config.COUPLES_ACCOUNTS_FOLDER]
    total = 0
    results = ""
    for folder in folders:
        if os.path.exists(folder):
            for file in [f for f in os.listdir(folder) if f.endswith('.json')]:
                filepath = os.path.join(folder, file)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    results += f"📄 {os.path.basename(folder)}/{file}: {len(data)} accounts\n"
                    total += len(data)
                except:
                    pass
    results += f"\n📊 TOTAL: {total} accounts"
    print(VISUAL.create_panel("📁 SAVED ACCOUNTS", results))
    input(f"\n{VISUAL.COLORS['warning']}⏎ Press Enter...{VISUAL.COLORS['reset']}")

def show_stats():
    VISUAL.show_header(Config.USER_LEVEL)
    stats = f"""SESSION STATISTICS (approximate)
━━━━━━━━━━━━━━━━━━━━━━
⚡ Async Engine Active
🔌 APIs      : {API_COUNT}
👤 Level     : {Config.USER_LEVEL}
⚡ Concurrency: {Config.MAX_THREADS}
✅ Auto Act   : {Config.AUTO_ACT}
🔑 Proxies   : {len(IPRotator.PROXIES) if IPRotator.PROXIES else 'OFF'}"""
    print(VISUAL.create_panel("📈 STATISTICS", stats))
    input(f"\n{VISUAL.COLORS['warning']}⏎ Press Enter...{VISUAL.COLORS['reset']}")

def about():
    VISUAL.show_header(Config.USER_LEVEL)
    about_text = f"""🔥 BLINX ULTIMATE PRO GENERATOR v12.0
💎 Created by : Blinx
📱 Telegram   : Blinx, Blinx

✨ FEATURES:
• {API_COUNT} Working APIs (OB54 updated)
• Async aiohttp engine (10+ acc/sec)
• Sequential Name ID Counting (Id 1, Id 2, Id 3...)
• Batch file saving
• Auto Activation (Safe TCP) – Silent
• Rare Finder & Couples Detector
• Dynamic Location IP Spoofing (All 13 Servers)
• Real-time statistics · Dark Gold UI

⚠️ DO NOT REMOVE CREDITS
🔒 Protected by TEAM"""
    print(VISUAL.create_panel("ℹ️  ABOUT", about_text))
    input(f"\n{VISUAL.COLORS['warning']}⏎ Press Enter...{VISUAL.COLORS['reset']}")

def main_menu():
    Config.create_folders()
    IPRotator.load_proxies()  # silent load
    while True:
        VISUAL.show_header(Config.USER_LEVEL)
        C = VISUAL.COLORS
        menu = """1) 🚀 Generate Accounts (Async Fast)
2) 📁 View Saved Accounts
3) 📊 Statistics
4) ⁉️  About
5) 🚪 Exit"""
        print(VISUAL.create_panel("📌 MAIN MENU", menu))
        choice = input(f"{C['primary']}🎯 Choose: {C['reset']}").strip()
        if choice == "1":
            generate_accounts_flow()
        elif choice == "2":
            view_saved_accounts()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            about()
        elif choice == "5":
            sys.exit(0)
        else:
            print("Invalid")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(0)