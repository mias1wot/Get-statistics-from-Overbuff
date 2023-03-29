#!/usr/bin/env python
# coding: utf-8

# <h1>Overwatch data collection<br>
#     <small>version 3</small>
# </h1><br>
# 
# The code is originally written via Jupyter Notebook.<br>
# 
# This notebook contains 2 programs:
# 1. Main program for data fetching.
# 2. Program for fixing previously retrieved data which reuses the code of the main program.
# 
# ## 1. Main program
# 
# The data collection is done in 5 stages, described below.<br>
# To execute the program, you need to compile all methods and run main() method located in <b>Stage 0: Program setup</b>.<br>
# Also you can fine-tune the program execution with global variables contained in <b>Stage 0: Program setup</b>. When you change a cell with global variables, you need to <b>run</b> that cell ('Control' + 'Enter'). For instance, here you can set a competitive season for which you want to get information (or set quick play).<br>
# 
# For this file compilation, I suggest you <b>comment out main()</b> method and run all cells ('Cell' -> 'Run All'). After that delete comment from main() method and execute it (click on cell with main(); 'Cell' -> 'Run Cells' or  simply hit a key combination: 'Control' + 'Enter'). The program will be writing its current state of execution.
# <hr>
# 
# <h2>Data collection process:</h2>
# <h3>First stage - data collection:</h3>
# Data is read from "www.overbuff.com" with selenium library.
# 
# The retrieved data is stored in <b>heroStats</b> list of lists.<br>
# Its columns: <b>Stats_Name, Stats_Value</b>.<br>
# Each hero characteristic (including hero name and skill_tier) is written to <b>Stats_Name</b>, the corresponding value - to <b>Stats_Value</b>.
# 
# Important moments:<br>
# <pre>
# 1) Future table columns will have the same names as <b>Stats_Name</b> of <b>heroStats</b>.<br>
# 2) Values with percentage numbers have <b>", %"</b> suffix in their <b>Stats_Name</b>; <b>Stats_Value</b> doesn't contain % - there is only a number. So 'Win Rate' of 50.08% translates into <b>Stats_Name</b>: 'Win Rate, %' and <b>Stats_Value</b>: '50.08'.<br>
# 3) Relative values, such as Damage per 10 minutes, contain <b>" / 10min"</b> suffix. Here "/ 10min" part goes from server and is not hard coded. For example: <b>Stats_Name</b>: 'Damage / 10min'<br>
# </pre>
# 
#   &emsp;Data collection is done by parsing DOM of HTML page and retreiving data from HTML elements. The code won't work if HTML page is changed by site developers. In that case, paths of HTML elements in the code which retrieves info from them will need to be tweaked. Also, if site dev change link paths, it'll need to be changed as well.<br>
#   &emsp;New hero may break the program if it contains some special characters in their names. In that case, you should add this case to heroToOverbuffUrl() and tweakHeroNameForSpecialCases().
# 
# <h3>Second stage - data cleansing:</h3>
# After collecting data, it needs to be cleansed. This is done in the second section of this document.<br>
# Current cleansing:
# <pre>
# 1) Delete comma separator on thousands (e.g. 1,009 => 1009) for each Stats_Value.
# 2) Translate time representation (e.g. '01:23') to seconds (1*60 + 23 => 83)
# </pre>
# 
# <h3>Third stage - data translation into table (building table from data):</h3>
# Here the tabular representation is built. All unique <b>Stats_Name</b> will be the columns of that table (columns don't repeat).<br>
# If a current hero has particular <b>Stats_Name</b>, its corresponding <b>Stats_Value</b> is written to the table. Otherwise the cell will contain <b>None</b>.<br>
# A combination of <b>'Hero'</b> and <b>'Skill Tier'</b> columns is unique for each record.<br>
# 
# <h3>Fourth stage: Data validation and fixing (for columns with numeric data)</h3>
#   &emsp;Finds all non-numeric data in columns which are expected to contain only numeric data (all columns except for STRING_COLUMNS). The user will have a choice what data to drop (via GUI form). The selected data is deleted (set to None), and if all column rows contain empty data, the column will be dropped.<br>
#   &emsp;Thanks to that stage, you won't have corrupted data in the final table. This is important since Overbuff has some missing values.<br>
#   &emsp;Note: found errors are dumped into NAME_OF_FILE_WITH_DATA_ERRORS file.
# 
# 
# <h3>Fifth stage - data table saving:</h3>
# The final table is saved as csv file with a name:<br>
# &emsp;"ow2_quickplay_heroes_stats__{current Date}.csv"<br>
# or<br>
# &emsp;"ow2_season_{OW2_SEASON with 2 digits}_{"FINAL" or "INTERMEDIATE"}_heroes_stats__{current Date}.csv"
# <hr>
# <br>
# 
# 
# ## 2. Program for fixing previously retrieved data<br><small>Located after the main program</small>
# If you've already fetched the data but want to check and fix them, you can use this program. It reuses stage 4 and 5 of the main program. The program consists of 3 stages:
# 1. Input a file path where data table is located.
# 2. Find and fix the errors (stage 4 and 5 of main program).
# 3. Output corrected data table to a specified file.

# <pre>
# 
# 
# </pre>
# <h2>Stage 0: Program setup and run</h2>
# <pre>
# 
# </pre>

# <h3>Global variables documentation:</h3><br>
# 
# <b>1) HERO_ROLE_POSITION</b> = 'None'|'Last'
# 
# &emsp;This determines the 'Role' column position in the table. From the code, the 'Role' must be the second table column. If this is ok, take 'None' value. If you want it to be the last table column (as it provides no visual information to ow players as they know well the roles of each heroes; this column is more for a machine), you should opt for 'Last' value.
# 
# <b>'None'</b> - the Role column will be at it ordinary position.<br>
# <b>'Last'</b> - the Role will be at the last table column.<br>
# <hr>

# <h3>Program setup</h3>

# <h4>Data setup</h4>

# In[ ]:


# These are the names for columns:
HERO_STATS_NAME = 'Hero'
HERO_ROLE_NAME = 'Role'
SKILL_TIER_STATS_NAME = 'Skill Tier'

