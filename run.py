from config import *
from setting import *

import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import time
import re
import csv
from datetime import datetime
from datetime import date

def execute_code():
    threading.Timer(120.0, execute_code).start()

    profile_id = fnGetUUID()
    port = get_debug_port(profile_id)
    driver = get_webdriver(port)
    driver.get(TARGET_URL)
    time.sleep(60)

    match_dates = []
    match_time = []
    home_team_name = []
    away_team_name = []
    home_team_odds = []
    away_team_odds = []
    scores = []
    home_team_Asian_Handicap_odds = []
    away_team_Asian_Handicap_odds = []
    home_team_Line = []
    away_team_Line = []
    num = [0, 0, 0, 0, 0, 0]
    n = 0
    date_num = 0
    write_result = []
    result_league_names = []
    result_match_rounds = []
    result_match_dates = []
    result_match_times = []
    result_home_team_names = []
    result_away_team_names = []
    result_home_team_odds = []
    result_away_team_odds = []
    result_home_team_Asian_Handicap_odds = []
    result_away_team_Asian_Handicap_odds = []
    result_home_team_Lines = []
    result_away_team_Lines = []

    league_name = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/span').text
    match_round = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div[1]/div/span').text
    # print(league_name)
    header = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]')

    all_childrens = header.find_elements(By.XPATH, './div')

    for c in range(0, len(all_childrens)):
        div_class_name = all_childrens[c].get_attribute("class")
        div_childrens = all_childrens[c].find_elements(By.XPATH, './*')
        if (div_class_name.__contains__("rcl-MarketHeaderLabel-isdate")):
            match_dates.append(all_childrens[c].text)
            n = n + 1
        elif (len(div_childrens) != 0) :
            num[n-1] = num[n-1] + 1

    match_times = driver.find_elements(By.CLASS_NAME, 'src-ParticipantFixtureDetailsExtraLineHigher_BookCloses')

    for i in range(0, len(match_times)):
        match_time.append(match_times[i].text)

    team_names = driver.find_elements(By.CLASS_NAME, 'src-ParticipantFixtureDetailsExtraLineHigher_TeamWrapper')

    for i in range(len(team_names)):
        
        if (i % 3 == 0):
            home_team_name.append(team_names[i].text)

        elif (i % 3 ==1):
            away_team_name.append(team_names[i].text)

    scores = driver.find_elements(By.CLASS_NAME, 'src-ParticipantCenteredStacked48ET')

    for j in range(0, len(home_team_name) * 3):
        if (j % 3 == 0):
            home_team_odds.append(scores[j].text)
        elif (j % 3 ==1):
            away_team_odds.append(scores[j].text)

    for k in range(len(home_team_name) * 3, len(home_team_name) * 3 * 2):
        if (k % 3 == 0):
            home_team_Asian_Handicap_odds.append(scores[k].text)
        elif (k % 3 ==1) :
            away_team_Asian_Handicap_odds.append(scores[k].text)

    for l in range(len(home_team_name) * 3 * 2, len(home_team_name) * 3 * 3):
        if (l % 3 == 0):
            home_team_Line.append(scores[l].text)
        elif (l % 3 ==1) :
            away_team_Line.append(scores[l].text)

    now_time = str(pd.datetime.now().year) + str(pd.datetime.now().month) + str(pd.datetime.now().day) + str(pd.datetime.now().hour) + str(pd.datetime.now().minute) + str(pd.datetime.now().second)
    result_file_name = now_time + ".csv"
    print(">>>>>", result_file_name)
    print(type(result_file_name))
    for j in range(0, len(num)):
        
        for i in range(0, num[j]):

            result_league_names.append(league_name)
            result_match_rounds.append(match_round)
            result_match_dates.append(match_dates[j])
            result_match_times.append(match_time[date_num + i])
            result_home_team_names.append(home_team_name[date_num + i])
            result_away_team_names.append(away_team_name[date_num + i])
            result_home_team_odds.append(home_team_odds[date_num + i])
            result_away_team_odds.append(away_team_odds[date_num + i])
            result_home_team_Asian_Handicap_odds.append(home_team_Asian_Handicap_odds[date_num + i])
            result_away_team_Asian_Handicap_odds.append(away_team_Asian_Handicap_odds[date_num + i])
            result_home_team_Lines.append(home_team_Line[date_num + i])
            result_away_team_Lines.append(away_team_Line[date_num + i])

            write_data = {}

            write_data["League Name"] = league_name
            write_data["Match Round"] = match_round
            write_data["Match Date"] = match_dates[j]
            write_data["Match Time"] = match_time[date_num + i]
            write_data["Home Team Name"] = home_team_name[date_num + i]
            write_data["Away Team Name"] = away_team_name[date_num + i]
            write_data["Home Team Odds"] = home_team_odds[date_num + i]
            write_data["Away Team Odds"] = away_team_odds[date_num + i]
            write_data["Home Team Asian Handicap Odds"] = home_team_Asian_Handicap_odds[date_num + i]
            write_data["Away Team Asian Handicap Odds"] = away_team_Asian_Handicap_odds[date_num + i]
            write_data["Home Team Line"] = home_team_Line[date_num + i]
            write_data["Away Team Line"] = away_team_Line[date_num + i]

            write_result.append(write_data)

            dict = {'League Name': result_league_names, 'Match Round': result_match_rounds, 'Match Date': result_match_dates, 'Match Time': result_match_times, 'Home Team Name': result_home_team_names, 'Away Team Name': result_away_team_names, 'Home Team Odds': result_home_team_odds, 'Away Team Odds': result_away_team_odds, 'Home Team Asian Handicap Odds': result_home_team_Asian_Handicap_odds, 'Away Team Asian Handicap Odds': result_away_team_Asian_Handicap_odds, 'Home Team Line': result_home_team_Lines, 'Away Team Line': result_away_team_Lines}
            df = pd.DataFrame(dict)
            df.to_csv(result_file_name)

        date_num = date_num + num[j]

    driver.close()
    
execute_code()