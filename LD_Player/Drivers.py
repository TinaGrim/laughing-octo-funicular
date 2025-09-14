
import os
import re
import sys
import time
import requests
import threading
import subprocess
from Option import option
from Option import Activity
from datetime import datetime 
from selenium.webdriver.common.by import By
from urllib3.exceptions import MaxRetryError
from requests.exceptions import ConnectionError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import  NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as EC


class LDPlayerRemote():
    def __init__(self, driverID: int):
        super().__init__()

        self.driverID = driverID
        self.emu = f"emulator-55{(self.driverID-1)*2+54}"
        self.port = 4722 + self.driverID

        self.GET = option()
        self.SELECTOR = self.GET.SELECTOR
        self.IMFORMATION = self.GET.IMFORMATION
        self.activity = Activity(self.emu, self.driverID)
        self.GET = option()
        self.SELECTOR = self.GET.SELECTOR
        self.IMFORMATION = self.GET.IMFORMATION
        
        self.Driver = self.GET.cap(self.port, self.driverID)
        if self.Driver is None:
            print("Driver did not exist...")
            return 0
        
        time.sleep(2)
        self.ProxyConnect()
        self.driverRun(self.driverID)
        
        
    def ProxyConnect(self):
        try:
            if self.Driver is None:
                print("Driver did not exist...")
                return 0
            self.Driver.press_keycode(3)
            
            try:
                time.sleep(2)
                self.activity.setActivity("Open Proxy")
                time.sleep(3)
                WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["Proxy"] ))).click()
            except Exception as e:
                print(f"Error opening proxy: {e}")

            self.activity.setActivity("Add New")
            time.sleep(3)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["addProxy"] ))).click()

            try:
                proxy = self.activity.proxy()
                ip, pot = proxy.split(":") if proxy is not None else ("OK", "OK")

                print("[ \033[92mOK\033[0m ] " + f"Using Proxy: {ip}:{pot}")
            except Exception as e:
                print("[ \033[92mNot Found\033[0m ] " + f"Error getting proxy: {e}")

            try:
                self.activity.setActivity("Server")
                time.sleep(3)
                clickserver = WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["server"] )))
                clickserver.click()
                time.sleep(1)
                clickserver.send_keys(ip)
            except Exception as e:
                print(f"Error filling server: {e}")
            try:
                self.activity.setActivity("Port")
                time.sleep(3)
                clickport = WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["port"] )))
                clickport.click()
                time.sleep(1)
                clickport.send_keys(pot)
            except Exception as e:
                print(f"Error filling port: {e}")


            self.activity.setActivity("Save Proxy")
            time.sleep(6)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["save"] ))).click()

            self.activity.setActivity("Start Proxy")
            time.sleep(6)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["startProxy"] ))).click()



            self.GET.KillAppium(self.port, self.driverID)

        except (InvalidSessionIdException, MaxRetryError, ConnectionError):
            print("[ \033[91mClose\033[0m ] " + "Closing Appium server During Remote Driver")
            self.activity.setActivity("No Action...")
            sys.exit(1)
        except (NoSuchElementException, TimeoutException):
            print("[ \033[91mClose\033[0m ] " + "Found no element")
            self.activity.setActivity("No Action...")
            sys.exit(1)
        except WebDriverException as e:
            print(f"[ \033[91mClose\033[0m ] " + "Server get error")
            self.activity.setActivity("No Action...")
            sys.exit(1)
            
    def driverRun(self, driverID):

        try:
            
            self.Driver = self.GET.cap(self.port, self.driverID)
            time.sleep(2)
            
            if self.Driver is None:
                print("Driver did not exist...")
                return 0
            

            # GET.KillAppium(port, driverID)



            self.activity.setActivity("Start")
            
            self.Driver.press_keycode(3)
            self.GET.clear_app_data(self.emu, "com.facebook.orca")
            self.activity.setActivity("Messenger")
            time.sleep(3)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH,self.GET.SELECTOR["Messenger"] ))).click()

            self.activity.setActivity("Cancel Button")
            time.sleep(8)
            
            try:
                output = subprocess.check_output(f'adb -s {self.emu} shell dumpsys activity activities', shell=True).decode('utf-8')
                Attempt = 0
                passing = False
                for line in output.splitlines():
                    if re.match("Activities=", line.strip()):
                        line = line.split("=", 1)
                        act = line[1].strip("[]")
                        print("[ \033[92mOK\033[0m ] " + f"Current Activity: {act}")
                        break

                while "AssistedSignInGET" not in act and "AssistedSignInActivity" not in act:

                    if Attempt < 8:
                        time.sleep(5)
                        Attempt += 1
                        output = subprocess.check_output(f'adb -s emulator-55{(driverID-1)*2+54} shell dumpsys activity activities', shell=True).decode('utf-8')
                        for line in output.splitlines():
                            if re.match("Activities=", line.strip()):
                                line = line.split("=", 1)
                                act = line[1].strip("[]")
                                print("[ \033[92mOK\033[0m ] " + f"Current Activity: {act}")
                                break
                    else:
                        print("Not found try pass")
                        passing = True
                        break
                if not passing:
                    print("[ \033[92mOK\033[0m ] " + "Found Cancel Button")
                    WebDriverWait(self.Driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["cancelAuth"]))
                    ).click()

            except subprocess.CalledProcessError as e:
                print(f"Error executing adb command: {e}")
                

            self.activity.setActivity("Create Account")
            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["createAccount"]))).click()

            self.activity.setActivity("Create Account")
            time.sleep(4)
            
            try:
                WebDriverWait(self.Driver, 10).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["getStarted"]))).click()
            except Exception:
                WebDriverWait(self.Driver, 10).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["getStarted2"]))).click()

            time.sleep(4)
            try:
                WebDriverWait(self.Driver, 10).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["permissionDeny"]))).click()
            except Exception:
                pass


            #WebDriverWait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, SELECTOR["startAfterDeny"]))).click()

            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["firstNameWidget"]))).send_keys(self.IMFORMATION["firstName"])
            time.sleep(4)



            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["lastNameWidget"]))).send_keys(self.IMFORMATION["lastName"])
            time.sleep(4)

            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.GET.SELECTOR["afterNameFill"]))).click()

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
                    
                    WebDriverWait(self.Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year}"]"""))).click()
                    time.sleep(1)
            except Exception:
                WebDriverWait(self.Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year+1}"]"""))).click()
                time.sleep(1)
                



            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.SELECTOR["setDate"]))).click()

            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.SELECTOR["afterDate"]))).click()
            

            Gender = self.IMFORMATION["gender"]
            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.RadioButton[@content-desc="{Gender}"]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView"""))).click()

            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.SELECTOR["afterGender"]))).click()

            self.activity.setActivity("sign in email")
            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.SELECTOR["signUpEmail"]))).click()

            time.sleep(4)
            Email = WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.SELECTOR["emailWidget"])))
            Email.click()

            Mail = self.IMFORMATION["emailRan"]
            Email.send_keys(Mail)


            time.sleep(4)
            WebDriverWait(self.Driver, 30).until(EC.presence_of_element_located((By.XPATH, self.SELECTOR["confirmEmail"]))).click()

            self.activity.setActivity("Save Data")
            time.sleep(1)
            with open(f"Data.txt", "a") as file:

                file.write("="*50 + "\nFirst Name: {First_Name} \nLast Name: {Last_Name} \nEmail: {Mail}\nDate of Birth: {Day}/{month}/{Year}\nGender: {Gender}\n".format(First_Name=self.IMFORMATION["firstName"],Last_Name=self.IMFORMATION["lastName"],Mail=Mail,Day=Day,month=Month,Year=Year,Gender=Gender))

            self.activity.setActivity("Close appium")
            time.sleep(1)
            self.Driver.quit()
            self.GET.KillAppium(self.port, driverID)

            self.activity.setActivity("Done")
            time.sleep(1)
            self.activity.setActivity("No Action...")
            sys.exit(0)

        except (InvalidSessionIdException, MaxRetryError, ConnectionError):
            print("[ \033[91mClose\033[0m ] " + "Closing Appium server During Remote Driver")
            self.activity.setActivity("No Action...")
            sys.exit(1)
        except (NoSuchElementException, TimeoutException):
            print("[ \033[91mClose\033[0m ] " + "Found no element")
            self.activity.setActivity("No Action...")
            sys.exit(1)
        except WebDriverException as e:
            print(f"[ \033[91mClose\033[0m ] " + "Server get error")
            self.activity.setActivity("No Action...")
            sys.exit(1)

if __name__ == "__main__":
    URL = "http://127.0.0.1:5000/"
    try:
        r = requests.get(URL + "openOrder")
        response = r.json()
        LDId: list[int] = response.get("openOrder", False)
        print("[ \033[92mOK\033[0m ]" ,"LDPlayer open => ", LDId)
    except Exception as e:
        print(f"Server Error: {e}")

    if LDId:
        for i in LDId:
            Mythread = threading.Thread(
                target=lambda ID=i: LDPlayerRemote(ID))
            Mythread.start()

