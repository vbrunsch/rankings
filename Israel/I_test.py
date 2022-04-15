import platform
import numpy as np
import datetime
from datetime import timedelta
import pandas as pd

import re
import os
import time
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def chrome_version():
    osname = platform.system()
    if osname == 'Darwin':
        installpath = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
    elif osname == 'Windows':
        installpath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    elif osname == 'Linux':
        installpath = "/usr/bin/google-chrome"
    else:
        raise NotImplemented(f"Unknown OS '{osname}'")

    verstr = os.popen(f"{installpath} --version").read().strip('Google Chrome ').strip()
    return verstr
  
print(chrome_version())
