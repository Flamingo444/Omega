from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from OMEGA import *
from selenium.common.exceptions import NoSuchElementException
import os.path
import os

allPlayersOld = 'all_players_old.csv'
allPlayers = 'all_players.csv'

driver = webdriver.Chrome()
driver.get("https://app.prizepicks.com/")
driver.maximize_window()

driver.find_element(By.CLASS_NAME, "close").click()
time.sleep(2)

sports = ['NBA', 'NBA2H', 'NBA4Q', 'CBB', 'CBB2H', 'PGA', 'NHL', 'NBA1H', 'SOCCER', 'CSGO', 'WCBB', 'XFL', 'TENNIS', 'LoL', 'F1', 'NASCAR', 'Dota2', 'NFLSZN', 'AFL', 'MLBSZN', 'WEURO']

while True:
# EVERYTHING FROM THE "for sports in sports" LOOP DEALS WITH THE SCRAPER AND WORKDS
    all_players = []
    for sport in sports:
        try:
            driver.find_element(By.XPATH, f"//div[normalize-space()='{sport}']").click()
            time.sleep(1)

            # Wait for the stat-container element to be present and visible
            stat_container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

            # Find all stat elements within the stat-container
            # i.e. categories is the list ['Points','Rebounds',...,'Turnovers']
            categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

            # Initialize empty list to store data
            players = []

            # Iterate over each stat element
            for category in categories:
                # Click the stat element
                line = '-'*len(category)
                print(line + '\n' + category + f' ({sport})' + '\n' + line)
                driver.find_element(By.XPATH, f"//div[text()='{category}']").click()
                time.sleep(2)

                projections = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

                for projection in projections:
                    names = projection.find_element(By.XPATH, './/div[@class="name"]').text
                    points= projection.find_element(By.XPATH, './/div[@class="presale-score"]').get_attribute('innerHTML')
                    text = projection.find_element(By.XPATH, './/div[@class="text"]').text.replace('\n','')
                    #print(names, points, text)

                    player = {'Name': names, 'Prop':points, 'Line':text}
                    players.append(player)

            # THE HOLY GRAIL OF DATA
            all_players += players

        except NoSuchElementException:
            # Catch any exceptions and continue to the next sport
            print(f"No {sport} data available.")
            continue

 # COMPARE DATA (BELOW AND SO FORTH)

    # Check if all_players.csv exists
    if os.path.isfile(allPlayers):

            # If it does and all_players_old.csv also exists
            if os.path.isfile(allPlayersOld):
                os.remove(allPlayersOld)
                os.rename(allPlayers,allPlayersOld)
                df_all = pd.DataFrame(all_players)
                df_all.to_csv(allPlayers, index=False)

            else: # If all_players_old.csv does not exist
                os.rename(allPlayers,allPlayersOld)
                df_all = pd.DataFrame(all_players)
                df_all.to_csv(allPlayers, index=False)

            # Compare new and old data
            compareCSV(allPlayers, allPlayersOld)

    else:
        # If all players data file doesn't exist, create it and save new player data
        df_all = pd.DataFrame(all_players)
        df_all.to_csv(allPlayers, index=False)

    print("Waiting for 2 minutes before checking again...")
    time.sleep(120)