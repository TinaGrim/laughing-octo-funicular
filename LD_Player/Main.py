import time
from selenium.webdriver.common.by import By
import os
from .Option import option as Get
import sys
import platform
class LDPlayer():
    def run(self,number:int):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            sys.exit("Only Windows supported!")
            
        Number = number
        if Number > 10 :
            print("Limit only 10 LD ;(")
            return 0
        

        print("Starting...\n")

        Get().Open_LD(Number)
        Get().Full_setup(Number)
        Get().Remote_Driver(Number)







