"""
NBA_Stats_Scraper
Author: Samuel Nelson

Script that retrieves the NBA regular season stat leaders in points, rebounds, assists, blocks, 3-pointers made, and
steals from the ESPN website. Retrieved ouput is stored in a newly created Excel file with a separate sheet for each
stat category name. Each sheet includes the top 5 players with their respective averages.
"""

import time
import xlsxwriter
import pandas as pd
from typing import List, Union, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By


# --- Set up the driver ---
url = "https://www.espn.com/nba/stats/_/season/2025/seasontype/3" # URL of the website to be scraped

driver = webdriver.Chrome()
driver.implicitly_wait(5) # Set an implicit wait of 5 seconds to allow time for elements to appear

driver.get(url) # Open the web driver with specified URL
time.sleep(5)


# --- Structure for holding player data ---
points =   [] # Most points
rebounds = [] # Most rebounds
assists =  [] # Most assists
blocks =   [] # Most blocks
threes =   [] # Most 3-pointers made
steals =   [] # Most steals


# --- Helper functions ---
def create_player_profiles(stat_lines: List[str], index: int) -> Union[Tuple[List[str], List[str], List[str], List[str], List[str]], bool]:
    """
    Converts a collection of raw player stat lines into readable format.
    Return a list for each of the top-5 stat leaders with their respective name and average.
    """
    try:
        player1 = stat_lines[index + 1].text.split()
        player2 = stat_lines[index + 2].text.split()
        player3 = stat_lines[index + 3].text.split()
        player4 = stat_lines[index + 4].text.split()
        player5 = stat_lines[index + 5].text.split()

        profile1 = [" ".join(player1[1:-2]), player1[-1]]
        profile2 = [" ".join(player2[1:-2]), player2[-1]]
        profile3 = [" ".join(player3[1:-2]), player3[-1]]
        profile4 = [" ".join(player4[1:-2]), player4[-1]]
        profile5 = [" ".join(player5[1:-2]), player5[-1]]

    except:
        print("Error: create_player_profiles")
        return None

    return profile1, profile2, profile3, profile4, profile5

def appending(dest: List[str], items: List[List[str]]) -> None:
    """
    Adds any number of items to the destination list.
    """
    try:
        for item in items:
            dest.append(item)
    except:
        print("Error: appending")


# --- Find all table row page elements within the page DOM ---
stat_lines = driver.find_elements(By.TAG_NAME, "tr") # Contains some extra page elements as well, but we can generalize and check within core loop


# --- Core of looping through parsed page content ---
line_number = 0
while line_number <= len(stat_lines):
    content = stat_lines[line_number].text.split()
    match content[0]:
        case "POINTS":
            profiles = create_player_profiles(stat_lines, line_number)
            appending(points, profiles)
            line_number += 6 # Fast forward past the 5 player profiles we just recorded
            continue         # Skip to next iteration, so we can miss the extra line_number increment

        case "ASSISTS":
            profiles = create_player_profiles(stat_lines, line_number)
            appending(assists, profiles)
            line_number += 6
            continue

        case "3-POINTERS":
            profiles = create_player_profiles(stat_lines, line_number)
            appending(threes, profiles)
            line_number += 6
            continue

        case "REBOUNDS":
            profiles = create_player_profiles(stat_lines, line_number)
            appending(rebounds, profiles)
            line_number += 6
            continue

        case "BLOCKS":
            profiles = create_player_profiles(stat_lines, line_number)
            appending(blocks, profiles)
            line_number += 6
            continue

        case "STEALS":
            profiles = create_player_profiles(stat_lines, line_number)
            appending(steals, profiles)
            break # Steals is the final category, so we can break to prevent uneccessary loops

    line_number += 1 # Increment to the next line if we don't hit any of the cases


driver.close() # Close the web driver


# --- Convert to data frames ---
column_labels = ["Name", "Average"]
# Convert each of the stat categories to their respective data frames
df_points =   pd.DataFrame(points, columns=column_labels)
df_assists =  pd.DataFrame(assists, columns=column_labels)
df_threes =   pd.DataFrame(threes, columns=column_labels)
df_rebounds = pd.DataFrame(rebounds, columns=column_labels)
df_blocks =   pd.DataFrame(blocks, columns=column_labels)
df_steals =   pd.DataFrame(steals, columns=column_labels)


# --- Write the data to an Excel file ---
# Specify ExcelWriter object so we can write more than a single sheet to a workbook
# Use xlsxwriter as the engine, so we can generate a new file
with pd.ExcelWriter("nba_player_stat_leaders.xlsx", engine="xlsxwriter") as writer:
    df_points.to_excel(writer, sheet_name="POINTS", index=False)
    df_assists.to_excel(writer, sheet_name="ASSISTS", index=False)
    df_threes.to_excel(writer, sheet_name="3-POINTERS MADE", index=False)
    df_rebounds.to_excel(writer, sheet_name="REBOUNDS", index=False)
    df_blocks.to_excel(writer, sheet_name="BLOCKS", index=False)
    df_steals.to_excel(writer, sheet_name="STEALS", index=False)
