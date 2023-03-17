#!/usr/bin/env python
# coding: utf-8

# <h1>Overwatch data collection<br>
#     <small>version 2</small>
# </h1><br>
# 
# The code is originally written via Jupyter Notebook.<br>
# 
# The data collection is done in 3 stages, described below.<br>
# To execute the program, you need to compile all methods and run main() method located in <b>Stage 0: Program setup</b>.<br>
# Also you can fine-tune the program execution with global variables contained in <b>Stage 0: Program setup</b>. When you change a cell with global variables, you need to <b>run</b> that cell ('Control' + 'Enter'). For instance, here you can set a competative season for which you want to get information (or set quick play).<br>
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
# <h3>Third stage - building table from data and saving:</h3>
# Here the tabular representation is built. All unique <b>Stats_Name</b> will be the columns of that table (columns don't repeat).<br>
# If a current hero has particular <b>Stats_Name</b>, its corresponding <b>Stats_Value</b> is written to the table. Otherwise the cell will contain <b>None</b>.<br>
# A combination of <b>'Hero'</b> and <b>'Skill Tier'</b> columns is unique for each record.<br>
# 
# The final table is saved as csv file with name "ow_heroes_data_season3_{YYYY-mm-dd}.csv".

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
# &emsp;This determines the 'Role' stats position in table. From the code, the 'Role' must be the second table column. If this is ok, take 'None' value. If you want it to be the last table column (as it provides no visual information to ow players as they know well the roles of each heroes; this column is more for machine code), you should opt for 'Last' value.
# 
# <b>'None'</b> - the stats column will be at it ordinary position<br>
# <b>'Last'</b> - the stats will be at the last table column<br>
# <hr>

# <h3>Program setup</h3>

# <h4>Data setup</h4>

# In[32]:


# These are the names for columns:
HERO_STATS_NAME = 'Hero'
HERO_ROLE_NAME = 'Role'
SKILL_TIER_STATS_NAME = 'Skill Tier'

# For which season to retrieve data?
# Ignored if GET_QUICK_DATA = True.
OW2_SEASON = 3

# Current overwatch season (this is needed to determine the name of file containing the stats data)
# Ignored if GET_QUICK_DATA = True.
OW2_CURRENT_SEASON = 3

# If True, get only data about quick play. Otherwise retrieve competitive data for the specified season.
GET_QUICK_DATA = False

# This determs the 'Role' stats position. Information for these values is above.
SPECIFIC_HERO_ROLE_POSITION = 'Last'


# <h4>Browser setup</h4>

# In[31]:


# [Unnecessary] The path to firefox.exe file. Ignored if FIREFOX_PATH = None.
FIREFOX_PATH = None

# [Unnecessary] The path to firefox profile folder. Ignored if PROFILE_PATH = None.
PROFILE_PATH = None

# [Unnecessary] if EXTENSION_PATH != None, the extension will be added (extension is a file ending with .xpi). It may contain path to adblock, for example.
EXTENSION_PATH = None


# <h4>Debug setup</h4>

# In[33]:


# If you want to fetch ALL data, set DEBUG to False. If you want to see how the program operate or if you changed the program and want to test it, set DEBUG to True.
DEBUG = True

# Works only if DEBUG is True! Otherwise ignored:

# How many heroes do you need to fetch information about from the site.
# 0 - iterate all heroes.
DEBUG__ITERATE_HEROES_COUNT = 1

# How many skill_tiers do you need to fetch information about from the site.
# 0 - iterate all skill_tiers.
DEBUG__ITERATE_SKILL_TIERS_COUNT = 2

# Do you want to see browser during scraping? If so, make it True. Invisibility benefits performance and the browser doesn't blink if front of you.
IS_BROWSER_VISIBLE = True

# This property disables many browser features to operate faster. If you want to explore how the program works, set False for better pictures.
BROWSER_OPTIMIZATION_ENABLED = False

# Indicates whether you want all found stats to be output to console.
OUTPUT_UNIQUE_STATS_TO_CONSOLE = False


# <h3>Program execution (make all setups above if necessary)</h3>

# In[ ]:


main()


# <pre>
# </pre>
# <h3>Project tuning is ended here (don't change anything in document that goes below that text).</h3>
# <h3> You need to compile all code below (as well as compile all code above excluding main() method - this is the only execution of this file).</h3>
# <pre>
# 
# </pre>
# 

# In[6]:


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


# In[30]:


#heroStats = [['Stats Name', 'Stats Value'], ...]
#Before proceeding with that method, you need to compile functions below in that section
def main():
    heroStats = collectData()
    print()
    cleanseData(heroStats)
    print()
    fileName = translateDataToTableAndSaveTable(heroStats)
    print()
    
    print(f"\nProgram has finished successfully.\nYour data is in '{fileName}' file.")


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

# In[8]:


def collectData():
    browser = None
    try:
        browser = launchBrowser()
        print('Browser launched.')
        heroes = getAllHeroes(browser)
        print('All hero names fetched.')
        heroStats = collectStatsFromAllHeroes(heroes, browser)
        print('Stats of all heroes were fetched.')
        
        print('Data collection (stage 1) completed.')
    finally:
        if browser != None:
            browser.quit()
    
    return heroStats


