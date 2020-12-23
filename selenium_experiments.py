import chrome_driver
import msedge_driver
import time

ENABLE_ADBLOCK = False
BROWSER_TO_USE = 1

if BROWSER_TO_USE == 0:
	driver = chrome_driver.createChromeDriver(ENABLE_ADBLOCK)
elif BROWSER_TO_USE == 1:
	driver = msedge_driver.createMSEdgeDriver(ENABLE_ADBLOCK)

if ENABLE_ADBLOCK:
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