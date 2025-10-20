
import os
import re
import sys
import time
import requests
import threading
import subprocess
from datetime import datetime 
try:
    from .Option import option, Activity
except ImportError:
    from LD_Player.Option import option, Activity
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import  NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
class LDPlayerRemote():
    def __init__(self, LDPlayer):

        self.GET = option()
        self.LDPlayer = LDPlayer
        self.driverID = LDPlayer.ID
        self.port = 4722 + self.driverID
        self.SELECTOR = self.GET.SELECTOR
        self.IMFORMATION = self.GET.IMFORMATION
        self.emu = f"emulator-55{(self.driverID-1)*2+54}"
        self.activity = Activity(self.emu, self.driverID)
        self.Driver = self.GET.cap(self.port, self.driverID)
        print(self.port, self.driverID)
        self.pause = False
        if self.Driver is None:
            print("Driver did not exist...")
            return 0
        
        time.sleep(2)
        # self.safe_run(self.ProxyConnect)
        self.safe_run(self.driverRun)

    def safe_run(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except (InvalidSessionIdException, MaxRetryError, ConnectionError) as e:
            print("[ \033[91mClose\033[0m ] " + "Closing Appium server During Remote Driver => ", str(e))
            self.action("No Action...")
            sys.exit(1)
        except NoSuchElementException as e:
            print(str(func))
            
            print("[ \033[91mClose\033[0m ] " + "Found no element => " + str(e))
            self.action("No Action...")
            sys.exit(1)
        except TimeoutException as e:
            print(str(func))
            
            print(f"[ \033[91mClose\033[0m ] " + "Time out => " + str(e))
            self.action("No Action...")
            sys.exit(1)
        except WebDriverException as e:
            print(f"[ \033[91mClose\033[0m ] " + "Server get error => " + str(e))
            self.action("No Action...")
            sys.exit(1)
            
    def is_pause(self):
        if hasattr(self.LDPlayer, 'resume_event'):
            self.LDPlayer.resume_event.wait()
    def wait_and_click_to(self, xpath, timesleep=3, timeout:float=30):
        self.is_pause()
            
        time.sleep(timesleep)
        el = WebDriverWait(self.Driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        el.click()
        return el
    
    def check_element(self, xpath, timesleep=0.5, timeout:float=3):
        self.is_pause()
        time.sleep(timesleep)
        try:
            WebDriverWait(self.Driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except (NoSuchElementException, TimeoutException):
            return False
        return True
    
    def wait_and_send_keys_to(self, xpath, text, timesleep=3, timeout: float=30):
        self.is_pause()
        time.sleep(timesleep)
        el = WebDriverWait(self.Driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        el.click()
        el.clear()
        el.send_keys(text)
        return el

    def action(self, label, func = None, *args, **kwargs):
        try:
            if not func:
                self.activity.setActivity(label)
                return
            self.activity.setActivity(label)
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ \033[91mERROR\033[0m ] {label}: {e}")
            return None
        
    def ProxyConnect(self):

            if self.Driver is None:
                print("Driver did not exist...")
                return 0
            self.Driver.press_keycode(3)

            self.GET.clear_app_data(self.emu, "com.scheler.superproxy")
            self.action("Open Proxy", self.wait_and_click_to, self.GET.SELECTOR["Proxy"])
            self.action("Add New Proxy", self.wait_and_click_to, self.GET.SELECTOR["addProxy"])

            ip, pot = self._get_proxy()
            
            self.action("Server", self.wait_and_send_keys_to, self.GET.SELECTOR["server"], ip)
            self.action("Port", self.wait_and_send_keys_to, self.GET.SELECTOR["port"], pot)
            self.action("Save Proxy", self.wait_and_click_to, self.GET.SELECTOR["save"], 6)
            self.action("Start Proxy", self.wait_and_click_to, self.GET.SELECTOR["startProxy"], 6)

            self.Driver.press_keycode(3)
            self.Driver.quit()
            self.GET.KillAppium(self.port, self.driverID)
            time.sleep(2)
            # reconnect
            self.Driver = self.GET.cap(self.port, self.driverID)

    def _get_proxy(self):
        try:
            proxy = self.activity.proxy()
            ip, pot = proxy.split(":") if proxy is not None else ("OK", "OK")

            print("[ \033[92mOK\033[0m ] " + f"Using Proxy: {ip}:{pot}")
            return ip, pot
        except Exception as e:
            print("[ \033[92mNot Found\033[0m ] " + f"Error getting proxy: {e}")
            return None, None

    # def scroll_into_view(self, by, locator, container=None, timeout=15):
        
    #     try:
    #         return WebDriverWait(self.Driver, 2).until(EC.presence_of_element_located((by, locator)))
    #     except Exception:
    #         pass

    #     size = self.Driver.get_window_size()
    #     args = {"direction": "down", "percent": 0.85}
    #     if container is not None:
    #         args["elementId"] = container.id
    #     else:
    #         args.update({"left": 5, "top": 5, "width": max(1, size["width"] - 10), "height": max(1, size["height"] - 10)})

    #     for _ in range(6):
    #         self.Driver.execute_script("mobile: scrollGesture", args)
    #         try:
    #             return WebDriverWait(self.Driver, 1.5).until(EC.presence_of_element_located((by, locator)))
    #         except Exception:
    #             continue

    #     try:
    #         self.Driver.find_element(
    #             AppiumBy.ANDROID_UIAUTOMATOR,
    #             'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()'
    #         )
    #         return WebDriverWait(self.Driver, 2).until(EC.presence_of_element_located((by, locator)))
    #     except Exception:
    #         raise
    
    def scroll_region(self, top: int, left: int, height: int, direction: str = "down", percent: float = 1.0):
        
        # size = self.Driver.get_window_size()
        args = {
            "left": left,
            "top": top,
            "width": 10,
            "height": max(1, height),
            "direction": direction,
            "percent": percent,
        }
        try:
            self.Driver.execute_script("mobile: swipeGesture", args)
        except Exception:
            self.Driver.execute_script("mobile: scrollGesture", args)

    def driverRun(self):


            if self.Driver is None:
                print("Driver did not exist...")
                return 0
            
            # self.scroll_region(top=0, left=0, height=400, direction="down", percent=1.0)

            
            
            self.GET.clear_app_data(self.emu, "com.facebook.orca")
            self.action("Open Messenger", self.wait_and_click_to, self.GET.SELECTOR["Messenger"], 3)

            self.action("Cancel Button")
            time.sleep(8)
            self._find_cancel()
            
            self.action("Create Account")
            # self.action("Create Account", self.wait_and_click_to, self.GET.SELECTOR["createAccount"], 4)
            
            try:
                self.wait_and_click_to(self.GET.SELECTOR["getStarted"],timesleep=5, timeout=10)
            except Exception:
                self.wait_and_click_to(self.GET.SELECTOR["getStarted2"], timeout=10)
                
            self.action("Deny Permission", self.wait_and_click_to, self.GET.SELECTOR["permissionDeny"], timesleep=4, timeout=10)



            #WebDriverWait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, SELECTOR["startAfterDeny"]))).click()

            self.action("Fill First Name", self.wait_and_send_keys_to, self.GET.SELECTOR["firstNameWidget"], self.IMFORMATION["firstName"], 4)

            self.action("Fill Last Name", self.wait_and_send_keys_to, self.GET.SELECTOR["lastNameWidget"], self.IMFORMATION["lastName"], 4)

            self.action("After Name Fill", self.wait_and_click_to, self.GET.SELECTOR["afterNameFill"], 4)

            time.sleep(4)


            # #Month
            # months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            # Month_now= datetime.now().month
            Month = self.IMFORMATION["month"]
            # Year_Back = 0
            # i = 2

            # try:
            #     while months[Month_now- i] != IMFORMATION["month"]:
            #         WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{months[Month_now- i]}"]"""))).click()
            #         if months[Month_now- i] == "Dec":
            #             Year_Back += 1
            #         i += 1
            #         time.sleep(1)
            # except Exception:

            #     WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{months[Month_now- i+1]}"]"""))).click()
            #     if months[Month_now- i] == "Dec":
            #         Year_Back += 1
            #     time.sleep(1)


            # #Day
            # time.sleep(4)


            # TodayDay = datetime.now().day
            Day = self.IMFORMATION["day"]

            # try:
            #     if (Day<TodayDay):
            #         for day in range(TodayDay -1 , Day-1,-1):
            #             WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day:02d}"]"""))).click()

            #             time.sleep(1)
            #     elif (TodayDay<Day):
            #         for day in range(TodayDay +1 , Day+1):
            #             WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day:02d}"]"""))).click()

            #             time.sleep(1)
            # except Exception:
            #     if (Day<TodayDay):
                    
            #         WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day+1:02d}"]"""))).click()

            #         time.sleep(1)
            #     elif (TodayDay<Day):
            #         WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day-1:02d}"]"""))).click()

            #         time.sleep(1)

            #Year
            time.sleep(4)
            Year = self.IMFORMATION["year"]
            Year_Now = 2024 #- Year_Back
            
            try:
                for Year in range(Year_Now,Year-1,-1):

                    self.wait_and_click_to(f"""//android.widget.Button[@text="{Year}"]""", timesleep=0, timeout=5)
                    time.sleep(1)
            except Exception:
                self.wait_and_click_to(f"""//android.widget.Button[@text="{Year+1}"]""", timesleep=0, timeout=5)
                time.sleep(1)
                



            self.action("Set Date", self.wait_and_click_to, self.SELECTOR["setDate"], timesleep=4, timeout=30)

            self.action("After Date", self.wait_and_click_to, self.SELECTOR["afterDate"], timesleep=4, timeout=30)

            Gender = self.IMFORMATION["gender"]
            self.action("Select Gender", self.wait_and_click_to, f"""//android.widget.RadioButton[@content-desc="{Gender}"]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView""", timesleep=4, timeout=30)

            self.action("After Gender", self.wait_and_click_to, self.SELECTOR["afterGender"], timesleep=4, timeout=30)

            self.action("Sign Up Email", self.wait_and_click_to, self.SELECTOR["signUpEmail"], timesleep=4, timeout=30)
            Mail = self.IMFORMATION["email"]
            self.action("Enter Email", self.wait_and_send_keys_to, self.SELECTOR["emailWidget"], Mail, timesleep=4, timeout=30)


            time.sleep(4)
            self.action("Confirm Email", self.wait_and_click_to, self.SELECTOR["confirmEmail"], timesleep=4, timeout=30)

            self.action("Save Data")
            time.sleep(1)

            self._save_data(Mail, Day, Month, Year, Gender)

            self.action("Close appium")
            time.sleep(1)
            self.Driver.quit()
            time.sleep(1)
            self.GET.KillAppium(self.port, self.driverID)

            self.action("Done")
            time.sleep(1)
            self.action("No Action...")
            sys.exit(0)
            
    def _save_data(self, Mail, Day, Month, Year, Gender):
        with open(f"Data.txt", "a") as file:
            file.write("="*50 + "\nFirst Name: {First_Name} \nLast Name: {Last_Name} \nEmail: {Mail}\nDate of Birth: {Day}/{month}/{Year}\nGender: {Gender}\n".format(First_Name=self.IMFORMATION["firstName"],Last_Name=self.IMFORMATION["lastName"],Mail=Mail,Day=Day,month=Month,Year=Year,Gender=Gender))

    def _find_cancel(self):
        passed = False
        while not passed:
            cancel_auth = self.check_element(self.GET.SELECTOR["cancelAuth"], timesleep=0, timeout=3)
            if not cancel_auth:
                find_account = self.check_element(self.GET.SELECTOR["findMyAccount"], timesleep=0, timeout=3)
            else:
                find_account = False

            print(f"from {self.driverID}, cancel_auth: {cancel_auth}")
            if find_account:
                print("click Create account")
                self.wait_and_click_to(self.GET.SELECTOR["getStarted"], timesleep=0, timeout=3)
                
            elif cancel_auth:
                
                print("click Cancel Auth")
                self.wait_and_click_to(self.GET.SELECTOR["cancelAuth"], timesleep=0, timeout=3)
                print("next")
                self.wait_and_click_to(self.GET.SELECTOR["getStarted"], timesleep=1, timeout=15)
                passed = True
                continue
            
            print("check get started")
            passed = self.check_element(self.GET.SELECTOR["findMyAccount"], timesleep=0, timeout=10)
            print(passed)

            # try:
            #     output = subprocess.check_output(f'adb -s {self.emu} shell dumpsys activity activities', shell=True).decode('utf-8')
            #     Attempt = 0
            #     passing = False
            #     for line in output.splitlines():
            #         if re.match("Activities=", line.strip()):
            #             line = line.split("=", 1)
            #             act = line[1].strip("[]")
            #             print("[ \033[92mOK\033[0m ] " + f"Current Activity: {act}")
            #             break

            #     while "AssistedSignInGET" not in act and "AssistedSignInActivity" not in act:

            #         if Attempt < 8:
            #             time.sleep(5)
            #             Attempt += 1
            #             output = subprocess.check_output(f'adb -s emulator-55{(self.driverID-1)*2+54} shell dumpsys activity activities', shell=True).decode('utf-8')
            #             for line in output.splitlines():
            #                 if re.match("Activities=", line.strip()):
            #                     line = line.split("=", 1)
            #                     act = line[1].strip("[]")
            #                     print("[ \033[92mOK\033[0m ] " + f"Current Activity: {act}")
            #                     break
            #         else:
            #             print("Not found try pass")
            #             passing = True
            #             break
            #     if not passing:
            #         print("[ \033[92mOK\033[0m ] " + "Found Cancel Button")
            #         self.wait_and_click_to(self.GET.SELECTOR["cancelAuth"])

            # except subprocess.CalledProcessError as e:
            #     print(f"Error executing adb command: {e}")


