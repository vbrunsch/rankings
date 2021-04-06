import numpy as np
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import datetime
from datetime import timedelta
import pandas as pd


url1 = f"https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip"
resp = urlopen(url1)

with ZipFile(BytesIO(resp.read()), 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()
#zipfile = ZipFile(BytesIO(resp.read()))
#print(zipfile)
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
currentDirectory = os.getcwd()
pat = currentDirectory+'/chromedriver'
print(pat)
driver = webdriver.Chrome(options=options, executable_path=pat)
url = "https://data.gov.il/dataset/covid-19"
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
csv_url = driver.execute_script("""
let allLinks = document.querySelectorAll("a");
let targetLink;
for (let i = 0; i < allLinks.length; i++) {
    currTitle = allLinks[i].getAttribute("title");
    if (currTitle === "טבלת ישובים") {
        targetLink = allLinks[i];
        break;
    }
}
let resource = targetLink;
while (resource.className != "resource-item") {
    resource = resource.parentElement;
}
let resourceLinks = resource.querySelectorAll("a");
for (let i = 0; i < resourceLinks.length; i++) {
    if (resourceLinks[i].innerText.includes("להורדת המאגר")) {
        return resourceLinks[i].href;
    }
}
""")

print(csv_url)
