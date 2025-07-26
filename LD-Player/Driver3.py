import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android.uiautomator2.base import UiAutomator2Options
from selenium.webdriver.common.by import By
import subprocess
import os
from Option import option as Get
import unittest
import Drivers as start
from datetime import datetime 

#from Drives 

driver3 = Get().cap(4725, 3)
subprocess.run(["adb", "-s", "emulator-5554", "shell", "pm", "clear", "com.facebook.orca"])
time.sleep(5)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.TextView[@content-desc="Messenger"]"""))).click()
time.sleep(6)

try:
    WebDriverWait(driver3, 3).until(
        EC.presence_of_element_located((By.XPATH, """//android.widget.ImageView[@content-desc="Cancel"]"""))
    ).click()
except Exception:
    pass  

time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.Button[@content-desc="Create new account"]/android.view.ViewGroup"""))).click()


#//android.view.View[@content-desc="Create new account"]
time.sleep(4)

try:
    WebDriverWait(driver3, 1).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Get started"]"""))).click()

except Exception:
    WebDriverWait(driver3, 1).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Create new account"]"""))).click()
time.sleep(4)

   
try:
    WebDriverWait(driver3, 10).until(EC.presence_of_element_located((By.XPATH, """//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"]"""))).click()
except Exception:
    pass
time.sleep(4)

WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).click()

time.sleep(4)
First_Name = Get().Random_Name()
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).send_keys(First_Name)

time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).click()

time.sleep(4)
Last_Name = Get().Random_Name()
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"""))).send_keys(Last_Name)

time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]"""))).click()


#Month


time.sleep(4)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
Month = datetime.now().month
month = Get().Random_Month()
i = 2
Year_Back = 0
while months[Month - i] != month:
    WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{months[Month - i]}"]"""))).click()
    if months[Month - i] == "Dec":
        Year_Back = 1
    i += 1
    time.sleep(1)



#Day
time.sleep(4)

Day = Get().Random_Day()
TodayDay = datetime.now().day
if (Day<TodayDay):
    for day in range(TodayDay -1 , Day-1,-1):
        WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day:02d}"]"""))).click()

        time.sleep(1)
elif (TodayDay<Day):
    for day in range(TodayDay +1 , Day+1):
        WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{day:02d}"]"""))).click()

        time.sleep(1)


#Year
time.sleep(4)
Year = Get().Random_Year()
Year_Now = 2024 - Year_Back
for Year in range(Year_Now,Year-1,-1):
    
    WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@text="{Year}"]"""))).click()
    time.sleep(1)



time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.Button[@resource-id="android:id/button1"]"""))).click()

time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]"""))).click()
Gender = Get().Random_Gender()
time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, f"""//android.widget.Button[@content-desc="{Gender}"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView"""))).click()

time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]"""))).click()

time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Sign up with email"]"""))).click()

time.sleep(4)
Email = WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.widget.EditText""")))
Email.click()

Mail = "Not_Used@email.com"
Email.send_keys(Mail)


time.sleep(4)
WebDriverWait(driver3, 30).until(EC.presence_of_element_located((By.XPATH, """//android.view.View[@content-desc="Next"]
"""))).click()

with open("Data3.txt", "w") as file:
    file.write("First Name: {First_Name}, Last Name: {Last_Name} Email: {Mail}\nDate of Birth: {Day}/{month}/{Year}\nGender: {Gender}".format(First_Name,Last_Name,Mail,Day,month,Year,Gender))





























