import os
import sys
import time
import email
import queue
import names
import dotenv
import string
import random 
import signal
import imaplib
import requests
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
        time_get =  "[ \033[92mOK\033[0m ] " + f"Open {func.__name__} Time : {time_get} seconde"
        print(time_get)
        return result
    return wrapper
        
class option:
    def __init__(self, Number: Optional[list[int]] = []):
        self.SELECTOR = {
        "Proxy": """//android.widget.TextView[@content-desc="Super Proxy"]""",
        "addProxy": """//android.widget.Button[@content-desc="Add proxy"]""",
        "server": """//android.widget.ScrollView/android.widget.EditText[3]""",
        "port": """//android.widget.ScrollView/android.widget.EditText[4]""",
        "save": """//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.widget.Button[2]""",
        "startProxy": """//android.widget.Button[@content-desc="Start"]""",
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
        self.DIR_LD = "D:\\LDPlayer\\LDPlayer9"
        self.ok = "[ \033[92mOK\033[0m ] "
        

    @timer
    def __Open_Appium(self, port):
        """Opening Cmd of Appium"""
        
        subprocess.Popen(f'start /MIN cmd /c appium --log-level debug --relaxed-security --port {port}', shell=True, startupinfo=self.__info(2))
        time.sleep(0.5)

    @timer
    def __LDPlayer(self, startupinfo, index):
        """Opening LDPlayer by cmd"""
        SUP = self.__info(1)
        
        try:
            LDPlayer_launcher_path = f'"{self.DIR_LD}\\ldconsole.exe" launch --index {index}'
            LDPlayer_setup_path = f'"{self.DIR_LD}\\ldconsole.exe" modify --index {index} --resolution 300,600,160 --cpu 2 --memory 2048'

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
            path = f"{self.DIR_LD}\\ldconsole.exe list"
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
                with open(f"{self.DIR_LD}\\vms\\config\\leidian{i}.config") as f:
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
                        print(self.ok + f"LDPlayer {index + 1} Arranged successfully")
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
            "showLogcat": True,

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
                        print(self.ok + f"{device_name} is fully ready.")
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
        print(self.ok + f"Remote Driver Path: ", Driver_path)
        subprocess.Popen(["python",Driver_path]) # Sample Remote using Driver in Path That Exists

    def Full_setup(self):
        if not self.number:
            return
        for i in self.number:

            device_name = f"emulator-55{((i-1)*2+54)}"
            
            openLD = self.wait_for_ldplayer_device(device_name)# Sample running test shell CMD in LD
            if openLD:
                self.clear_app_data(device_name, "com.scheler.superproxy")# Sample Wait Full setup and clear it up
                time.sleep(2)
            else:
                print(f"Error: {device_name} not found in adb devices.")
                continue
                # self.clear_app_data(device_name,"com.facebook.orca")# Sample Wait Full setup  and clear it up
    # Not Mine
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

    def current_ld(self)-> list[str]:

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

    def clear_app_data(self, device_name: str, package_name: str) -> None:
        Clear = subprocess.run(["adb", "-s", device_name, "shell", "pm", "clear", package_name])
        print(self.ok + "Clear out: ",Clear)
        
        
    def KillAppium(self, port: int, ID:int) -> None:
        
        try:
        
            r = requests.get(self.URL + "schedule")
            close_appium_response = r.json().get("scheduleClose",True) 

        except Exception as e:
            print(f"Can not kill appium: {e}")
            
        find_pid_cmd = f'netstat -aon | findstr :{port}'
        line = []

        try:
            result = subprocess.check_output(find_pid_cmd, shell=True, text=True)
            line = result.strip().splitlines()
            
        except subprocess.CalledProcessError:
            print(self.ok + "Port Cleared")
        except Exception as e:
            print(f"Unexpected error: {e}")

        
        if close_appium_response:
            if line:
                pid = line[0].split()[-1]

                os.kill(int(pid), signal.SIGTERM)
                print("[ \033[92mOK\033[0m ] " + "Kill Appium server: ", ID)
                
                
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
        self.PROXY_FILE = os.path.dirname(os.path.abspath(__file__)) + "\\proxies.txt"
        self.TEST_URL1 = "http://ip-api.com/json"
        self.TEST_URL2 = "https://httpbin.org/ip"
        self.webproxy = ""
        self.TIMEOUT = 5
        self.stop_thread = False
        self.ok = "[ \033[92mOK\033[0m ] "



    def setActivity(self, status):
        body = {
            self.emulator: {
                "id": self.driverID,
                "status": status
            }
        }
        requests.post(self.URL + "LDActivity", json=body)
        
                
    def __check_proxy(self,proxy):
        proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
        try:
            from_ip_api = requests.get(self.TEST_URL1, proxies=proxies, timeout=self.TIMEOUT)
            from_httpbin = requests.get(self.TEST_URL2, proxies=proxies, timeout=self.TIMEOUT)
            if self.stop_thread:
                return
            print(self.ok + f"Proxy: {proxy} | IP API: {from_ip_api.status_code} | HTTPBin: {from_httpbin.status_code}")
            if from_httpbin.status_code == 200 and from_ip_api.status_code == 200:
                data = from_httpbin.json()
                ip = data.get("origin")
                self.results.put(proxy)
        except Exception:
            pass


    def proxy(self) -> str:
        proxies = []
        self.results = queue.Queue()
        proxies = self.__load_proxies()
        print(self.ok + f"Checking {len(proxies)} proxies using threads...")
        threads = []
        
        for proxy in proxies:

            t = threading.Thread(target=self.__check_proxy, args=(proxy,))
            t.daemon = True
            t.start()
            threads.append(t)

        working = []
        while True:
            try:
                proxy = self.results.get(timeout=0.1)
                working.append((proxy))
                if len(working) >= 2:
                    print(self.ok + f"Found {len(working)} working proxies.")
                    self.stop_thread = True
                    
                    proxy = random.choice(working)
                    return proxy if proxy else ""
                    
            except queue.Empty:
                if all(not t.is_alive() for t in threads):
                    print("No working proxy found.")
                    break
                time.sleep(0.05)

        if not working:
            print("proxies NONE.")
            return ""
        return ""

        
         
    def __load_proxies(self):
        try:

            with open(self.PROXY_FILE, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []
