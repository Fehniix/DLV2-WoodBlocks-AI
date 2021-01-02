import time
import chrome_driver
import msedge_driver
import pyautogui
from Shape import Shape

ENABLE_ADBLOCK = True
BROWSER_TO_USE = 0
MATRIX_LENGTH = 18
INITIAL_MATRIX = [[0 for x in range(MATRIX_LENGTH)] for y in range(MATRIX_LENGTH)]

def getShape(x):
	SHAPE = {}
	SHAPE["matrix"] = driver.execute_script("return PlayState.shapes[" + str(x) + "].state")
	SHAPE["startX"] = driver.execute_script("return PlayState.shapes[" + str(x) + "].startX")
	SHAPE["startY"] = driver.execute_script("return PlayState.shapes[" + str(x) + "].startY")
	
	return SHAPE

def getSimpleShape(index):
	# Script to run to get the basic Shape info
	_script = '''
		return {{
			state: PlayState.shapes[{0}].state,
			startX: PlayState.shapes[{0}].startX,
			startY: PlayState.shapes[{0}].startY
		}};
	'''.format(index)

	# Executing scripts
	rawShape = driver.execute_script(_script)

	return Shape(rawShape)

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

# Converts the element's x,y window location to screen coordinates
def getElementScreenCoordinates(element):
	# Element's location within the window
	windowCoords = element.location
	
	# Height of navigation bar, window controls etc.
	browserPanelsHeight = driver.execute_script('return window.outerHeight - window.innerHeight;') * screenHeightRatio

	# Very simple proportion.
	return windowCoords['x'] * screenWidthRatio, windowCoords['y'] * screenHeightRatio + browserPanelsHeight

if BROWSER_TO_USE == 0:
	driver = chrome_driver.createChromeDriver()
elif BROWSER_TO_USE == 1:
	driver = msedge_driver.createMSEdgeDriver()

# maximize the browser window so that you can get the absolute x and y based on the window inner and outer heights
driver.maximize_window()

# Load the game page.
driver.get("https://games.gamesplaza.com/ext/distribution/wood_blocks/index.html?dist.version=2&v1")
driver.execute_script('R.playerData.tutorialCompleted = true;') #Just skip this f*****g tutorial

# Real screen size
screenSize = pyautogui.size()
# Size ratio between real screen size and browser window size
screenWidthRatio 	= screenSize.width / driver.execute_script('return window.screen.width;')
screenHeightRatio 	= screenSize.height / driver.execute_script('return window.screen.height;')
# Size ratio between real screen size and browser window outer size
outerWidthRatio = screenSize.width
outerHeightRatio = screenSize.height / driver.execute_script('return window.outerHeight;')

# We can't get webpage completed status so, we use classic time.sleep
time.sleep(4)

if ENABLE_ADBLOCK:
	deleteAllAds()

canvasElem = driver.find_element_by_xpath("//*[@id=\"gameContainer\"]/canvas")

panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
abs_x = int(canvasElem.location['x'])
abs_y = int(canvasElem.location['y']) + panel_height
canvasSizeX = canvasElem.size["width"] #+ 250
canvasSizeY = canvasElem.size["height"] #+ 150

canvas = driver.find_element_by_css_selector('#gameContainer > canvas')
canvas_x, canvas_y = getElementScreenCoordinates(canvas)
canvas_width = canvas.size['width']
canvas_height = canvas.size['height']

# Bounding box coordinates in terms of ratios with respect to outerWidth and outerHeight (coord / outerSize)
shapesBoundingBoxCoords = [
	(0.3684895833333333, 0.7391304347826086),
	(driver.execute_script('return window.outerWidth;') / 566 * 2, driver.execute_script('return window.outerHeight;') / 680 * 2),
	(driver.execute_script('return window.outerWidth;') / 566 * 3, driver.execute_script('return window.outerHeight;') / 680 * 3)
]

pyautogui.moveTo(
	shapesBoundingBoxCoords[0][0] * driver.execute_script('return window.outerWidth;') * screenWidthRatio,
	shapesBoundingBoxCoords[0][1] * driver.execute_script('return window.outerHeight;') * outerHeightRatio
)

# Sleep until the document is ready.
while(not getPageState(driver)):
	time.sleep(0.050)

# Start the game!
driver.execute_script('game.state.start(\'play\')')

time.sleep(2)

# Test simple shape
shape0 = getSimpleShape(0)
print(shape0.startY)
pyautogui.moveTo(shape0.startX, shape0.startY)

# startX and startY are in availScreen coordinates space.
def convertToScreenCoordSpace(x = 0, y = 0):
	

	return x, y

dict_blocksPos = {
	2 : [abs_x + canvasSizeX - 50, abs_y + canvasSizeY + 30],
	1 : [abs_x + canvasSizeX - 210, abs_y + canvasSizeY + 30],
	3 : [abs_x + canvasSizeX + 140, abs_y + canvasSizeY + 30]
}

dict_mapPos = {
	0 : [abs_x + 160, abs_y + 160],
	1 : [abs_x + 215, abs_y + 153]
}

#pyautogui.moveTo(abs_x + getShape(1)["startX"], abs_y + getShape(1)["startY"])
#pyautogui.dragTo(dict_mapPos[0][0], dict_mapPos[0][1], button='left')

input()