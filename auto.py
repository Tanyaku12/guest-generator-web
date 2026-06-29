import os
import random
import subprocess
import sys
import time

# Konfigurasi
PROXY_FILE = "proxy.txt"
TARGET_SCRIPT = "app.py"

def load_proxies():
    """Membaca daftar proxy dari file."""
    if not os.path.exists(PROXY_FILE):
        print(f"Error: File {PROXY_FILE} tidak ditemukan!")
        print("Silakan buat file proxy.txt dan masukkan daftar proxy Anda di sana.")
        return []
    
    with open(PROXY_FILE, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

def get_random_proxy(proxies):
    """Memilih satu proxy secara acak."""
    return random.choice(proxies) if proxies else None

def run_with_proxy(proxy):
    """Menjalankan skrip target dengan proxy yang dipilih."""
    print(f"[*] Menjalankan {TARGET_SCRIPT} menggunakan proxy: {proxy}")
    
    # Menyiapkan environment variable untuk proxy
    # Mendukung format: ip:port atau user:pass@ip:port
    env = os.environ.copy()
    env["http_proxy"] = f"http://{proxy}"
    env["https_proxy"] = f"http://{proxy}"
    
    try:
        # Menjalankan skrip asli
        process = subprocess.Popen([sys.executable, TARGET_SCRIPT], env=env)
        process.wait()
    except KeyboardInterrupt:
        print("\n[!] Dihentikan oleh pengguna.")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Terjadi kesalahan: {e}")

def main():
    print("========================================")
    print("   AUTOPROXY LAUNCHER for app.py")
    print("========================================")
    
    proxies = load_proxies()
    if not proxies:
        print("[!] Tidak ada proxy yang bisa digunakan.")
        return

    while True:
        proxy = get_random_proxy(proxies)
        run_with_proxy(proxy)
        
        # Jeda sebelum rotasi berikutnya (jika skrip gen.py selesai berjalan)
        print("[*] Skrip selesai. Mengganti proxy dalam 5 detik...")
        time.sleep(5)

if __name__ == "__main__":
    main()