# For which season to retrieve data?
# Ignored if GET_QUICK_DATA = True.
OW2_SEASON = 1

# Current overwatch season (this is needed to determine the name of file containing the stats data)
# Ignored if GET_QUICK_DATA = True.
OW2_CURRENT_SEASON = 3

# If True, get only data about quick play. Otherwise retrieve competitive data for the specified season.
GET_QUICK_DATA = False

# This determines the 'Role' column position. Information for these values is above.
SPECIFIC_HERO_ROLE_POSITION = 'Last'


# <h4>Browser setup</h4>

# In[ ]:


# [Unnecessary] The path to firefox.exe file. Ignored if FIREFOX_PATH = None.
FIREFOX_PATH = None

# [Unnecessary] The path to firefox profile folder. Ignored if PROFILE_PATH = None.
PROFILE_PATH = None

# [Unnecessary] if EXTENSION_PATH != None, the extension will be added (extension is a file ending with .xpi). It may contain path to adblock, for example.
EXTENSION_PATH = None


# <h4>Debug setup</h4>

# In[ ]:


# If you want to fetch ALL data, set DEBUG to False. If you want to see how the program operate or if you changed the program and want to test it, set DEBUG to True.
DEBUG = True

# Works only if DEBUG is True! Otherwise ignored:

# How many heroes do you need to fetch information about from the site.
# 0 - iterate all heroes.
# Ignored if DEBUG__FETCH_HEROES is not empty
DEBUG__ITERATE_HEROES_COUNT = 1

# How many skill_tiers do you need to fetch information about from the site.
# 0 - iterate all skill_tiers.
DEBUG__ITERATE_SKILL_TIERS_COUNT = 2

# You can specify concrete heroes you want the program to fetch information about (e.g. ['Genji', 'Ashe'])
# Default value: []
DEBUG__FETCH_HEROES = []

# Do you want to see browser during scraping? If so, make it True. Invisibility benefits performance and the browser doesn't blink if front of you.
IS_BROWSER_VISIBLE = True

# This property disables many browser features to operate faster. If you want to explore how the program works, set False for better pictures.
BROWSER_OPTIMIZATION_ENABLED = False

# Indicates whether you want all found stats to be output to console.
OUTPUT_UNIQUE_STATS_TO_CONSOLE = False


# <h4>Column data check setup</h4>

# In[ ]:


# All column errors will be dumped in that file.
NAME_OF_FILE_WITH_DATA_ERRORS = "Columns_errors.txt"

# Columns with str type. All other columns MUST be numeric and will be checked to contain numeric data.
STRING_COLUMNS = [HERO_STATS_NAME, HERO_ROLE_NAME, SKILL_TIER_STATS_NAME]


# <h3>Main program execution (make all setups above if necessary)</h3>

# In[ ]:


# Uncomment this method call when done with compilation
#main()


# <pre>
# </pre>
# <h3>Project tuning is ended here (don't change anything in document that goes below that text).</h3>
# <h3> You need to compile all code below (as well as compile all code above excluding main() method - this is the only execution of this file).</h3>
# <pre>
# 
# </pre>
# 

# In[ ]:


#pip install selenium
#https://github.com/jamie-ralph/overbuff-webscrape/blob/309317ae5316487478c9295eb2281a99a50f94c4/webscrape.py#L33

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
from datetime import datetime
import re
import csv
import numpy as np
from collections import OrderedDict
from pathlib import Path
from enum import Enum

# For UI for data checking
import ipywidgets as widgets
from ipywidgets import Checkbox
from IPython.display import HTML
import threading

# For fixing previously retrieved data (standalone program)
import pandas as pd


# In[ ]:


#heroStats = [['Stats Name', 'Stats Value'], ...]
#Before proceeding with that method, you need to compile functions below in that section
def main():
    curTime = datetime.today().strftime("%H:%M")
    print(f"Starting... ({curTime})\n")
    
    # Stage 4 requires user input from widgets which can't receive focus while main thread is busy. But the main thread
    # cannot continue its work until Stage 4 is done. So here we're creating another thread to make it wait for user input
    # on Stage 4. If you run 'asyncMain' from the same thread, you'll get deadlock! 
    # (Now you'll get just exception that prompts you to call a method from another thread)
    t = threading.Thread(target = asyncMain)
    t.start()


# In[ ]:


def asyncMain():
    heroStats = collectData()
    print()
    
    cleanseData(heroStats)
    print()
    
    (uniqueStats, heroStatsTable) = translateDataToTable(heroStats)
    print()
    
    validateAndFixColumnsWithNumericData(heroStatsTable, uniqueStats)
    print()
        
    fileName = saveTable(heroStatsTable, uniqueStats)
    print()
    
    curTime = datetime.today().strftime("%H:%M")
    print(f"\nProgram has finished successfully. ({curTime})\nYour data is in '{fileName}' file.")


# <pre>
# 
# 
# </pre>
# <h2>Stage 1: Data collection</h2>
# <pre>
# 
# 
# 
# </pre>
# 

# In[ ]:


def collectData():
    browser = None
    try:
        browser = launchBrowser()
        print('Browser launched.')
        
        heroes = getAllHeroes(browser)
        print('All hero names fetched.')
        
        if DEBUG == True and DEBUG__FETCH_HEROES:
            heroStats= collectStatsFromAllHeroes(DEBUG__FETCH_HEROES, browser)
        else:
            heroStats = collectStatsFromAllHeroes(heroes, browser)
        print('Stats of all heroes were fetched.')
        
        print('Data collection (stage 1) completed.')
    finally:
        if browser != None:
            browser.quit()
    
    return heroStats


# In[ ]:


