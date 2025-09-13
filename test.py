from unicodedata import name
import unittest
from unittest import result
from LD_Player import *
import requests
import threading
import queue
import random
import time
import subprocess
class test_proxy:
    def __init__(self):
        self.stop_thread = False
        
    def load_proxies(self):
        try:

            with open("LD_Player/proxies.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []

    def check_proxy(self,proxy):
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
        try:
            from_ip_api = requests.get("http://ip-api.com/json", proxies=proxies, timeout=5)
            from_httpbin = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
            if self.stop_thread:
                return
            print("[ \033[92mOK\033[0m ] " + f"Proxy: {proxy} | IP API: {from_ip_api.status_code} | HTTPBin: {from_httpbin.status_code}")
            if from_httpbin.status_code == 200 and from_ip_api.status_code == 200:
                data = from_httpbin.json()
                ip = data.get("origin")
                self.results.put(proxy)
        except Exception:
            pass


    def proxy(self) -> str:

        proxies = []
        self.results = queue.Queue()
        proxies = self.load_proxies()
        print("[ \033[92mOK\033[0m ] " + f"Checking {len(proxies)} proxies using threads...")
        threads = []
        
        for proxy in proxies:

            t = threading.Thread(target=self.check_proxy, args=(proxy,))
            t.daemon = True
            t.start()
            threads.append(t)

        working = []
        while True:
            try:
                proxy = self.results.get(timeout=0.1)
                working.append((proxy))
                if len(working) >= 1:
                    print("[ \033[92mOK\033[0m ]" + f" Found {len(working)} working proxies.")
                    self.stop_thread = True

                    
                    proxy = random.choice(working)
                    return proxy if proxy else ""
                    
            except queue.Empty:
                if all(not t.is_alive() for t in threads):
                    print("No working proxy found.")
                    break
                time.sleep(0.05)

        if not working:
            print("proxies NONE.")
            return ""
        return ""


def test_adb():
    result = subprocess.run(["adb"], capture_output=True, text=True)
    
    return result.stdout

class TestSocks5Proxy(unittest.TestCase):
    def test_valid_proxy(self):

        test_class = test_proxy()
        proxy = test_class.proxy()
        self.assertIsInstance(proxy, str)
        if proxy:
            self.assertIn(":", proxy)
            print("[ \033[92mOK\033[0m ] " + "proxy test passed")
        else:
            self.assertEqual(proxy, "")
            print("[ \033[91mfail\033[0m ] " + "proxy test failed")
            
class TestADBCommand(unittest.TestCase):      
    def test_adb(self):
        adb = test_adb()
        self.assertIsInstance(adb, str)

        if adb:
            self.assertIn("Android", adb)
            print("[ \033[92mOK\033[0m ] " + "adb test passed")
        else:
            self.assertEqual(adb, "")
            print("[ \033[91mfail\033[0m ] " + "adb test failed")

if __name__ == "__main__":
    unittest.main()
