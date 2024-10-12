from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import urllib3 # urllib3 es un cliente HTTP potente y fácil de usar para Python.
import re # Expresiones regulares 
import time
import pandas as pd
import numpy as np


url = "https://ew.com/best-book-to-screen-adaptations-of-all-time-8685833"
selenium_path = "../../../Selenium_eject/chromedriver.exe"

service = Service(executable_path= selenium_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
close_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/div/div[1]/div/div[2]/div/button[2]')))

close_cookies.click()

content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/article/div[2]/div[3]/div[2]")))
titles = content.find_elements(By.TAG_NAME, "h2")
print("acceso correcto a datos")

tabla_dict = {"libro": [title.text.split(" and ")[0] for title in titles],
              "película": [title.text.split(" and ")[1].split("(")[0] for title in titles],
              "film_year": [title.text.split(" and ")[1].split("(")[1].replace(")","") for title in titles]} 

book_adapt_df = pd.DataFrame(tabla_dict)

book_adapt_df.to_csv("../data/bookfilm_adapt.csv")