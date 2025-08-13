import platform
import time
import sys
import platform
from appium import webdriver
import subprocess
from appium.options.android.uiautomator2.base import UiAutomator2Options
import random 
import requests
import os
import pygetwindow as gw
import names
import traceback
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_get = end - start
        time_get = round(time_get, 1) 
        time_get =  f"Open {func.__name__} Time : {time_get} seconde"
        print(time_get)
        return result
    return wrapper
        
class option:
    def __init__(self):
        self.SELECTOR = {
        "Messenger": """//android.widget.TextView[@content-desc="Messenger"]""",
        "cancelAuth": """//android.widget.ImageView[@content-desc="Cancel"]""",
        "createAccount": """//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup""",
        "getStarted": """//android.view.View[@content-desc="Get started"]""",
        "getStarted2": """//android.view.View[@content-desc="Create new account"]""",
        "permissionDeny": """//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]""",
        "startAfterDeny": """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText""",
        "firstNameWidget": """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.EditText""",
        "lastNameWidget": """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.EditText""",
        "afterNameFill": """//android.view.View[@content-desc="Next"]""",
        "setDate": """//android.widget.Button[@resource-id="android:id/button1"]""",
        "afterDate": """//android.view.View[@content-desc="Next"]""",
        "afterGender": """//android.view.View[@content-desc="Next"]""",
        "signUpEmail": """//android.view.View[@content-desc="Sign up with email"]""",
        "emailWidget": """//android.widget.EditText""",
        "confirmEmail": """//android.view.View[@content-desc="Next"]"""
        }
        self.IMFORMATION = {
        "firstName":self.Random_first_Name(),
        "lastName":self.Random_last_Name(),
        "month": self.Random_Month(),
        "day": self.Random_Day(),
        "year": self.Random_Year(),
        "gender": self.Random_Gender(),
        "email": "Not_Used@email.com"
        }
        
    @timer
    def Open_Appium(self, port):
        """Opening Cmd of Appium"""
        startupinfo = self.info(2)
        subprocess.Popen(f'start /MIN cmd /c appium --port {port}', shell=True, startupinfo=startupinfo)
        time.sleep(1)
        
    @timer
    def LDPlayer(self, startupinfo, index):
        """Opening LDPlayer by cmd"""
        startupinfo = self.info(1)
        
        try:
            LDPlayer_launcher_path = f'"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" launch --index {index}'
            LDPlayer_setup_path = f'"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" modify --index {index} --resolution 300,600,160 '
            print("LDPlayer count:", index + 1)
            
            subprocess.run(LDPlayer_setup_path, shell=True, startupinfo=startupinfo) 
            subprocess.Popen(LDPlayer_launcher_path, shell=True, startupinfo=startupinfo)
        except Exception as e:
            traceback.print_exc()
            print(f"Error launching LDPlayer: {e}")
            return
        time.sleep(1)
        
        self.Arrangment(index)

    def check_ld_in_list(self)->list[str]:
        try:
            path = "D:\\LDPlayer\\LDPlayer9\\ldconsole.exe list"
            self.ld_list_name = subprocess.run(path, shell = True,stdout=subprocess.PIPE, text=True)

        except:
            print("Error locating LD Folder")
            return []
        self.ld_list_name = (self.ld_list_name.stdout.split("\n"))
        self.ld_list_name.pop()
        return self.ld_list_name
    
    def Arrangment(self, index) -> None:
        """Arranging LDPlayer windows"""
        try:
            LD_Name = f"LDPlayer" if index == 0 else f"LDPlayer-{index}"
            found = False
            while not found:
                for w in gw.getAllWindows():
                    if w.title == LD_Name:
                        w.moveTo(index * 250,0)
                        print(f"LDPlayer {index + 1} Arranged successfully")
                        found = True
                        break
                time.sleep(1)
        except Exception as e:
            print(f"Error moving window: {e}")

    def cap(self,port,choose)->webdriver.Remote:#type: ignore
        try:
            desired_caps = self.get_des_cap(choose)
            options = UiAutomator2Options()
            for k, v in desired_caps.items():
                options.set_capability(k, v)
                
            self.Open_Appium(port=port)
            self.driver = webdriver.Remote(f"http://localhost:{port}", options=options) # type: ignore
        except Exception as e:
            print(f"Error initializing Appium driver: {e}")
            traceback.print_exc()
            
        return self.driver

    def get_des_cap(self, ID) -> dict:
        
        des_cap = {
            "automationName": "UiAutomator2",
            "platformName": "Android",
            "platformVersion": "9",
            "deviceName": f"emulator-55{(ID-1)*2 + 54}",
            "udid" : f"emulator-55{(ID-1)*2 + 54}",
            "noReset": True
        }
        return des_cap

    def info(self, Show) -> subprocess.STARTUPINFO:
        """Just for hide window - Windows only"""
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = Show
            return startupinfo
        else:
            # currently only support Windows
            sys.exit(1)
    
    def wait_for_ldplayer_device(self, device_name, timeout=60):
        """check if LDPlayer fully opened"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check if command is available
            try:
                result = subprocess.run(
                    ['adb', 'devices'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            except Exception as e:
                print(f"Error running adb.exe: {e}")
            
            # debugging
            for line in result.stdout.splitlines():
                if device_name in line and "\tdevice" in line:
                    
                    shell_result = subprocess.run(
                        ["adb", "-s", device_name, "shell", "echo", "ok"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if shell_result.returncode == 0 and "ok" in shell_result.stdout:
                        print(f"{device_name} is fully ready.")
                        return True
        print(f"Timeout: {device_name} did not appear in adb devices.")
        return False

    def Open_LD(self, Number: list[int]):
        startupinfo = self.info(1)
        for i in Number:
            self.LDPlayer(startupinfo, index=i-1)

    def Remote_Driver(self) -> None:
        """Start Remote Driver"""   
        Driver_path = os.path.abspath(__file__)
        Driver_path = os.path.dirname(Driver_path) + f"\\Drivers.py"
        print("Remote Driver Path: ", Driver_path)
        subprocess.Popen(["python",Driver_path])
    
    def Full_setup(self,Number):
        for i in Number:

            device_name = f"emulator-55{((i-1)*2+54)}"
            
            openLD = self.name = self.wait_for_ldplayer_device(device_name)
            if openLD:
                self.__clear_app_data(device_name)

    def opened_drivers(self)-> list[str]:
        Drivers_list = [f"emulator-55{(i-1)*2+54}" for i in range(1, 21)]
        Drivers_list_opened = []
        
        try:
            result = subprocess.run(
                ['adb', 'devices'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            print(f"not found adb.exe: {e}")
            return Drivers_list_opened
            
        """Activity Check"""
        for line in result.stdout.splitlines():
            for driver_name in Drivers_list:
                if driver_name in line:
                    Drivers_list_opened.append(driver_name)
        return Drivers_list_opened

    def Random_first_Name(self)-> str:
        NAME = names.get_first_name()
        return NAME
    def Random_last_Name(self)-> str:
        NAME = names.get_last_name()
        return NAME
    def Random_Gender(self)-> str:
        GENDER = ["Female","Male"]
        Gender = random.choice(GENDER)
        return Gender
    
    def Get_Temp_Mail(self):

        Mail = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = Mail.json()[0]
        return email
    
    def Random_Year(self)-> int:
        YEAR = random.randint(2000, 2005)
        return YEAR

    def Random_Day(self)-> int:
        Day = random.randint(15,30)
        return Day
    def Random_Month(self)-> str:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        MONTH = random.choice(months)
        return MONTH
    
    def __clear_app_data(self, device_name, package_name = "com.facebook.orca")-> None:
        Clear = subprocess.run(["adb", "-s", device_name, "shell", "pm", "clear", package_name])
        print("Clear out: ",Clear)
