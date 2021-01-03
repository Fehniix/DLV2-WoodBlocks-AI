import time
import chrome_driver
import msedge_driver
import os
from dotenv import load_dotenv
from Shape import Shape

# Load .env file with configuration variables which can then be read as environment variables
load_dotenv()

ENABLE_ADBLOCK = True

# 0 - Google Chrome (default if .env is not found)
# 1 - MSEdge
BROWSER_TO_USE = os.getenv('BROWSER_TO_USE') or 0

MATRIX_ORIGIN = (154, 58)
CELL_SIZE = 58

def getShape(x):
	SHAPE = {}
	SHAPE["matrix"] = driver.execute_script("return PlayState.shapes[" + str(x) + "].state")
	SHAPE["startX"] = driver.execute_script("return PlayState.shapes[" + str(x) + "].startX")
	SHAPE["startY"] = driver.execute_script("return PlayState.shapes[" + str(x) + "].startY")
	
	return SHAPE

def getSimpleShape(index):
	# Script to run to get the basic Shape info
	script = '''
		return {{
			state: PlayState.shapes[{0}].state
		}};
	'''.format(index)

	# Executing scripts
	rawShape = driver.execute_script(script)

	return Shape(rawShape)

def getGameMatrixCoordinates(x, y):
	return driver.execute_script('''
		const cell = PlayState.well.cells[x][y]; 
		return {{x: cell.position.x, y: cell.position.y}};
		''')

def placeShapeToMatrix(shapeIndex, x, y):
	coords = getGameMatrixCoordinates(x, y);
	
	placeScript = '''
    PlayState.shapes[{0}].setPosition({1}, {2});
    PlayState.shapes[{0}].parent.scale = {{x: 1, y: 1, type: 25}};
    PlayState.well.tryAddShape(PlayState.shapes[shapeIndex]);
    PlayState.existsShapes--;
	''' % (shapeIndex, coords.x, coords.y)

def getPageState(driver): 
	return driver.execute_script("return document.readyState;") == 'complete'

def deleteAllAds():
	driver.execute_script('''
		function getElementByXpath(path) 
		{
		  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
		}

		toRemove_1 = getElementByXpath(\"//*[@id=\\"coolgames-ad-block\\"]\");
		toRemove_1.remove();

		toRemove_2 = getElementByXpath(\"//*[@id=\\"top_banner\\"]\");
		toRemove_2.remove();
	''')

if BROWSER_TO_USE == 0:
	driver = chrome_driver.createChromeDriver()
elif BROWSER_TO_USE == 1:
	driver = msedge_driver.createMSEdgeDriver()

# maximize the browser window so that you can get the absolute x and y based on the window inner and outer heights
driver.maximize_window()

# Load the game page.
driver.get("https://games.gamesplaza.com/ext/distribution/wood_blocks/index.html?dist.version=2&v1")
driver.execute_script('R.playerData.tutorialCompleted = true;') #Just skip this f*****g tutorial

# We can't get webpage completed status so, we use classic time.sleep
time.sleep(4)

if ENABLE_ADBLOCK:
	deleteAllAds()

# Sleep until the document is ready.
while(not getPageState(driver)):
	time.sleep(0.050)

# Start the game!
driver.execute_script('game.state.start(\'play\')')

time.sleep(2)



input()