# In[9]:


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


# In[10]:


#Get all heroes
#fills 'heroes' variable
def getAllHeroes(browser):
    heroesUrl = "https://www.overbuff.com/heroes"
    browser.get(heroesUrl)

    table = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[3]/table/tbody")
    heroesCount = int(table.get_attribute("childElementCount"))
    heroes =  [None] * heroesCount

    for i in range(heroesCount):
        heroes[i] = tweakHeroNameForSpecialCases(table.find_element("xpath", f"tr[{i+1}]/td/div/div[2]/div/a").get_attribute('innerHTML'))
        
    return heroes


# In[11]:


def tweakHeroNameForSpecialCases(hero):
    #hero.replace('ö', 'o')
    if hero == 'Lúcio':
        return 'Lucio'
    
    #hero.replace('ú', 'u')
    if hero == 'Torbjörn':
        return 'Torbjorn'
    
    return hero


# In[12]:


#Overbuff represents differently some special symbols in URL (e.g. ':' as '-')
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


# In[13]:


#Overbuff represents seasons as two numbers. If the season has only 1 number, '0' is added in front (e.g. season 2 => '02')
def seasonToOverbuffUrl(season):
    seasonUrl = str(season)
    if season < 10:
        seasonUrl = '0' + seasonUrl
        
    return seasonUrl


# In[14]:


#This is the main method where stats are collected
#heroStats = [['Stats Name', 'Stats Value'], ...]
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
        
        if DEBUG == True:
            debug_iterateHeroesCount -= 1
            if debug_iterateHeroesCount == 0:
                break
                
    print()
    
    return heroStats


# In[15]:


#'heroStats' will get appended
#If a hero didn't exist in that season, they're skipped
def getHeroInfo(hero, browser, heroStats):
    skillTiers = ["All", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"]
    heroUrl = heroToOverbuffUrl(hero)
    ow2SeasonUrl = seasonToOverbuffUrl(OW2_SEASON)

    #Only in debug mode: How many skill tiers to iterate before break
    debug_iterateSkillTiersCount = DEBUG__ITERATE_SKILL_TIERS_COUNT
    
    #If hero didn't exist in this season
    browser.get(f"https://www.overbuff.com/heroes/{heroUrl}?platform=pc&gameMode=competitive&hero={heroUrl}&skillTier={skillTiers[0].lower()}&season=ow2s{ow2SeasonUrl}")
    nodeWithStatsTable = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]")
    if nodeWithStatsTable.get_attribute('innerHTML') == '':
        print(f"{hero} didn't exist in that season.")
        return
    
    
    #Add 'Hero' stats
    heroStats.append([HERO_STATS_NAME, hero])
    
    #Add hero role (support, dmg, tank)
    #We've come to that page when we were checking if the hero existed in current season
    #browser.get(f"https://www.overbuff.com/heroes/{heroUrl}")
    heroRole = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div/div[2]/div/div[3]/div/a/div").get_attribute('innerHTML')
    heroStats.append([HERO_ROLE_NAME, heroRole])
    
    for curSkillTier in skillTiers:
        if GET_QUICK_DATA == True:
            browser.get(f"https://www.overbuff.com/heroes/{heroUrl}?platform=pc&gameMode=quickplay&hero={heroUrl}&skillTier={curSkillTier.lower()}")
        else:
            browser.get(f"https://www.overbuff.com/heroes/{heroUrl}?platform=pc&gameMode=competitive&hero={heroUrl}&skillTier={curSkillTier.lower()}&season=ow2s{ow2SeasonUrl}")
        statsTable = browser.find_element("xpath", "/html/body/div/div/main/div[2]/div[2]/div[3]/div/div[2]/div")
        
        #Add 'Skill Tier' stats
        heroStats.append([SKILL_TIER_STATS_NAME, curSkillTier])
        
        #first stats bar
        divWithDiscreteStats = statsTable.find_element("xpath", "div")
        iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats)
            
        #second stats bar
        divWithDiscreteStats = statsTable.find_element("xpath", "div[2]/div/div")
        iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats)
        
        #third stats bar
        divWithDiscreteStats = statsTable.find_element("xpath", "div[2]/div[2]/div")
        iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats)
        
        print(f"{hero}: *{curSkillTier}* tier finished.")
        
        #For debug purposes
        if DEBUG == True:
            debug_iterateSkillTiersCount -= 1
            if debug_iterateSkillTiersCount == 0:
                break


# In[16]:


#'heroStats' will get appended
def iterateAllDiscreteStatsInDiv(hero, curSkillTier, divWithDiscreteStats, heroStats):
    discreteStatsCount = int(divWithDiscreteStats.get_attribute("childElementCount"))
    for i in range(discreteStatsCount):
        getDiscreteStatsFromStatsDiv(hero, curSkillTier, divWithDiscreteStats.find_element("xpath", f"div[{i+1}]"), heroStats)


# In[17]:


