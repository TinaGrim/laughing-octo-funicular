import time
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
import subprocess
from appium.options.android.uiautomator2.base import UiAutomator2Options
from Option import option as Get
def drivers_startup(Number):
    
    if Number ==1:
        driver1 = Get().cap(4723, 1)
        return (driver1,)
    elif Number == 2:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        return (driver1, driver2)
    elif Number == 3:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        return (driver1, driver2, driver3)
    elif Number == 4:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        return (driver1, driver2, driver3, driver4)
    elif Number == 5:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        driver5 = Get().cap(2727, 5)
        return (driver1, driver2, driver3, driver4, driver5)
    elif Number == 6:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        driver5 = Get().cap(2727, 5)
        driver6 = Get().cap(2728, 6)
        return (driver1, driver2, driver3, driver4, driver5, driver6)
    elif Number == 7:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        driver5 = Get().cap(2727, 5)
        driver6 = Get().cap(2728, 6)
        driver7 = Get().cap(2729, 7)
        return (driver1, driver2, driver3, driver4, driver5, driver6, driver7)
    elif Number == 8:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        driver5 = Get().cap(2727, 5)
        driver6 = Get().cap(2728, 6)
        driver7 = Get().cap(2729, 7)
        driver8 = Get().cap(2730, 8)
        return (driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8)
    elif Number == 9:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        driver5 = Get().cap(2727, 5)
        driver6 = Get().cap(2728, 6)
        driver7 = Get().cap(2729, 7)
        driver8 = Get().cap(2730, 8)
        driver9 = Get().cap(2731, 9)
        return (driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8, driver9)
    elif Number == 10:
        driver1 = Get().cap(4723, 1)
        driver2 = Get().cap(4724, 2)
        driver3 = Get().cap(2725, 3)
        driver4 = Get().cap(2726, 4)
        driver5 = Get().cap(2727, 5)
        driver6 = Get().cap(2728, 6)
        driver7 = Get().cap(2729, 7)
        driver8 = Get().cap(2730, 8)
        driver9 = Get().cap(2731, 9)
        driver10 = Get().cap(2732, 10) 
        return (driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8, driver9, driver10 )

        

        