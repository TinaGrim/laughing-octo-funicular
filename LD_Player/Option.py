import time

from appium import webdriver
import subprocess
from appium.options.android.uiautomator2.base import UiAutomator2Options
import random 
import requests
import os
import pygetwindow as gw


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_get = end - start
        time_get = round(time_get, 1) 
        time_get =  f"Open {func.__name__} Time : {time_get-1} seconde"
        print(time_get)
        return result
    return wrapper
        
class option:
    def __init__(self):
        self.drivers = []
    @timer
    def Open_Appium(self, port):
        """Opening Cmd of Appium"""
        startupinfo = self.info(2)
        
        subprocess.Popen(f'start /MIN cmd /c appium --port {port}', shell=True, startupinfo=startupinfo)

        time.sleep(1)
        
    @timer
    def LDPlayer(self, startupinfo, index):
        """Opening LDPlayer by cmd"""
        import platform
        startupinfo = self.info(1)
        
        system = platform.system()
        
        if system == "Windows":

            LDPlayer_launcher_path = f'"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" launch --index {index}'
            LDPlayer_setup_path = f'"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" modify --index {index} --resolution 300,600,160 '
            print("LDPlayer count:", index + 1)
            
            LD_Name = f"LDPlayer" if index == 0 else f"LDPlayer-{index}"
            
            subprocess.run(LDPlayer_setup_path, shell=True, startupinfo=startupinfo) 
            subprocess.run(LDPlayer_launcher_path, shell=True, startupinfo=startupinfo)
        else:
            print("Not supported for this OS")
        time.sleep(1)

        try:
            
            for w in gw.getAllWindows():
                if w.title == LD_Name:
                    w.moveTo(index * 215,0)
                    break
                print(f"LDPlayer {index + 1} Arranged successfully")
            else:
                print(f"LDPlayer {index + 1} launched (window positioning unavailable in headless mode)")
        except Exception as e:
            print(f"Error moving window: {e}")

    def cap(self,port,choose):
        
        desired_caps = self.get_des_cap(choose)
        options = UiAutomator2Options()
        
        
        for k, v in desired_caps.items():
            options.set_capability(k, v)
            
        self.Open_Appium(port=port)
        self.driver = webdriver.Remote(f"http://localhost:{port}", options=options) # type: ignore

        return self.driver

    def get_des_cap(self, ID):
        ID = (ID-1)*2 + 54
        des_cap = {
            "automationName": "UiAutomator2",
            "platformName": "Android",
            "platformVersion": "9",
            "deviceName": f"emulator-55{ID}",
            "udid" : f"emulator-55{ID}",
            "noReset": True
        }
        return des_cap 
    
    def info(self, Show):
        """Just for hide window - Windows only"""
        import platform
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = Show
            return startupinfo
        else:
            # On macOS/Linux, return None since STARTUPINFO doesn't exist
            return None
    
    def wait_for_ldplayer_device(self, device_name, timeout=60):
        """check if LDPlayer fully opened"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                result = subprocess.run(
                    ['adb', 'devices'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            except Exception as e:
                print(f"Error running adb.exe: {e}")
                return False
            
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
                        self.drivers.append(device_name)
                        
            

            
        print(f"Timeout: {device_name} did not appear in adb devices.")
        return False
    
    def Open_LD(self, Number):
            startupinfo = self.info(1)
            for i in range(0, Number):
                self.LDPlayer(startupinfo, index = i)
                
    def Remote_Driver(self,Number):
        for i in range(1, Number +1):
            
            Driver_path = os.path.abspath(__file__)
            Driver_path = os.path.dirname(Driver_path) + f"\\Driver{i}.py"
            print("Remote Driver Path: ", Driver_path)
            subprocess.Popen(["python",Driver_path])
    
    def Full_setup(self,Number):
        
        for i in range(0, Number):
            #Get().Open_LDPlayer(startupinfo, index = i)
            device_name = f"emulator-555{(i*2)+4}"

            self.name = self.wait_for_ldplayer_device(device_name)
            self.__clear_app_data(device_name)
            
    def opened_drivers(self):
        """Get all opened drivers"""
        return self.drivers
    
    def Random_Name(self):
        NAME = ["Tina","Roth", "Thida","Jonh" , "Nher"]
        Name = random.choice(NAME)
        return Name
    
    def Random_Gender(self):
        GENDER = ["Female","Male"]
        Gender = random.choice(GENDER)
        return Gender
    
    def Get_Temp_Mail(self):

        Mail = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = Mail.json()[0]
        return email
    
    def Random_Year(self):
        YEAR = random.randint(2000, 2005)
        return YEAR
    def Random_Day(self):
        Day = random.randint(15,30)
        return Day
    def Random_Month(self):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        MONTH = random.choice(months)
        return MONTH
    
    def __clear_app_data(self, device_name, package_name = "com.facebook.orca"):
        Clear = subprocess.run(["adb", "-s", device_name, "shell", "pm", "clear", package_name])
        print("Clear out: ",Clear)
