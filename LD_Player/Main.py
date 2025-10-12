import os
import sys
import time
import requests
import platform
from .Option import option
from selenium.webdriver.common.by import By
from .MyThread import Threader
from .Drivers import LDPlayerRemote
from threading import Thread, Event
class LDPlayer():
    def __init__(self, GUI, ID):
        self.URL = "http://127.0.0.1:5000"
        self.headers = {
            "Content-Type": "application/json",
        }
        self.index = ID - 1
        self.ID = ID
        self.GUI = GUI
        self.opt = option()
        self.resume_event = Event()
        self.resume_event.set()   
        self.running = False   
    
    def open(self):
        self.opt.modify_LD(self.index)
        self.opt.LDPlayer(index=self.index)
    def check_command(self):
        self.opt.wait_for_ldplayer_device(self.ID)
        print("check command done", self.ID)
    
    def remote(self):
        print("Start Remote", self.ID)
        Thread(target=LDPlayerRemote, args=(self,), daemon=True).start()
    
    def stop(self):
        self.running = False
        self.resume_event.clear()
    def resume(self):
        self.running = True
        self.resume_event.set()
    def processing(self):
        pass
    # def run(self, Number: list[int]):
        
    #     if platform.system() == "Windows":
    #         os.system("cls")
    #     else:
    #         sys.exit("Only Windows supported!")

    #     if len(Number) > 10:
    #         print("Limit only 10 LD ;(")
    #         return 0

    #     remainLD = self.get_LD_of(Number)

    #     print("No Action LD: ", remainLD)
    #     requests.post(f"{self.URL}/Order", json=remainLD, headers=self.headers)
        
        
    #     GET = Get(remainLD)
    #     print("Starting...\n")
            
    #     GET.Open_LD()
    #     GET.Full_setup()
    #     GET.Remote_Driver()
        
        
        
        
        

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

    def __repr__(self):
        state = "running" if self.running else "stopped"
        return f"<LDPlayer id={self.ID} state={state}>"
    def __hash__(self):
        return hash((self.ID, self.running))
    def __eq__(self, other):
        if not isinstance(other, LDPlayer):
            return False
        return self.ID == other.ID and self.running == other.running








