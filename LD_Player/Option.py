import os
import sys
import time
import email
import queue
import names
import dotenv
import string
import random 
import imaplib
import requests
import platform
import platform
import traceback
import threading
import subprocess
import pygetwindow
from typing import Optional
from appium import webdriver
from email.header import decode_header
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver





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
    def __init__(self, Number: Optional[list[int]] = []):
        self.SELECTOR = {
        "Messenger": """//android.widget.TextView[@content-desc="Messenger"]""",
        "cancelAuth": """//android.widget.ImageView[@content-desc="Cancel"]""",
        "createAccount": """//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup""",
        "getStarted2": """//android.view.View[@content-desc="Get started"]""",
        "getStarted": """//android.view.View[@content-desc="Create new account"]""",
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
        "day": self.__Random_Day(),
        "year": self.__Random_Year(),
        "month": self.__Random_Month(),
        "gender": self.__Random_Gender(),
        "emailRan": self.__Get_Temp_Mail(),
        "lastName":self.__Random_last_Name(),
        "firstName":self.__Random_first_Name()
        }
        self.number = Number
        self.URL = "http://127.0.0.1:5000/"
        

    @timer
    def __Open_Appium(self, port):
        """Opening Cmd of Appium"""
        
        subprocess.Popen(f'start /MIN cmd /c appium --port {port}', shell=True, startupinfo=self.__info(2))
        time.sleep(0.5)

    @timer
    def __LDPlayer(self, startupinfo, index):
        """Opening LDPlayer by cmd"""
        SUP = self.__info(1)
        
        try:
            LDPlayer_launcher_path = f'"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" launch --index {index}'
            LDPlayer_setup_path = f'"D:\\LDPlayer\\LDPlayer9\\ldconsole.exe" modify --index {index} --resolution 300,600,160 --cpu 2 --memory 2048'
            
            subprocess.run(LDPlayer_setup_path, shell=True, startupinfo=SUP) 
            subprocess.Popen(LDPlayer_launcher_path, shell=True, startupinfo=SUP)
        except Exception as e:
            traceback.print_exc()
            print(f"Error launching LDPlayer: {e}")
            return
        time.sleep(0.5)

        self.__Arrangment(index)

    def check_ld_in_list(self)->list[str]:
        
        try:
            path = "D:\\LDPlayer\\LDPlayer9\\ldconsole.exe list"
            self.ld_list_name = subprocess.run(path, shell = True,stdout=subprocess.PIPE, text=True)

        except:
            print("Error locating LD Folder")
            return []
        self.ld_list_name = (self.ld_list_name.stdout.split("\n"))
        self.ld_list_name.pop()
        return self.ld_list_name #Sample [LDPlayer-1, LDPlayer-2]
    
    def LD_devieces_detail(self, FIND) -> list[str]:
        
        try:
            Datas = []
            for i in range(0, 5):
                with open(f"D:\\LDPlayer\\LDPlayer9\\vms\\config\\leidian{i}.config") as f:
                    lines = f.readlines()
                    for line in lines:
                        if FIND in line:
                            Data = line.split('"')[3].strip()
                            Datas.append(Data)
            return Datas # Sample Love You 
        except FileNotFoundError:
            print("LDPlayer config file not found.")
            return []

    def __Arrangment(self, index: int) -> None:
        """Arranging LDPlayer windows"""
        try:
            LD_Name = f"LDPlayer" if index == 0 else f"LDPlayer-{index}"
            found = False
            while not found:
                for w in pygetwindow.getAllWindows():
                    if w.title == LD_Name:
                        w.moveTo(index * 300,0)
                        print(f"LDPlayer {index + 1} Arranged successfully")
                        found = True
                        break
                time.sleep(1)
                
        except Exception as e:
            print(f"Error moving window: {e}")

    def cap(self,port: int,choose: int)-> WebDriver:
        try:
            desired_caps = self.__get_des_cap(choose)
            options = UiAutomator2Options()
            for k, v in desired_caps.items():
                options.set_capability(k, v)

            self.__Open_Appium(port=port)
            self.driver = WebDriver(f"http://localhost:{port}", options=options) 
        except Exception as e:
            print(f"Error initializing Appium driver: {e}")
            traceback.print_exc()

        return self.driver #Sample [webdriver.Remote]

    def __get_des_cap(self, ID: int) -> dict[str,str]:
        
        des_cap = {
            "automationName": "UiAutomator2",
            "platformName": "Android",
            "platformVersion": "9",
            "deviceName": f"emulator-55{(ID-1)*2 + 54}",
            "udid" : f"emulator-55{(ID-1)*2 + 54}",
            "noReset": True
        }
        return des_cap

    def __info(self, Show: int)->subprocess.STARTUPINFO:
        """Just for hide window - Windows only"""
        if platform.system() == "Windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = Show
            return startupinfo
        else:
            # currently only support Windows
            sys.exit(1)
    
    def wait_for_ldplayer_device(self, device_name: str, timeout=60):
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

    def Open_LD(self):
        
        if not self.number:
            return
        for i in self.number:
            self.__LDPlayer(self.__info(1), index=i-1) # Sample Open Your LDName

    def Remote_Driver(self) -> None:
        """Start Remote Driver"""   
        Driver_path = os.path.abspath(__file__)
        Driver_path = os.path.dirname(Driver_path) + f"\\Drivers.py"
        print("Remote Driver Path: ", Driver_path)
        subprocess.Popen(["python",Driver_path]) # Sample Remote using Driver in Path That Exists

    def Full_setup(self):
        if not self.number:
            return
        for i in self.number:

            device_name = f"emulator-55{((i-1)*2+54)}"
            
            openLD = self.wait_for_ldplayer_device(device_name)# Sample running test shell CMD in LD
            if openLD:
                self.__clear_app_data(device_name)# Sample Wait Full setup  and clear it up

    def GetCode(self, username: str, password: str, email):
        imap_server = "imap.yandex.ru"
        port = 993
        try:
            mail = imaplib.IMAP4_SSL(imap_server, port)
            mail.login(username, password)
            mail.select("INBOX")

            status, messages = mail.search(None, 'ALL')
            email_ids = messages[0].split()
            found_match = False
            latest_email_id = email_ids[-1]
            if not email_ids:
                print("No emails found.")
            else:
                status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        to_ = msg.get("To", "")

                        recipients = f"{to_}".replace(" ", "").lower()
                        if email.lower() in recipients and "is your" in subject:
                            return subject.split(' ')[0]
                            found_match = True
            if not found_match:
                print(f"No emails found with {email} in any recipient field.")

            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Error: {e}")


    # username = "tinagrim@yandex.com"
    # password = "frshsghyvjqeiayv"  # Use app password if 2FA is enabled
    # filter_email = "tinagrim+001kh@yandex.com"

    def opened_drivers(self)-> list[str]:

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
            if "emulator" in line:
                driver_name: str = line.split("\t")[0]
                Drivers_list_opened.append(driver_name)

        return Drivers_list_opened # sample [emulator-5554, emulator-5556] is open

    def __Random_first_Name(self)-> str:
        NAME = names.get_first_name()
        return NAME
    def __Random_last_Name(self)-> str:
        NAME = names.get_last_name()
        return NAME
    def __Random_Gender(self)-> str:
        GENDER = ["Female","Male"]
        Gender = random.choice(GENDER)
        return Gender
    
    def __Get_Temp_Mail(self):

        Mail = "tinagrim+"+ ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6)) + "@yandex.com"
        return Mail

    def __Random_Year(self)-> int:
        YEAR = random.randint(2000, 2005)
        return YEAR

    def __Random_Day(self)-> int:
        Day = random.randint(15,30)
        return Day
    def __Random_Month(self)-> str:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        MONTH = random.choice(months)
        return MONTH
    
    def __clear_app_data(self, device_name, package_name = "com.facebook.orca")-> None:
        Clear = subprocess.run(["adb", "-s", device_name, "shell", "pm", "clear", package_name])
        print("Clear out: ",Clear)