#Launch browser
def launchBrowser():
    options = FirefoxOptions()
    if PROFILE_PATH != None:
        options.add_argument("-profile")
        options.add_argument(profilePath)


    if DEBUG == False or BROWSER_OPTIMIZATION_ENABLED == True:
        #Optimize browser for fatest performance:
        #Time tests for optimization were done on method getHeroInfo("Ana"). Time calculation code is in calculateTime() method.

        #https://erayerdin.com/how-to-make-selenium-load-faster-with-firefox-in-python-ck7ncjyvw00sd8ss1v4i5xob1
        #If only this solution (without stack overflow) Time:  16.203362099999595
        options.set_preference("network.http.pipelining", True)
        options.set_preference("network.http.proxy.pipelining", True)
        options.set_preference("network.http.pipelining.maxrequests", 8)
        options.set_preference("content.notify.interval", 500000)
        options.set_preference("content.notify.ontimer", True)
        options.set_preference("content.switch.threshold", 250000)
        options.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
        options.set_preference("browser.startup.homepage", "about:blank")
        options.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
        options.set_preference("browser.pocket.enabled", False) # Duck pocket too!
        options.set_preference("loop.enabled", False)
        options.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
        options.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
        options.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
        options.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
        options.set_preference("browser.display.use_system_colors", True) # Use system colors.
        options.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
        options.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
        options.set_preference("browser.shell.checkDefaultBrowser", False)
        options.set_preference("browser.startup.homepage", "about:blank")
        options.set_preference("browser.startup.page", 0) # blank
        options.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
        options.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
        options.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
        options.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
        options.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
        options.set_preference("extensions.checkCompatibility", False) # Addon update disabled
        options.set_preference("extensions.checkUpdateSecurity", False)
        options.set_preference("extensions.update.autoUpdateEnabled", False)
        options.set_preference("extensions.update.enabled", False)
        options.set_preference("general.startup.browser", False)
        options.set_preference("plugin.default_plugin_disabled", False)
        options.set_preference("permissions.default.image", 2) # Image load disabled again

        #https://stackoverflow.com/questions/20892768/how-to-speed-up-browsing-in-selenium-firefox
        #If only this solution (without erayerdin.com) Time:  10.61023540000042
        options.set_preference("javascript.enabled", False);
        options.set_preference("permissions.default.stylesheet", 2);
        #options.set_preference("permissions.default.image", 2) 

        #When both stack overflow and erayerdin.com optimization works: 
        # In full browser: Time:  8.615919899999426
        # In headlerss mode: Time:  7.479380399999172


    if DEBUG == False or IS_BROWSER_VISIBLE == False:
        options.add_argument("-headless");
        
    if FIREFOX_PATH != None:
        options.binary_location = FIREFOX_PATH

    browser = webdriver.Firefox(options = options)
    
    if EXTENSION_PATH != None:
        browser.install_addon(EXTENSION_PATH, temporary=True)
    
    return browser


# In[ ]:


# Get all heroes
def getAllHeroes(browser):
    heroesUrl = "https://www.overbuff.com/heroes"
    browser.get(heroesUrl)

    table = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[3]/table/tbody")
    heroesCount = int(table.get_attribute("childElementCount"))
    heroes =  [None] * heroesCount

    for i in range(heroesCount):
        heroes[i] = tweakHeroNameForSpecialCases(table.find_element("xpath", f"tr[{i+1}]/td/div/div[2]/div/a").get_attribute('innerHTML'))
        
    return heroes


# In[ ]:


def tweakHeroNameForSpecialCases(hero):
    #hero.replace('ö', 'o')
    if hero == 'Lúcio':
        return 'Lucio'
    
    #hero.replace('ú', 'u')
    if hero == 'Torbjörn':
        return 'Torbjorn'
    
    return hero


# In[ ]:


# Overbuff represents differently some special symbols in URL (e.g. ':' as '-').
def heroToOverbuffUrl(hero):
    if ':' in hero:
            if ': ' in hero:
                hero = hero.replace(': ', '-')
            else:
                hero = hero.replace(':', '-')
    if ' ' in hero:
        hero = hero.replace(' ', '-')
    if '.' in hero:
        hero = hero.replace('.', '')
        
    return hero.lower()


# In[ ]:


# Overbuff represents seasons as two numbers. If the season has only 1 number, '0' is added in front (e.g. season 2 => '02').
def seasonToOverbuffUrl(season):
    seasonUrl = str(season)
    if season < 10:
        seasonUrl = '0' + seasonUrl
        
    return seasonUrl


# In[ ]:


# This is the main method where stats are collected.
# heroStats = [['Stats Name', 'Stats Value'], ...]
def collectStatsFromAllHeroes(heroes, browser):
    debug_iterateHeroesCount = DEBUG__ITERATE_HEROES_COUNT
    
    fetchingInfo = 'quickplay' if GET_QUICK_DATA else f'competitive, season {OW2_SEASON}'
    print(f"\nFetching heroes stats ({fetchingInfo}):")
    
    heroesCount = len(heroes)
    heroStats = []
    for i in range(heroesCount):
        hero = heroes[i]
        getHeroInfo(heroes[i], browser, heroStats)
        print(f"{i+1} of {heroesCount} heroes finished.")
        
        if DEBUG == True and not DEBUG__FETCH_HEROES:
            debug_iterateHeroesCount -= 1
            if debug_iterateHeroesCount == 0:
                break
                
    print()
    
    return heroStats


# In[ ]:


