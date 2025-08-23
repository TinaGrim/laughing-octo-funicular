from LD_Player import *
act = Activity("",1)
address = act.proxy()
print(address)
import requests

def test_socks5(proxy_ip, proxy_port, username=None, password=None):
    proxy = f"socks5://{proxy_ip}:{proxy_port}"
    if username and password:
        proxy = f"socks5://{username}:{password}@{proxy_ip}:{proxy_port}"

    proxies = {
        "http": proxy,
        "https": proxy,
    }

    try:
        # Step 1: test connectivity to proxy (fast site)
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
        if r.status_code != 200:
            print(f"[FAIL] Proxy {proxy_ip}:{proxy_port} responded with {r.status_code}")
            return False

        # Step 2: check returned IP (to confirm proxy is used)
        origin_ip = r.json()["origin"]
        print(f"[OK] Proxy works! Reported IP: {origin_ip}:{port}")
        return True

    except requests.exceptions.ConnectTimeout:
        print(f"[FAIL] Proxy {proxy_ip}:{proxy_port} timed out.")
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] Proxy {proxy_ip}:{proxy_port} connection error.")
    except Exception as e:
        print(f"[FAIL] Proxy {proxy_ip}:{proxy_port} error: {e}")

    return False


# Example usage:

ip, port = address.split(":") if address else (None, None)
test_socks5(ip, port)
