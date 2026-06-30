import asyncio
import aiohttp
import json
import hmac
import hashlib
import time

HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
API_KEY = bytes.fromhex(HEX_KEY)
REGISTER_URL = "https://100067.connect.garena.com/api/v2/oauth/guest:register"

async def test_direct():
    async with aiohttp.ClientSession() as session:
        payload_reg = json.dumps({
            "app_id": 100067, "client_type": 2,
            "password": "Blinx_ABCD", "source": 2
        }, separators=(',', ':'))
        sig_reg = hmac.new(API_KEY, payload_reg.encode(), hashlib.sha256).hexdigest()
        
        # Try with a random IP in headers
        headers_reg = {
            "User-Agent": "GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)",
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Connection": "Keep-Alive",
            "Host": "100067.connect.garena.com",
            "X-Garena-Timestamp": str(int(time.time() * 1000)),
            "Authorization": f"Signature {sig_reg}",
            "X-Forwarded-For": "36.69.123.45",
            "X-Real-IP": "36.69.123.45",
            "Client-IP": "36.69.123.45",
        }

        async with session.post(REGISTER_URL, data=payload_reg, headers=headers_reg) as resp:
            print("Status:", resp.status)
            print("Body:", await resp.text())

asyncio.run(test_direct())