# 'heroStats' will get appended.
# If a hero didn't exist in that season, they're skipped.
def getHeroInfo(hero, browser, heroStats):
    skillTiers = ["All", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]
    heroUrl = heroToOverbuffUrl(hero)
    ow2SeasonUrl = seasonToOverbuffUrl(OW2_SEASON)

    # Only in debug mode: How many skill tiers to iterate before break
    debug_iterateSkillTiersCount = DEBUG__ITERATE_SKILL_TIERS_COUNT
    
    # If hero didn't exist in this season
    browser.get(f"https://www.overbuff.com/heroes/{heroUrl}?platform=pc&gameMode=competitive&hero={heroUrl}&skillTier={skillTiers[0].lower()}&season=ow2s{ow2SeasonUrl}")
    nodeWithStatsTable = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]")
    if nodeWithStatsTable.get_attribute('innerHTML') == '':
        print(f"{hero} didn't exist in that season.")
        return
    
    
    # Add 'Hero' stats
    heroStats.append([HERO_STATS_NAME, hero])
    
    # Add hero role (support, dmg, tank)
    # We've come to that page when we were checking if the hero existed in current season
    #browser.get(f"https://www.overbuff.com/heroes/{heroUrl}")
    heroRole = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div/div[2]/div/div[3]/div/a/div").get_attribute('innerHTML')
    heroStats.append([HERO_ROLE_NAME, heroRole])
    
    for curSkillTier in skillTiers:
        if GET_QUICK_DATA == True:
            browser.get(f"https://www.overbuff.com/heroes/{heroUrl}?platform=pc&gameMode=quickplay&hero={heroUrl}&skillTier={curSkillTier.lower()}")
        else:
            browser.get(f"https://www.overbuff.com/heroes/{heroUrl}?platform=pc&gameMode=competitive&hero={heroUrl}&skillTier={curSkillTier.lower()}&season=ow2s{ow2SeasonUrl}")
        statsTable = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/div")
        
        # Add 'Skill Tier' stats
        heroStats.append([SKILL_TIER_STATS_NAME, curSkillTier])
        
        # First stats bar
        divWithDiscreteStats = statsTable.find_element("xpath", "div")
        iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats)
            
        # Second stats bar
        divWithDiscreteStats = statsTable.find_element("xpath", "div[2]/div/div")
        iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats)
        
        # Third stats bar
        divWithDiscreteStats = statsTable.find_element("xpath", "div[2]/div[2]/div")
        iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats)
        
        print(f"{hero}: *{curSkillTier}* tier finished.")
        
        # For debug purposes
        if DEBUG == True:
            debug_iterateSkillTiersCount -= 1
            if debug_iterateSkillTiersCount == 0:
                break


# In[ ]:


# 'heroStats' will get appended.
def iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats):
    discreteStatsCount = int(divWithDiscreteStats.get_attribute("childElementCount"))
    for i in range(discreteStatsCount):
        getDiscreteStatsFromStatsDiv(hero, curSkillTier, divWithDiscreteStats.find_element("xpath", f"div[{i+1}]"), heroStats)


# In[ ]:


# 'heroStats' will get appended.
def getDiscreteStatsFromStatsDiv(hero, curSkillTier, discreteStatsDiv, heroStats):
    statsValue = discreteStatsDiv.find_element("xpath", "div/div/span/span").get_attribute('innerHTML')
    statsName = discreteStatsDiv.find_element("xpath", "div/div[2]").get_attribute('innerHTML')
    
    # If stats is in percent
    if '%' in statsValue:
        statsValue = re.search('[0-9\.,]+', statsValue).group()
        statsName += ', %'
        
    # If this is stats per N minutes (for example: /10min)
    try:
        if (statsPerN := discreteStatsDiv.find_element("xpath", "div/div/span[2]")) is not None:
            statsName += f" {statsPerN.get_attribute('innerHTML')}"
    except NoSuchElementException:
        pass
    
    heroStats.append([statsName, statsValue])


# <pre>
# 
# 
# </pre>
# <h2>Stage 2: Data cleansing</h2>
# <pre>
# 
# 
# 
# </pre>
# 

# In[ ]:


# Be careful when 'Stats Name'='Hero' as hero name may contain symbols which are cleared from cleansing methods.
def cleanseData(heroStats):
    print("Cleansing has begun.")
    
    cleansing_deleteThousandsComma(heroStats)
    print(f"Cleansing: Thousands comma delimiter deletion finished.")
    
    cleansing_translateTimeWithColonToSeconds(heroStats)
    print(f"Cleansing: Translation time to seconds finished.")
    
    print(f"Data cleansing (stage 2) finished.")


# In[ ]:


# Data cleansing: delete comma separator on thousands (e.g. 1,009 => 1009).
# This method modifies heroStats.
def cleansing_deleteThousandsComma(heroStats):
    for heroStatsRecord in heroStats:
        if  ',' in heroStatsRecord[1]:
            heroStatsRecord[1] = heroStatsRecord[1].replace(',','')


# In[ ]:


# Data cleansing: translate time representation (e.g. '01:23') to seconds (1*60 + 23 => 83).
# This method modifies heroStats.
def cleansing_translateTimeWithColonToSeconds(heroStats):
    for heroStatsRecord in heroStats:
        if ':' in heroStatsRecord[1] and heroStatsRecord[0] != HERO_STATS_NAME:
            colonIndex = heroStatsRecord[1].find(':')
            heroStatsRecord[1] = str(int(heroStatsRecord[1][:colonIndex]) * 60 + int(heroStatsRecord[1][colonIndex+1:]))


# <pre>
# 
# 
# </pre>
# <h2>Stage 3: Data translation into table</h2>
# <pre>
# 
# 
# 
# </pre>
# 

# In[ ]:


# Returns 'uniqueStats' and 'heroStatsTable'.
def translateDataToTable(heroStats):
    print("Data translation to table has begun.")
    
    uniqueStats = retrieveUniqueStatsFromData(heroStats)
    heroStatsTable = createTableFromData(heroStats, uniqueStats)
    
    print(f"Data translation to table (stage 3) finished.")
    
    if DEBUG == True and OUTPUT_UNIQUE_STATS_TO_CONSOLE == True:
        print(f"\nUnique stats:\n{uniqueStats}\n")
        
    return (uniqueStats, heroStatsTable)


# In[ ]:


# Find all unique stats names.
# All data are immutable here.
def retrieveUniqueStatsFromData(heroStats):
    npHeroStats = np.array(heroStats)
    statsNames = npHeroStats[:,0]
    uniqueStats = list(OrderedDict.fromkeys(statsNames))
    
    if SPECIFIC_HERO_ROLE_POSITION == 'Last':
        setHeroRoleToLastPosition(uniqueStats)
    
    return uniqueStats


# In[ ]:


# Position 'Role' to the last element.
def setHeroRoleToLastPosition(uniqueStats):
    uniqueStats.remove(HERO_ROLE_NAME)
    uniqueStats.append(HERO_ROLE_NAME)


