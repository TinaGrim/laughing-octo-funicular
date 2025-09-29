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
mypro = Activity(emulator="emulator-5554", driverID=1)
class test_proxy:
    def proxy(self) -> str:
        return mypro.proxy()

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
