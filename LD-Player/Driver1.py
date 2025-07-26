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

current_file = os.path.basename(__file__)
number_match = re.search(r'Driver(\d+)\.py', current_file)\
    
if number_match:
    driver_number = int(number_match.group(1))

Driver = Get().cap(4722 + driver_number, driver_number)
time.sleep(5)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.TextView[@content-desc="Messenger"]"""))).click()
time.sleep(8)

try:
    WebDriverWait(Driver, 10).until(
        EC.presence_of_element_located((By.XPATH, """//android.widget.ImageView[@content-desc="Cancel"]"""))
    ).click()
except Exception as e:
    print("Cancel err",e)

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup"""))).click()


#//android.view.View[@content-desc="Create new account"]
time.sleep(4)

try:
    WebDriverWait(Driver, 1).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Get started"]"""))).click()
except Exception:
    WebDriverWait(Driver, 1).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Create new account"]"""))).click()
time.sleep(4)

   
try:
    WebDriverWait(Driver, 10).until(EC.presence_of_element_located((By.XPATH, """//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]"""))).click()
except Exception:
    pass
time.sleep(4)

WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).click()

time.sleep(4)
First_Name = Get().Random_Name()
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).send_keys(First_Name)

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).click()

time.sleep(4)
Last_Name = Get().Random_Name()
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).send_keys(Last_Name)

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]"""))).click()


#Month


time.sleep(4)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
Month_now= datetime.now().month
month= Get().Random_Month()
Year_Back = 0
i = 2

try:
    while months[Month_now- i] != month:
        WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{months[Month_now- i]}"]"""))).click()
        if months[Month_now- i] == month:
            Year_Back += 1
        i += 1
        time.sleep(1)
except Exception:

    WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{months[Month_now- i+1]}"]"""))).click()
    if months[Month_now- i] == month:
        Year_Back += 1
    time.sleep(1)


#Day
time.sleep(4)

Day = Get().Random_Day()
TodayDay = datetime.now().day
try:
    if (Day<TodayDay):
        for day in range(TodayDay -1 , Day-1,-1):
            WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day:02d}"]"""))).click()

            time.sleep(1)
    elif (TodayDay<Day):
        for day in range(TodayDay +1 , Day+1):
            WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day:02d}"]"""))).click()

            time.sleep(1)
except Exception:
    if (Day<TodayDay):
        
        WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day+1:02d}"]"""))).click()

        time.sleep(1)
    elif (TodayDay<Day):
        WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day-1:02d}"]"""))).click()

        time.sleep(1)

#Year
time.sleep(4)
Year = Get().Random_Year()
Year_Now = 2024 - Year_Back

try:
    for Year in range(Year_Now,Year-1,-1):
        
        WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year}"]"""))).click()
        time.sleep(1)
except Exception:
    WebDriverWait(Driver, 5).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year+1}"]"""))).click()
    time.sleep(1)
    


time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.Button[@resource-id="android:id/button1"]"""))).click()

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]"""))).click()

Gender = Get().Random_Gender()
time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@content-desc="{Gender}"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView"""))).click()

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]"""))).click()

time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Sign up with email"]"""))).click()

time.sleep(4)
Email = WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.EditText""")))
Email.click()

Mail = "Not_Used@email.com"
Email.send_keys(Mail)


time.sleep(4)
WebDriverWait(Driver, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]
"""))).click()

with open("Data1.txt", "w") as file:
    file.write("First Name: {First_Name}, Last Name: {Last_Name} Email: {Mail}\nDate of Birth: {Day}/{month}/{Year}\nGender: {Gender}".format(First_Name=First_Name,Last_Name=Last_Name,Mail=Mail,Day=Day,month=month,Year=Year,Gender=Gender))





