# In[ ]:


# Create tabular form of results.
# All data are immutable here.
def createTableFromData(heroStats, uniqueStats):
    heroStatsTable = []

    curHero = ''
    curSkillTier = ''
    curHeroRole = ''
    curTableRow = -1
    uniqueStatsCount = len(uniqueStats)
    for heroStatsRecord in heroStats:
        #all stats of previous hero were passed
        if heroStatsRecord[0] == HERO_STATS_NAME:
            curHero = heroStatsRecord[1]
            continue
            
        #all stats of previous hero were passed
        if heroStatsRecord[0] == HERO_ROLE_NAME:
            curHeroRole = heroStatsRecord[1]
            continue
            
        #all stats of previous skill_tier of current hero were passed
        if heroStatsRecord[0] == SKILL_TIER_STATS_NAME:
            curSkillTier = heroStatsRecord[1]
            curTableRow += 1
            heroStatsTable.append([None] * uniqueStatsCount)
            heroStatsTable[curTableRow][0] = curHero
            if SPECIFIC_HERO_ROLE_POSITION == 'Last':
                heroStatsTable[curTableRow][1] = curSkillTier
                heroStatsTable[curTableRow][uniqueStatsCount - 1] = curHeroRole
            else:
                heroStatsTable[curTableRow][2] = curSkillTier
                heroStatsTable[curTableRow][1] = curHeroRole
            continue

        #set stats value to current hero of current skill_tier
        #columns in table go in uniqueStats order
        statsIndex = uniqueStats.index(heroStatsRecord[0])
        heroStatsTable[curTableRow][statsIndex] = heroStatsRecord[1]

    return heroStatsTable


# <pre>
# 
# 
# </pre>
# <h2>Stage 4: Data validation and fixing<br><small>(for columns with numeric data)</small></h2>
# <pre>
# 
# 
# 
# </pre>
# 
# This is the only proper way to test stage 4 - with a seperate thread.
#threading.Thread(target = validateAndFixColumnsWithNumericData, args = (heroStatsTable, uniqueStats)).start()
# In[ ]:


# Finds all non-numeric data in columns which MUST contain numeric data (all columns except for STRING_COLUMNS).
# Found info is dumped into NAME_OF_FILE_WITH_DATA_ERRORS file.
# After that the user needs to choose which data to delete via UI form.
# The selected data is deleted (set to None), and if all column rows contain empty data, the column will be dropped.

# Note! This method must be called from a seperate thread (not Main thread as it waits for the user click on a button
# and only Main thread checks button clicks)! Otherwise - exception. If it weren't exception, then it'd be deadlock.

# Returns bool indicating whether data had errors at the beginning of this stage (before fixing them)
# (so that returns True even if all errors were fixed).

# heroStatsTable and uniqueStats are modified in this stage
def validateAndFixColumnsWithNumericData(heroStatsTable, uniqueStats):
    if threading.current_thread() is threading.main_thread():
        raise RuntimeError(f"You must call '{validateAndFixColumnsWithNumericData.__name__}' method from seperate thread, not from Main thread.")
        
    print("Data validation and fixing have begun.")
    
    (erroneousHeroStats, columnHasOnlyEmptyOrErroneousData) = findErrorsInColumnsWithNumericData(heroStatsTable, uniqueStats)
    
    # If an error was found on at least 1 column (data is incorrect)
    if erroneousHeroStats:
        dataHadErrors = True
        # Group erroneous records by column (by stats name)
        # groupedErorrsByCol = {"<Column_name>": [ErroneousHeroRecord]}
        groupedErorrsByCol = {}
        for erroneousHeroRecord in erroneousHeroStats:
            groupedErorrsByCol.setdefault(erroneousHeroRecord.ColName, []).append(erroneousHeroRecord)


        logColumnsWithErrors(erroneousHeroStats, columnHasOnlyEmptyOrErroneousData, uniqueStats, groupedErorrsByCol)

        # Wait for user input
        waitForErroneousDataToBeDeleted = formForDataCleaning(groupedErorrsByCol, columnHasOnlyEmptyOrErroneousData, uniqueStats, heroStatsTable)
        waitForErroneousDataToBeDeleted.wait()
    else:
        # No error found (all data is OK)
        dataHadErrors = False
        print(f"Columns data passed the validation.")
    
    print(f"Data validation and fixing (stage 4) finished.")
    
    return dataHadErrors


# In[ ]:


class ErroneousHeroRecord:
    #Wrong
    Hero = ""
    SkillTier = ""
    ColName = ""  # statsName
    ColValue = ""  # statsValue
    
    RowIndex = -1
    ColIndex = -1
    
    
    def __init__(self, hero, skillTier, columnName, columnValue, RowIndex, ColIndex):
        self.Hero = hero
        self.SkillTier = skillTier
        self.ColName = columnName
        self.ColValue = columnValue
        self.RowIndex = RowIndex
        self.ColIndex = ColIndex
        
    
    def __iter__(self):
        return iter([self.Hero, self.SkillTier, self.ColName, self.ColValue])
        
    def simpleStr(self):
        return f"['{self.Hero}', '{self.SkillTier}', '{self.ColName}', '{self.ColValue}']"
    
    def __str__(self):
        return f'[Hero: {self.Hero}, Rank: {self.SkillTier}, Column_name: \'{self.ColName}\', Column_value: \'{self.ColValue}\''


# In[ ]:


