from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import logging as logger

# Default logger level (root) is set to WARNING. `logging` ignores any level below it.
logger.root.setLevel(level=logger.NOTSET)

# POST over a JavaScript script to the current tab and return the readyState
def getPageState(driver):        
    return driver.execute_script('return document.readyState')

def getAvailableShapes(driver):
	return driver.execute_script('return PlayState.shapes;')

# goog:loggingPrefs allows for access to console logs.
desiredCapabilities = DesiredCapabilities.CHROME
desiredCapabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

# Pack options to load the Adblock extension.
# This needs to be either abstracted or automated.
chrome_options = Options()
chrome_options.add_argument('load-extension=/Users/Johnny/AppData/Local/Google/Chrome/User Data/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/4.25.1_0/')

# Load Chrome WebDriver.
driver = webdriver.Chrome(desired_capabilities=desiredCapabilities, options=chrome_options)

# Wait for Adblock to show their "welcome" tab...
WebDriverWait(driver, 2)

# switch to it, close it and switch target window back to first.
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])

# Load the game page.
driver.get("https://games.gamesplaza.com/ext/distribution/wood_blocks/index.html?dist.version=2&v1")

# Sleep until the document is ready.
while(getPageState(driver) != 'complete'):
	time.sleep(0.050)

# Let's not go through the tutorial each single time, ay?
# No, seriously, set the tutorialCompleted property to true so that the tutorial doesn't fire.
driver.execute_script('R.playerData.tutorialCompleted = true;')

# Wait for game to load
time.sleep(7)

# Start the game!
driver.execute_script('game.state.start(\'play\')')

# Dumb logging. Needs to ideally be a thread continuously polling for logs.
debug = False
while(debug):
	for entry in driver.get_log('browser'):
		print(entry)
	time.sleep(100)