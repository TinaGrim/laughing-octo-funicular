import os
import sys
import time
import requests
import platform
from .Option import option as Get
from selenium.webdriver.common.by import By

class LDPlayer():
    def __init__(self):
        self.URL = "http://127.0.0.1:5000"
        self.headers = {
            "Content-Type": "application/json",
        }
        
    def run(self, Number: list[int]):
        
        if platform.system() == "Windows":
            os.system("cls")
        else:
            sys.exit("Only Windows supported!")

        if len(Number) > 10:
            print("Limit only 10 LD ;(")
            return 0

        remainLD = self.get_LD_of(Number)

        print("No Action LD: ", remainLD)
        requests.post(f"{self.URL}/Order", json=remainLD, headers=self.headers)
        
        
        GET = Get(remainLD)
        print("Starting...\n")
            
        GET.Open_LD()
        GET.Full_setup()
        GET.Remote_Driver()

    def get_LD_of(self, Number):
        response = requests.get(f"{self.URL}/LDActivity", headers=self.headers)

        remainLD: list[int] = []
        
        if response.status_code == 200:
            response = response.json()
            LDActivity = response.get('LDActivity', {})
            print("LDActivity Response: ", LDActivity)

            for number in Number:
                    numkey = f"emulator-55{(number-1)*2+54}"
                    status = LDActivity.get(numkey, {'status': "No Action..."}).get('status')
                    if status == "No Action...":
                        remainLD.append(number)# sample [1, 2, 3]
        else:
            print("Error:", response.status_code)
            sys.exit(1)
        return remainLD