def findErrorsInColumnsWithNumericData(heroStatsTable, uniqueStats):
    heroNameInd = uniqueStats.index(HERO_STATS_NAME)
    skillTierInd = uniqueStats.index(SKILL_TIER_STATS_NAME)
    erroneousHeroStats = []
    columnHasOnlyEmptyOrErroneousData = [True] * len(uniqueStats)
    for col in range(len(uniqueStats)):
        if uniqueStats[col] in STRING_COLUMNS:
            # String columns are not checked and assumed to have the correct data
            columnHasOnlyEmptyOrErroneousData[col] = False
        else:
            # This column MUST contain number
            for row in range(len(heroStatsTable)):
                # Heroes mostly have unique abilities, so the current hero can lack the current ability (None in that case)
                if not cellWithNumberIsEmpty(heroStatsTable[row][col]):
                    if not isNumber(heroStatsTable[row][col]):
                        # curHero, curSkillTier, statsName, statsValue, row, column
                        erroneousHeroStats.append(ErroneousHeroRecord(heroStatsTable[row][heroNameInd], heroStatsTable[row][skillTierInd], uniqueStats[col], heroStatsTable[row][col], row, col))
                    else:
                        # This column has miningful data, so it shouldn't be dropped
                        columnHasOnlyEmptyOrErroneousData[col] = False
            
    
    return (erroneousHeroStats, columnHasOnlyEmptyOrErroneousData)


# In[ ]:


# Dumps all errors to file NAME_OF_FILE_WITH_DATA_ERRORS. 
def logColumnsWithErrors(erroneousHeroStats, columnHasOnlyEmptyOrErroneousData, uniqueStats, groupedErorrsByCol):
    # Find all unique columns containing errors and dump errors to string
    errors = ''
    for erroneousHeroRecord in erroneousHeroStats:
        errors += f'{erroneousHeroRecord.simpleStr()}\n'
        
        
    onlyErroneousDataColumns = []
    # Names of columns which contain only erronious data (they can be safely dropped)
    for i in range(len(columnHasOnlyEmptyOrErroneousData)):
        if columnHasOnlyEmptyOrErroneousData[i]:
            onlyErroneousDataColumns.append(uniqueStats[i])
            
        
    # Output current time
    s = datetime.today().strftime("%H:%M  %d.%m.%Y") + '\n\n'
    
    # Output names of columns with erroneous data (with a label whether it contains only miningless data - erroneous and empty)
    s += 'Columns with errors in data:\n'
    for colWithError in groupedErorrsByCol.keys():
        additionalError = ''
        if(colWithError in onlyErroneousDataColumns):
            additionalError = '  [only miningless data]'
        s += f'{colWithError}{additionalError}\n'
        
        
    s += '\n\nColumns with only miningless data (erroneous and empty) should be dropped.\n'
        
        
    # Output erroneous column data
    s += '\n\nErrors (Hero, Skill tier, Stats name, Stats value):\n'
    s += errors
        
    with open(NAME_OF_FILE_WITH_DATA_ERRORS, "w") as file:
        file.write(s)


# In[ ]:


def formForDataCleaning(groupedErorrsByCol, columnHasOnlyEmptyOrErroneousData, uniqueStats, heroStatsTable):
    # Its structure: 
    '''
    checkboxes = {
        "<Column_name>": {
            "ColIndex": int
            "Parent":  Checkbox,
            "Children": 
            [
                {
                    "Checkbox": Checkbox,
                    "RowIndex": int,
                }
            ]
        }
    }
    checkboxes["col"]["Children"][i].RowIndex
    '''
    checkboxes = {}


    # Header of form
    labelHtml =     f"<h1 align='center'>        Choose all data to drop<br>        <small>choosing a column will drop the whole column</small>    </h1>    <hr>"
    display(HTML(labelHtml))


    for colName, erroneousHeroRecords in groupedErorrsByCol.items():
        colIndex = uniqueStats.index(colName)

        # If you click on parent checkbox, all children checkbox are checked / unchecked
        parentCheckbox = Checkbox(description = colName, layout=widgets.Layout(width='100%'))

        # Add recommendation to drop the column if it has only empty or erroneous data
        if columnHasOnlyEmptyOrErroneousData[colIndex]:
            parentCheckbox.description += f' (This column contains only miningless data (erroneous and empty) - it should be dropped)'

        display(parentCheckbox)
        checkboxes[colName] = {"ColIndex": colIndex, "Parent": parentCheckbox, "Children": []}

        # Create children ckeckboxes and link them to the parent one
        for erroneousHeroRecord in erroneousHeroRecords:
            childCheckbox = Checkbox(description = erroneousHeroRecord.simpleStr(), 
                                  layout=widgets.Layout(width='100%', padding='0 0 0 20px', margin = '-10px 0px 0 0'))
            widgets.dlink((parentCheckbox, 'value'), (childCheckbox, 'value'))
            display(childCheckbox)
            checkboxes[colName]["Children"].append(
            {
                "Checkbox": childCheckbox,
                "RowIndex": erroneousHeroRecord.RowIndex
            })


    # When a user clicks that button, all selected data will be deleted from the table
    dropSelectedDataCapsule = DropSelectedDataCapsule(checkboxes, heroStatsTable, uniqueStats)
    confirmSelectionBtn = widgets.Button(description="Drop selected data", button_style = "danger")
    confirmSelectionBtn.on_click(dropSelectedDataCapsule.onDropSelectedData)
    centered_layout = widgets.Layout(display='flex',
                    flex_flow='column',
                    align_items='center',
                    width='100%')
    display(widgets.HBox(children = [confirmSelectionBtn],layout = centered_layout))
    
    
    return dropSelectedDataCapsule.WaitForErroneousDataToBeDeleted


# In[ ]:


