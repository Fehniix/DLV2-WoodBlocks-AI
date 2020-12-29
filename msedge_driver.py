from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def createMSEdgeDriver():
	# goog:loggingPrefs allows for access to console logs.
	desiredCapabilities = DesiredCapabilities.CHROME
	desiredCapabilities['goog:loggingPrefs'] = { 'browser':'ALL' }

	msedge_options = EdgeOptions()
	msedge_options.use_chromium = True
	
	driver = Edge(options = msedge_options)
	
	return driver