#'heroStats' will get appended
def getDiscreteStatsFromStatsDiv(hero, curSkillTier, discreteStatsDiv, heroStats):
    statsValue = discreteStatsDiv.find_element("xpath", "div/div/span/span").get_attribute('innerHTML')
    statsName = discreteStatsDiv.find_element("xpath", "div/div[2]").get_attribute('innerHTML')
    
    #if stats is in percent
    if '%' in statsValue:
        statsValue = re.search('[0-9\.,]+', statsValue).group()
        statsName += ', %'
        
    #if this is stats per N minutes (for example: /10min)
    try:
        if (statsPerN := discreteStatsDiv.find_element("xpath", "div/div/span[2]")) is not None:
            statsName += f" {statsPerN.get_attribute('innerHTML')}"
    except NoSuchElementException:
        pass
    
    heroStats.append([statsName, statsValue])


# <strong>Tests:</strong>

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

# In[18]:


#Be careful when 'Stats Name'='Hero' as hero name may contain symbols which are cleared from cleansing methods.
def cleanseData(heroStats):
    print("Cleansing has begun.")
    cleansing_deleteThousandsComma(heroStats)
    print(f"Cleansing: Thousands comma delimiter deletion finished.")
    cleansing_translateTimeWithColonToSeconds(heroStats)
    print(f"Cleansing: Translation time to seconds finished.")
    
    print(f"Data cleansing (stage 2) finished.")


# In[19]:


#Data cleansing: delete comma separator on thousands (e.g. 1,009 => 1009)
#This method modifies heroStats
def cleansing_deleteThousandsComma(heroStats):
    for heroStatsRecord in heroStats:
        if  ',' in heroStatsRecord[1]:
            heroStatsRecord[1] = heroStatsRecord[1].replace(',','')


# In[20]:


#Data cleansing: translate time representation (e.g. '01:23') to seconds (1*60 + 23 => 83)
#This method modifies heroStats
def cleansing_translateTimeWithColonToSeconds(heroStats):
    for heroStatsRecord in heroStats:
        if ':' in heroStatsRecord[1] and heroStatsRecord[0] != HERO_STATS_NAME:
            colonIndex = heroStatsRecord[1].find(':')
            heroStatsRecord[1] = str(int(heroStatsRecord[1][:colonIndex]) * 60 + int(heroStatsRecord[1][colonIndex+1:]))


# <pre>
# 
# 
# </pre>
# <h2>Stage 3: Data translation into table and saving</h2>
# <pre>
# 
# 
# 
# </pre>
# 

# In[21]:


#Returns a name of file with data
def translateDataToTableAndSaveTable(heroStats):
    print("Data translation to table and saving have begun.")
    uniqueStats = retrieveUniqueStatsFromData(heroStats)
    heroStatsTable = createTableFromData(heroStats, uniqueStats)
    print("Data translation to table finished.")
    fileName = saveTable(heroStatsTable, uniqueStats)
    print("Data saving finished.")
    
    print(f"Data translation to table and saving (stage 3) finished.")
    
    if DEBUG == True and OUTPUT_UNIQUE_STATS_TO_CONSOLE == True:
        print(f"\nUnique stats:\n{uniqueStats}\n")
        
    return fileName


# In[22]:


#Find all unique stats names
#All data are immutable here
def retrieveUniqueStatsFromData(heroStats):
    npHeroStats = np.array(heroStats)
    statsNames = npHeroStats[:,0]
    uniqueStats = list(OrderedDict.fromkeys(statsNames))
    
    if SPECIFIC_HERO_ROLE_POSITION == 'Last':
        setHeroRoleToLastPosition(uniqueStats)
    
    return uniqueStats


# In[23]:


#position 'Role' to the last element
def setHeroRoleToLastPosition(uniqueStats):
    uniqueStats.remove(HERO_ROLE_NAME)
    uniqueStats.append(HERO_ROLE_NAME)


# In[24]:


#Create tabular form of results
#all data are immutable here
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


# In[25]:


#Returns a name of file with data
def saveTable(heroStatsTable, uniqueStats):
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
        
        return fileName


# In[26]:


# Seasons is represented  as two numbers. If the season has only 1 number, '0' is added in front (e.g. season 2 => '02')
def seasonToFileName(season):
    seasonFileName = str(season)
    if season < 10:
        seasonFileName = '0' + seasonFileName
        
    return seasonFileName


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
browser = launchBrowser()browser.quit()heroStats = []DEBUG = True
#heroStats = []

#hero = "Ana"
#hero = "Mercy"
#hero = "Doomfist"
hero = "Soldier: 76"

#browser = launchBrowser()
getHeroInfo(hero, browser, heroStats)cleanseData(heroStats)translateDataToTableAndSaveTable(heroStats)
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

# In[27]:


def isBrowserAlive(browser):
    try:
        browser.title
        print(True)
    except:
        print(False)
        
#isBrowserAlive(browser)


# In[28]:


import timeit
def calculateTime():
    start = timeit.default_timer()
    
    #Here goes your code.
    
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    
#calculateTime()