class DropSelectedDataCapsule:
    WaitForErroneousDataToBeDeleted = threading.Event()
    
    def __init__(self, checkboxes, heroStatsTable, uniqueStats):
        self.checkboxes = checkboxes
        self.heroStatsTable = heroStatsTable
        self.uniqueStats = uniqueStats
        self.WaitForErroneousDataToBeDeleted.clear()
        

    # Deletes erroneous data (set None in table) and drops all empty columns, including columns that became empty after deleting erroneous data.
    # Requires checkboxes, heroStatsTable, uniqueStats variables to work
    def onDropSelectedData(self, confirmSelectionBtn):
        # Disable all UI elements
        for _, parentChildrenCheckboxes in self.checkboxes.items(): 
            parentChildrenCheckboxes["Parent"].disabled = True
            for childCheckbox in parentChildrenCheckboxes["Children"]:
                childCheckbox["Checkbox"].disabled = True
        confirmSelectionBtn.disabled = True
        

        # Delete data selected by the user
        columnsToDrop = []
        cellChangedCount = 0 # it doesn't count cells from deleted columns
        for colName, parentChildrenCheckboxes in self.checkboxes.items():
            if parentChildrenCheckboxes["Parent"].value:
                # Drop column 'col'
                columnsToDrop.append(parentChildrenCheckboxes["ColIndex"])
            else:
                # Delete data rows - set None value
                colChanged = 0
                for childCheckbox in parentChildrenCheckboxes["Children"]:
                    if childCheckbox["Checkbox"].value:
                        row = childCheckbox["RowIndex"]
                        col = parentChildrenCheckboxes["ColIndex"]

                        self.heroStatsTable[row][col] = None
                        colChanged += 1

                # If the column now contains only empty rows - drop it.
                if colChanged and columnIsEmpty(self.heroStatsTable, parentChildrenCheckboxes["ColIndex"]):
                    columnsToDrop.append(col)
                else:
                    cellChangedCount += colChanged


        # Delete empty columns and output results to the user
        if not columnsToDrop:
            if cellChangedCount:
                print(f'No column was dropped. Selected data ({cellChangedCount} table cells) was changed to None.')
            else:
                print('No column was dropped, no data was changed.')
        else:
            # Drop columns from the end as it's more efficient and otherwise you'd get error due to column shift caused by previous deletion operation.
            columnsToDrop.reverse()
            droppedColumns = []
            for col in columnsToDrop:
                droppedColumns.append(self.uniqueStats[col])

                dropColumn(self.heroStatsTable, col)
                del self.uniqueStats[col]

            # Inform the user what columns were dropped.
            droppedColumns.reverse()
            for droppedColumn in droppedColumns:
                print(f"'{droppedColumn}' column was dropped.")

            if cellChangedCount:
                print(f'Selected data ({cellChangedCount} table cells) was changed to None (data in deleted columns does NOT count).')
            else:
                print(f'No data was changed (data in deleted columns does NOT count).')
                
             
        # Continue the code as the GUI form was processed
        self.WaitForErroneousDataToBeDeleted.set()


# In[ ]:


# True if None or NaN or 'nan'
def cellWithNumberIsEmpty(value):
    return value == None or str(value) == str(np.nan)


# In[ ]:


def columnIsEmpty(table, col):
    for row in range(len(table)):
        if not cellWithNumberIsEmpty(table[row][col]):
            return False
        
    return True


# In[ ]:


def dropColumn(table, col):
    for row in range(len(table)):
        del table[row][col]


# <pre>
# 
# 
# </pre>
# <h2>Stage 5: Data table saving</h2>
# <pre>
# 
# 
# 
# </pre>
# 

# In[ ]:


# Returns a name of the file with data.
def saveTable(heroStatsTable, uniqueStats, customFileName = ""):
    print("Data table saving has begun.")
    
    if customFileName != "":
        fileName = customFileName
    else:
        curDate = datetime.today().strftime("%Y-%m-%d")

        if GET_QUICK_DATA == True:
            fileName = f'ow2_quickplay_heroes_stats__{curDate}.csv'
        else:
            fileName = f'ow2_season_{seasonToFileName(OW2_SEASON)}_{"FINAL" if OW2_SEASON < OW2_CURRENT_SEASON else "INTERMEDIATE"}_heroes_stats__{curDate}.csv'

    
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header (heroes stats names)
        writer.writerow(uniqueStats)

        # write heroes stats values
        writer.writerows(heroStatsTable)
        
    print(f"Data table saving (stage 5) finished.")
        
    return fileName


# In[ ]:


# Seasons is represented  as two numbers. If the season has only 1 number, '0' is added in front (e.g. season 2 => '02').
def seasonToFileName(season):
    seasonFileName = str(season)
    if season < 10:
        seasonFileName = '0' + seasonFileName
        
    return seasonFileName


# <pre>
# 
# 
# 
# </pre>
# # Program for fixing previously retrieved data
# <pre>
# 
# 
# 
# 
# </pre>

# <h4>Program setup</h4>

# In[ ]:


# Note: all settings from 'Column data check setup' section are also applied.

# [Unnecessary] Path to a file with previously retrieved data table (otherwise you can specify the path during program execution)
INITIAL_DATA_FILE_NAME = ''


# <h4>Program execution (make all setups above if necessary)</h4>

# In[ ]:


# Uncomment this method call when done with compilation
#DataValidatorAndFixer().main()


# <pre>
# </pre>
# <h3>Project tuning is ended here (you are not supposed to change the code below).</h3>
# <pre>
# 
# </pre>
# 

# In[ ]:


