import time
import chrome_driver
import msedge_driver

ENABLE_ADBLOCK = False
BROWSER_TO_USE = 1
MATRIX_LENGTH = 18
INITIAL_MATRIX = [[0 for x in range(MATRIX_LENGTH)] for y in range(MATRIX_LENGTH)] 
SHAPE_0 = None
SHAPE_1 = None
SHAPE_2 = None

def getShapes():
	global SHAPE_0
	global SHAPE_1
	global SHAPE_2
	
	SHAPE_0 = driver.execute_script("return PlayState.shapes[0].state")
	SHAPE_1 = driver.execute_script("return PlayState.shapes[1].state")
	SHAPE_2 = driver.execute_script("return PlayState.shapes[2].state")

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
driver.execute_script('R.playerData.tutorialCompleted = true;') #Just skip this f*****g tutorial
input("Press any key to start the game....")

getShapes()

# Dumb logging. Needs to ideally be a thread continuously polling for logs.
#while(True):
#	for entry in driver.get_log('browser'):
#		print(entry)
#	time.sleep(100)

