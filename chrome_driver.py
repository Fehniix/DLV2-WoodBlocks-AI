from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def createChromeDriver():
	# goog:loggingPrefs allows for access to console logs.
	desiredCapabilities = DesiredCapabilities.CHROME
	desiredCapabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

	# Pack options to load the Adblock extension.
	# This needs to be either abstracted or automated.
	chrome_options = Options()

	# Load Chrome WebDriver.
	driver = webdriver.Chrome(desired_capabilities=desiredCapabilities, options=chrome_options)
	
	return driver