import numpy as np
import datetime
from datetime import timedelta
import pandas as pd

import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_url = "https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip"
resp = urlopen(chromedriver_url)
with ZipFile(BytesIO(resp.read()), 'r') as zipObj:
    zipObj.extractall()
mode = os.stat('./chromedriver').st_mode
os.chmod('./chromedriver', mode | 0o111)

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')

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
