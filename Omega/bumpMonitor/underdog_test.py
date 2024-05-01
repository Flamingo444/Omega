from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from OMEGA import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os.path
import os
from fake_useragent import UserAgent

# vars
username = "nichilusa@gmail.com"
password = "Icecream123!"
user_xpath = "//*[@id='root']/div/div/div[2]/div[2]/div/form/div[1]/label/div[2]/input"
pass_xpath = "//*[@id='root']/div/div/div[2]/div[2]/div/form/div[2]/label/div[2]/input"
signin_xpath = "//*[@id='root']/div/div/div[2]/div[2]/div/form/button"
pickem_xpath = "//*[@id='nav']/div[1]/a[2]"
pregame_xpath = "//*[@id='root']/div/div/div[1]/div/div[3]/div/div[2]/a[3]"

# Set options
options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options.add_argument(f'user-agent={user_agent}')

# Init webdriver
print("Initializing browser...")
driver = webdriver.Chrome(options=options)
driver.get("https://underdogfantasy.com/login")
driver.maximize_window()
print("Done. Logging in...")

time.sleep(2)

# Login & nav to pickem's page
driver.find_element(By.XPATH,user_xpath ).send_keys(username)
time.sleep(2)
driver.find_element(By.XPATH, pass_xpath).send_keys(password)
time.sleep(1)
driver.find_element(By.XPATH, signin_xpath).click()
time.sleep(4)
driver.find_element(By.XPATH, pickem_xpath).click()
time.sleep(1)
driver.find_element(By.XPATH, pregame_xpath).click()
time.sleep(1)
stat_container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "styles__playerListCol__boy4v")))

#players = driver.find_elements(By.CSS_SELECTOR,".styles__overUnderCell__KgzNn")

count = 1

# Update files
csv_path = "data.csv"
if os.path.isfile("data.csv"):
    if os.path.isfile("data_old.csv"):
        os.remove("data_old.csv")
        os.rename("data.csv","data_old.csv")
    else:
        os.rename("data.csv","data_old.csv")
print("Opening CSV file...")

# Begin scraping
with open(csv_path,'w',encoding='UTF8') as csvfile:
    print("Done. Scraping data...")
    while True:
        try:
            line = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[2]/div[2]/div[{count}]').text
            line_list = line.split('\n')
            player_info = []

            # Remove Higher and Lower
            for element in line_list:
                if element.strip() != "Higher" and element.strip() != "Lower":
                    player_info.append(element)

            # Write player to csv
            length = len(player_info)
            player_str = ""
            add_lines = False
            for i in range(0, length):
                if i > 3:
                    add_lines = True
                    if player_str != "":
                        csvfile.write(player_str)
                        csvfile.write("\n")
                        player_str =""
                    player_str = player_info[0].strip() +","+player_info[1].strip()+","+player_info[2].strip().replace("-","")+","+player_info[i].strip()
                    csvfile.write(player_str)
                    csvfile.write("\n")
                    player_str = ""
                elif i == 3:
                    player_str += player_info[i].strip()
                elif i == 2:
                    player_str += player_info[i].strip().replace("-","") + ","
                else:
                    player_str += player_info[i].strip() + ","
            if add_lines is False:
                csvfile.write(player_str)
                csvfile.write("\n")
            count += 1
        except NoSuchElementException:
            print("Done. Comparing data for bumps...")
            break
compareCSV(csv_path,"data_old.csv")
print("Done. Exiting...")

