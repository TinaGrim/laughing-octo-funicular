import time
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from selenium.webdriver.common.by import By
import subprocess
import os
from Option import option as Get #type: ignore

#from Drives 
class LDPlayer():
    
    def run(self,number):
        Number = number #input("LDPlayer Count: ")
        if Number > 10 :
            print("Limit only 10 LD ;(")
            return 0
        
        os.system("cls")
        print("Starting...\n")

        Get().Open_LD(Number)
        Get().Full_setup(Number)
        Get().Remote_Driver(Number)





# if __name__ == "__main__":
#     ld = LDPlayer()
#     ld.run()

