import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android.uiautomator2.base import UiAutomator2Options
from selenium.webdriver.common.by import By
import subprocess
import os
from Option import option as Get #type: ignore
from datetime import datetime 
import os
import re
import requests
GET = Get()
SELECTOR = GET.SELECTOR
IMFORMATION = GET.IMFORMATION
current_file = os.path.basename(__file__)
number_match = re.search(r'Driver(\d+)\.py', current_file)

if number_match:
    driver_number = int(number_match.group(1))

Driver = GET.cap(4722 + driver_number, driver_number)




#//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.EditText


if Driver is None:
    print("Driver did not exist...")
    exit(1)
    
time.sleep(5)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH,SELECTOR["Messenger"] ))).click()
time.sleep(8)

try:
    output = currentActivity = subprocess.check_output(f'adb -s emulator-55{(driver_number-1)*2+54} shell dumpsys activity activities', shell=True).decode('utf-8')
    Attempt = 0
    passing = False
    while ".auth.api.credentials.assistedsignin.ui.AssistedSignInActivity" not in output:
        if Attempt < 5:
            time.sleep(3)
            Attempt += 1
            output = subprocess.check_output(f'adb -s emulator-55{(driver_number-1)*2+54} shell dumpsys activity activities', shell=True).decode('utf-8')
        else:
            print("Not found try pass")
            passing = True
            break
    if not passing:
        print("Found")
        WebDriverWait(Driver, 10).until(
            EC.presence_of_element_located((By.XPATH, SELECTOR["cancelAuth"]))
        ).click()

except subprocess.CalledProcessError as e:
    print(f"Error executing adb command: {e}")
    

        


time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["createAccount"]))).click()



time.sleep(4)

try:
    WebDriverWait(Driver, 1).until(EC.presence_of_element_located((By.XPATH, SELECTOR["getStarted"]))).click()
except Exception:
    WebDriverWait(Driver, 1).until(EC.presence_of_element_located((By.XPATH, SELECTOR["getStarted2"]))).click()
time.sleep(4)

   
try:
    WebDriverWait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, SELECTOR["permissionDeny"]))).click()
except Exception:
    pass
time.sleep(4)


#WebDriverWait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, SELECTOR["startAfterDeny"]))).click()

WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["firstNameWidget"]))).send_keys(IMFORMATION["firstName"])
time.sleep(4)



WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["lastNameWidget"]))).send_keys(IMFORMATION["lastName"])
time.sleep(4)

WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["afterNameFill"]))).click()
time.sleep(4)


# #Month
# months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# Month_now= datetime.now().month
Month = IMFORMATION["month"]
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
Day = IMFORMATION["day"]

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
Year = IMFORMATION["year"]
Year_Now = 2024 #- Year_Back

try:
    for Year in range(Year_Now,Year-1,-1):
        
        WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year}"]"""))).click()
        time.sleep(1)
except Exception:
    WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year+1}"]"""))).click()
    time.sleep(1)
    


time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["setDate"]))).click()

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["afterDate"]))).click()

Gender = IMFORMATION["gender"]
time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.RadioButton[@content-desc="{Gender}"]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView"""))).click()

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["afterGender"]))).click()

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["signUpEmail"]))).click()

time.sleep(4)
Email = WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["emailWidget"])))
Email.click()

Mail = IMFORMATION["email"]
Email.send_keys(Mail)


time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, SELECTOR["confirmEmail"]))).click()

with open(f"Data{driver_number}.txt", "w") as file:
    file.write("First Name: {First_Name} \nLast Name: {Last_Name} \nEmail: {Mail}\nDate of Birth: {Day}/{month}/{Year}\nGender: {Gender}".format(First_Name=IMFORMATION["firstName"],Last_Name=IMFORMATION["lastName"],Mail=Mail,Day=Day,month=Month,Year=Year,Gender=Gender))
    
try:
    r = requests.get("http://127.0.0.1:5000/schedule")
    response = r.json().get("scheduleClose",False) 
except Exception as e:
    print(f"Server Can Not Get Schedule status: {e}")

port = 4722 + driver_number
find_pid_cmd = f'netstat -aon | findstr :{port}'
result = subprocess.check_output(find_pid_cmd, shell=True, text=True)
line = result.strip().splitlines()
if response:
    if line:
        pid = line[0].split()[-1]
        kill_cmd = f'taskkill /PID {pid} /F'
        subprocess.run(kill_cmd, shell=True)
        print("Kill LD: ",driver_number)
    else:
        print(f"Not found {port}")