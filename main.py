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
BROWSER_TO_USE = os.getenv('BROWSER_TO_USE') or 'chrome'

MATRIX_ORIGIN = (154, 58)
CELL_SIZE = 58

driver = None

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
				const cell = PlayState.well.cells[{0}][{1}]; 
				return {{x: cell.position.x, y: cell.position.y}};
			'''.format(x, y))

def placeShapeOnMatrix(shapeIndex, x, y):
	coords = getGameMatrixCoordinates(x, y)
	
	placeScript = '''
		PlayState.shapes[{0}].setPosition({1}, {2});
		PlayState.shapes[{0}].parent.scale = {{x: 1, y: 1, type: 25}};
		PlayState.well.tryAddShape(PlayState.shapes[{0}]);
		PlayState.existsShapes--;
	'''.format(shapeIndex, coords['x'], coords['y'])

	driver.execute_script(placeScript)

	# 1 second is enough for the game to correctly register shape placement on the matrix for the vast majority of devices
	time.sleep(1.0)

def getPageState(driver): 
	return driver.execute_script("return window.gameLoaded;") == True

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

if BROWSER_TO_USE == 'chrome':
	driver = chrome_driver.createChromeDriver()
elif BROWSER_TO_USE == 'msedge':
	driver = msedge_driver.createMSEdgeDriver()

# maximize the browser window so that you can get the absolute x and y based on the window inner and outer heights
driver.maximize_window()

# Load the game page. WebDriver waits for page load completion
driver.get("https://games.gamesplaza.com/ext/distribution/wood_blocks/index.html?dist.version=2&v1")

# Inject code in onload event
driver.execute_script('''
	window.proto = LoadState.loadComplete.prototype; 
	LoadState.loadComplete = () => {{ 
		proto.constructor(); 
		window.gameLoaded = true; 
	}};
''')

# Skip tutorial
driver.execute_script('R.playerData.tutorialCompleted = true;')

# Sleep until the document is ready.
while(not getPageState(driver)):
	time.sleep(0.050)

if ENABLE_ADBLOCK:
	deleteAllAds()

# Start the game!
driver.execute_script('game.state.start(\'play\')')

# Wait for PlayState to be fully created
time.sleep(0.5)

# Try placing the first shape on coords (5, 5)
placeShapeOnMatrix(0, 2, 2)


placeShapeOnMatrix(1, 6, 6)

input()