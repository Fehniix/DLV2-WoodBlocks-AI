class Shape:
	def __init__(self, rawObj):
		# A shape is defined building up from a JS game object. `rawJSObject` contains all the shape's original info.
		self.rawJSObject = rawObj
	
	@property
	def startX(self):
		return self.rawJSObject['startX']

	@property
	def startY(self):
		return self.rawJSObject['startY']