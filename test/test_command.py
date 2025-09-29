from unicodedata import name
import unittest
from unittest import result
import requests
import threading
import queue
import random
import time
import subprocess


def test_adb():
    result = subprocess.run(["adb"], capture_output=True, text=True)
    
    return result.stdout


            
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
