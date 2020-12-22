from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import time

# goog:loggingPrefs allows for access to console logs.
desiredCapabilities = DesiredCapabilities.CHROME
desiredCapabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

# Pack options to load the Adblock extension.
# This needs to be either abstracted or automated.
chrome_options = Options()
chrome_options.add_argument('load-extension=path_to_adblock')

# Load Chrome WebDriver.
driver = webdriver.Chrome(desired_capabilities=desiredCapabilities, options=chrome_options)

# Wait for Adblock to show their "welcome" tab...
WebDriverWait(driver, 2)

# switch to it, close it and switch target window back to first.
driver.switch_to_window(driver.window_handles[1])
driver.close()
driver.switch_to_window(driver.window_handles[0])

# Load the game page.
driver.get("https://games.gamesplaza.com/ext/distribution/wood_blocks/index.html?dist.version=2&v1")

# Dumb logging. Needs to ideally be a thread continuously polling for logs.
while(True):
	for entry in driver.get_log('browser'):
		print(entry)
	time.sleep(100)