# Finds errors in a data table from a specified file and corrects them according to user choice
class DataValidatorAndFixer:
    def main(self):
        self.__outputForm()
        
    
    # There are no other public methods which you are supposed to use!
        
        
    __dataFilePath = ""
    
    # You can write additional code in that method which will be executed 
    # after data validating, fixing and possibly saving (if it did contain errors) finished their work
    def __programFinishedHandler(self, dataHadErrors):
        print("The program has finished.")
        
    
    def __overwriteInitialDataFileCheckboxClick(self, change):
        if change.new == True:
            self.__overwriteInitialFile.add_class('overwrite-file-selected')
        else:
            self.__overwriteInitialFile.remove_class('overwrite-file-selected')
            
    
    def __outputForm(self):
        # Form header
        labelHtml = f"<h1 align='center'>Data validation and correction for a table in file<br></h1>        <hr>"
        display(HTML(labelHtml))
        
        # Form to get a file where input data is located
        # Create File path input 
        display(self.__createFilePathInput("Path to the file that needs data correction (.csv)", INITIAL_DATA_FILE_NAME))
        
        
        # 'Overwrite initial data file' checkbox
        self.__overwriteInitialFile = widgets.Checkbox(description = 'Output final data in that same file.', layout=widgets.Layout(width='100%'))
        self.__overwriteInitialFile.observe(self.__overwriteInitialDataFileCheckboxClick, names='value')
        display(HTML(
             "<style>.overwrite-file-selected {outline: solid red; height: 100%, width: 100%}</style>"
        ))
        display(self.__overwriteInitialFile)
        
        
        #Create Confirmation button
        display(self.__createConfirmationButton(self.__onConfirmInitialDataFilePath))
        
       
    # Creates file path input (Text widget)
    # Sets __filePathTxt
    def __createFilePathInput(self, fieldDescription, fieldInitialValue = ""):
        self.__filePathTxt = widgets.Text(description=fieldDescription, value=fieldInitialValue, style={'description_width': 'initial'}, layout = widgets.Layout(width='100%'))
        return self.__filePathTxt
        
        
    # Creates confirmation button (Button widget) aligned by Ox axis
    # Sets __confirmFilePathBtn
    def __createConfirmationButton(self, callback):
        if callback == None:
            raise ValueError("\'callback\' argument is mandatory to use")
            
        # Confirmation button
        self.__confirmFilePathBtn = widgets.Button(description="Confirm file path", button_style = "primary",  layout = widgets.Layout(width='auto'))
        self.__confirmFilePathBtn.on_click(callback)
        centered_layout = widgets.Layout(display='flex',
                        flex_flow='column',
                        align_items='center',
                        width='100%')
        return widgets.HBox(children = [self.__confirmFilePathBtn],layout = centered_layout)

    
    def __outputFormForFileName(self, fieldDescription, fieldInitialValue = "", callback = None):
        if callback == None:
            raise ValueError("\'callback\' argument is mandatory to use")
            
        # File path input and Confirmation button
        display(self.__createFilePathInput(fieldDescription, fieldInitialValue))
        display(self.__createConfirmationButton(callback))
        
        
    # Button clicked event handler
    def __onConfirmInitialDataFilePath(self, confirmFilePathBtn):
        filePath = self.__filePathTxt.value

        # If a file exists and it's not a directory
        if Path(filePath).is_file():
            self.__dataFilePath = filePath
            self.__disableCurrentInputWidgets()
            
            # It should be the last operation on that method
            threading.Thread(target = self.__runValidationAndDataCorrectionOnFile, args = [filePath]).start()
        else:
            print(f"File path \'{filePath}' doesn't exist.")
                
               
    # Button clicked event handler
    def __onConfirmCorrectedDataFilePath(self, confirmFilePathBtn):
        if self.__overwriteInitialFile.value == True:
            filePath = self.__dataFilePath
        else:
            filePath = self.__filePathTxt.value
        
        # New file must have another path (it cannot overwrite initial data file). It prevents the user to accidentally lose previous data.
        if self.__overwriteInitialFile.value == False and filePath == self.__dataFilePath:
            print("The new file must not be the same as the initial one!")
        else:
            # Save the fixed table
            self.__disableCurrentInputWidgets()

            fileName = saveTable(self.__heroStatsTable, self.__uniqueStats, filePath)
            print()
            
            self.__programFinishedHandler(True)
            
            
    def __disableCurrentInputWidgets(self):
        self.__filePathTxt.disabled = True
        self.__confirmFilePathBtn.disabled = True
        self.__overwriteInitialFile.disabled = True
        
        
    # The main method after the file name with the data was obtained: find errors and clean them.
    # This method must be run from another thread because it calls validateAndFixColumnsWithNumericData which requires another thread for GUI.
    def __runValidationAndDataCorrectionOnFile(self, filePath):
        if threading.current_thread() is threading.main_thread():
            raise RuntimeError(f"You must call '{self.__runValidationAndDataCorrectionOnFile.__name__}' method from seperate thread, not from Main thread.")
        
        # Read data from the file
        # Read empty string as empty string (instead of np.nan) and then replace empty string with None.
        # This is done to prevent saving 'nan' values instead of empty string which was causing a file to grow 2 times in size.
        heroStatsTableUncleaned = pd.read_csv(filePath, keep_default_na=False)
        heroStatsTableUncleaned.replace([''], [None], inplace=True)
        self.__heroStatsTable = heroStatsTableUncleaned.values.tolist()
        self.__uniqueStats = heroStatsTableUncleaned.columns.tolist()

        # Find data errors and process them
        dataHadErrors = validateAndFixColumnsWithNumericData(self.__heroStatsTable, self.__uniqueStats)
        print()
        
        # Output corrected data to the file only if the data did have errors.
        # Skip saving the table if it's been correct from the beginning (so its content hasn't changed - no need to save it).
        if dataHadErrors:
            # Overwrite input data file
            if self.__overwriteInitialFile.value == True:
                self.__onConfirmCorrectedDataFilePath(None)
            else:
                # Form to get file where to output data
                # Ask user for a place where to save the corrected data
                display(self.__createFilePathInput("Path to the file where to save corrected data (.csv)", self.__dataFilePath))
                display(self.__createConfirmationButton(self.__onConfirmCorrectedDataFilePath))
        else:
            self.__programFinishedHandler(False)


# <pre>
# 
# 
# </pre>
# <h2>Test area</h2>
# <pre>
# 
# 
# 
# </pre>
browser = launchBrowser()browser.quit()DEBUG = True
heroStats = []

#hero = "Ana"
#hero = "Mercy"
#hero = "Doomfist"
#hero = "Soldier: 76"
#hero = "Genji"
hero = "Widowmaker"

#browser = launchBrowser()
getHeroInfo(hero, browser, heroStats)heroStats
# <pre>
# 
# 
# </pre>
# <h2>Additional code</h2>
# <pre>
# 
# 
# 
# </pre>

# In[ ]:


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# In[ ]:


def isBrowserAlive(browser):
    try:
        browser.title
        return True
    except:
        return False
        
#isBrowserAlive(browser)


# In[ ]:


import timeit
def calculateTime():
    start = timeit.default_timer()
    
    #Here goes your code.
    
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    
#calculateTime()


# In[ ]:


def threadIsMain():
    return threading.current_thread() is threading.main_thread()


# In[ ]:


print('Compilation finished! You can now start the main() method.')

