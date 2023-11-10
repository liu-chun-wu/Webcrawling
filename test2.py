from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
# 設定瀏覽器選項
options = Options()
# 建立 driver
s = Service()
chrome = webdriver.Chrome(service=s, options=options)
url = "https://www.google.com/"
chrome.get(url)
SearchBar = chrome.find_element(By.ID, "APjFqb")
SearchBar.send_keys("戰車世界\ue007")
# 存取 Website

# 等待 5 秒鐘以載入頁面
time.sleep(5)
# 關閉瀏覽器視窗
chrome.close()
