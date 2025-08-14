import os
import sys
import time
import platform
from .Option import option as Get
from selenium.webdriver.common.by import By
GET = Get()
class LDPlayer():
    def run(self,Number: list[int]):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            sys.exit("Only Windows supported!")
        
        if len(Number) > 10 :
            print("Limit only 10 LD ;(")
            return 0
        
        print("Starting...\n")

        Get.Open_LD(Number)
        Get.Full_setup(Number)
        Get.Remote_Driver()








