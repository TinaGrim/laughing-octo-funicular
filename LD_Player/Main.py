import os
import sys
import time
import requests
import platform
from .Option import option as Get
from selenium.webdriver.common.by import By

class LDPlayer():
    def run(self,Number: list[int]):
        
        if platform.system() == "Windows":
            os.system("cls")
        else:
            sys.exit("Only Windows supported!")
        
        if len(Number) > 10 :
            print("Limit only 10 LD ;(")
            return 0

        r = requests.get("http://127.0.0.1:5000/LDActivity")
        remainLD: list[int] = []
        if r.status_code == 200:
            response = r.json()
            LDActivity = response.get('LDActivity', {})
            print("LDActivity Response: ", LDActivity)

            for number in Number:
                    numkey = f"emulator-55{(number-1)*2+54}"
                    status = LDActivity.get(numkey, {'status': "No Action..."}).get('status')
                    if status == "No Action...":
                        remainLD.append(number)
        else:
            print("Error:", r.status_code)
            sys.exit(1)
            
        print("Remaining LD: ", remainLD)
        requests.post("http://127.0.0.1:5000/openOrder", json=remainLD)
        GET = Get(remainLD)
        print("Starting...\n")
            
        GET.Open_LD()
        GET.Full_setup()
        GET.Remote_Driver()








