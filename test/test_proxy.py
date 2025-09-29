from unicodedata import name
import unittest
from unittest import result
import requests
import threading
import queue
import random
import time
import subprocess
import threading
import os
class Activity(unittest.TestCase):
    def __init__(self):

        self.URL = "http://127.0.0.1:5000/"
        prv_path = os.path.dirname(os.path.abspath(__file__))

        self.PROXY_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\LD_Player\\proxies.txt"
        self.TEST_URL1 = "http://ip-api.com/json"
        self.TEST_URL2 = "https://httpbin.org/ip"
        self.webproxy = ""
        self.TIMEOUT = 5
        self.stop_thread = False
        self.ok = "[ \033[92mOK\033[0m ] "

        
                
    def __check_proxy(self,proxy):
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
        try:
            from_ip_api = requests.get(self.TEST_URL1, proxies=proxies, timeout=self.TIMEOUT)
            if self.stop_thread: return
            from_httpbin = requests.get(self.TEST_URL2, proxies=proxies, timeout=self.TIMEOUT)
            if self.stop_thread: return
            print(self.ok + f"Proxy: {proxy} | IP API: {from_ip_api.status_code} | HTTPBin: {from_httpbin.status_code}")
            if from_httpbin.status_code == 200 and from_ip_api.status_code == 200:
                self.results.put(proxy)
        except Exception:
            pass


    def proxy(self, need: int = 5) -> str:
        self.results = queue.Queue()
        proxies = self.__load_proxies()
        print(self.ok + f"Checking {len(proxies)} proxies using threads...")
        threads = []
        
        for proxy in proxies:

            t = threading.Thread(target=self.__check_proxy, args=(proxy,))
            t.daemon = True
            t.start()
            threads.append(t)

        working = []
        while True:
            try:
                proxy = self.results.get(timeout=0.1)
                working.append((proxy))
                if len(working) >= need:
                    print(self.ok + f"Found {len(working)} working proxies.")
                    self.stop_thread = True
                    
                    proxy = random.choice(working)
                    return proxy if proxy else ""
                    
            except queue.Empty:
                if all(not t.is_alive() for t in threads):
                    print("No working proxy found.")
                    break
                time.sleep(0.05)

        if not working:
            print("proxies NONE")
            return ""
        return ""

        
         
    def __load_proxies(self):
        try:

            with open(self.PROXY_FILE, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []
        
    
class TestSocks5Proxy(unittest.TestCase):
    def test_valid_proxy(self):

        test_class = Activity()
        proxy = test_class.proxy()
        self.assertIsInstance(proxy, str)
        if proxy:
            self.assertIn(":", proxy)
            print("[ \033[92mOK\033[0m ] " + "proxy test passed")
        else:
            self.assertEqual(proxy, "")
            print("[ \033[91mfail\033[0m ] " + "proxy test failed")
if __name__ == "__main__":
    unittest.main()