class Activity:
    def __init__(self, emulator:str, driverID: int):
        self.emulator = emulator
        self.driverID = driverID
        self.URL = "http://127.0.0.1:5000/"
        prv_path = os.path.dirname(os.path.abspath(__file__))
        dotenv.load_dotenv(dotenv_path=os.path.join(prv_path, "..", ".env"))
        self.token = {
            1: os.getenv("TOKEN1"),
            2: os.getenv("TOKEN2"),
            3: os.getenv("TOKEN3"),
            4: os.getenv("TOKEN4"),
            5: os.getenv("TOKEN5"),
            6: os.getenv("TOKEN6"),
            7: os.getenv("TOKEN7"),
        }
        self.PROXY_FILE = "proxies.txt"
        self.TEST_URL = "http://ip-api.com/json"
        self.TIMEOUT = 5
        self.proxy = self.__proxy()


    def setActivity(self, status):
        body = {
            self.emulator: {
                "id": self.driverID,
                "status": status
            }
        }
        requests.post(self.URL + "LDActivity", json=body)
        
    def KillAppium(self, port: int, ID:int) -> None:
        
        try:
        
            r = requests.get(self.URL + "schedule")
            close_appium_response = r.json().get("scheduleClose",True) 

        except Exception as e:
            print(f"Server Can Not Get Schedule status: {e}")
            
        find_pid_cmd = f'netstat -aon | findstr :{port}'
        line = []
        try:
            result = subprocess.check_output(find_pid_cmd, shell=True, text=True)
            line = result.strip().splitlines()
            
        except subprocess.CalledProcessError:
            print("Port Cleared")
        except Exception as e:
            print(f"Unexpected error: {e}")

        
        if close_appium_response:
            if line:
                pid = line[0].split()[-1]
                kill_cmd = f'taskkill /PID {pid} /F'
                subprocess.run(kill_cmd, shell=True)
                print("Kill Appium server: ", ID)
                
    def __check_proxy(self,proxy):

        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
        try:
            response = requests.get(self.TEST_URL, proxies=proxies, timeout=self.TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                self.results.put((proxy, True, data.get("query"), data.get("country")))
        except Exception:
            pass


    def __proxy(self):
        proxies = []
        self.results = queue.Queue()
        proxies = self.__load_proxies()
        print(f"Checking {len(proxies)} proxies using threads...")
        threads = []
        
        for proxy in proxies:

            t = threading.Thread(target=self.__check_proxy, args=(proxy,))
            t.daemon = True
            t.start()
            threads.append(t)

        while True:
            try:
                proxy, _, ip, country = self.results.get(timeout=0.1)
                proxies.append(proxy)
                

            except queue.Empty:

                if all(not t.is_alive() for t in threads):
                    print("No working proxy found.")
                    break
                time.sleep(0.05)
            proxy = proxies[random.randint(0, len(proxies)-1)]
            ip, port = proxy.split(":")
            return ip, port

    def __load_proxies(self):
        try:
            with open(self.PROXY_FILE, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []
