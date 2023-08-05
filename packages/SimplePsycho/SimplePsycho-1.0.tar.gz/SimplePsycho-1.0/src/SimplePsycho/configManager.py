"""Config Manager

This module was designed to provide an easy-to-use structure
for accessing and maintaining configuration files for your
various projects.

This module contains the configObj class alongside Type enum,
it is recommended you import both for easy access.

"""

import json
from enum import Enum

class Type(Enum):
	NUMBER_INT = [int]
	NUMBER_FLOAT = [float]
	RANGE_INT = [int, int]
	RANGE_FLOAT = [float, float]
	STRING = [str]
	LIST = [list]
	FLEX_PARENT = [dict]
	PARENT = [dict]

	#Previous configManager used strings as value declarations, this was added so old codebases are still supported
	def convert(typeStr):
		typeStr = typeStr.lower().strip().split('-')
		while(len(typeStr) < 2):
			typeStr += [None]

		if typeStr[0] == "string":
			return Type.STRING
		elif typeStr[0] == "list":
			return Type.LIST
		elif typeStr[0] == "number":
			if typeStr[1] == "float":
				return Type.NUMBER_FLOAT
			else: 
				return Type.NUMBER_INT
		elif typeStr[0] == "range":
			if typeStr[1] == "float":
				return Type.RANGE_FLOAT
			else:
				return Type.RANGE_INT
		else:
			return None

'''
 configObj formats follow JSON formating, keys have an associated values with them.
 	- If a required config key is missing, configObj will add it to the file with the value 'null' to represent a missing property
 	- A ^ prefix on a key indicates that key's direct children are flexible, aka can take on various names
 	then, only required children will be checked

 Values: assign values based on type you would like to be submited:
 	- "list" for list; get() returns: []
 	- "range" for range; get() returns: (start, end)
 	- "string" for str
 	- "number" (NOT CURRENTLY SUPPORTED) TODO: Add num
 	
	For numerical values (num and range), you can add the extension -float to indicate decimal values.
	If no extension is given, int is assumed

 - When using the built in get function, it will automatically return the result in your desired type (see return types above)
'''
# Examples:
CONFIG_FORMAT = {
	"desired-traits": {
		"age": Type.RANGE_INT,
		"no-comorbidities": Type.LIST,
		"FIQ-score": Type.RANGE_INT,
		"no-dsm": Type.LIST,
		"selected-columns": Type.LIST
	},

	"^datasets": {
		"^bids_directory": {
			"subrange": {
				"runs": Type.RANGE_INT,
				"tasks": Type.LIST
			}
		}
	},

	"test": {
		"range": Type.RANGE_FLOAT,
		"float_num": Type.NUMBER_FLOAT,
		"int_num": Type.NUMBER_INT,
		"badrange": Type.RANGE_INT
	}
}
###################################################################
class configObj:
	"""
	A class used to represent a configuration file.

	Attributes
	----------
	jsonLoc : str
		Path string which points to the location of the json file.
	fileFormat : dict
		Configuration format dictionary. See Also: 
		https://wiki.uiowa.edu/display/scnlab/ConfigManager#ConfigManager-CreatingaConfigObject
	dataLoaded : dict
		Dictionary representation of json file, stored in memory for quick access to values.
	"""

	def __init__(self, jsonLoc, fileFormat, inputDict = None):
		"""
		Parameters
		----------
		jsonLoc : str
			Path string which points to the loation of the json file.
		fileFormat : dict
			Configurtation format dictionary. See Also:
			https://wiki.uiowa.edu/display/scnlab/ConfigManager#ConfigManager-CreatingaConfigObject
		inputDict : dict, default=None
			Input dictionary following file format with data already collected.
			Config object is built from this dictionary rather than existing .json
		
		Notes
		-----
		With specified jsonLoc, this will load in the config file.
		With specified inputDict, this will save the dictionary to config loc.
		"""

		self.jsonLoc = jsonLoc
		self.fileFormat = fileFormat
		self.dataLoaded = inputDict

		if self.jsonLoc != None:
			if inputDict != None:
				self.saveConfig()
			self.loadConfig()

	def loadConfig(self, jsonLoc = None):
		"""
		Loads in configuration file to memory.

		Parameters
		----------
		jsonLoc : str
			String path to .json file.
		"""

		if (jsonLoc != None):
			self.jsonLoc = jsonLoc

		print(f"Attempting to load file {self.jsonLoc}")
		with open(self.jsonLoc, 'r') as stream:
			self.dataLoaded = json.load(stream)
			if self.dataLoaded == None:
				self.dataLoaded = {}

			print("Repairing local dataset (Note: repair does not save repairs to disk, call saveConfig() after repair()")
			self.repair()
			self.saveConfig()

	###################################################################
	# Name: get
	# Inputs: keys - keys to index (in order)
	# Description: Takes an index location within the dictionary, returns its formatted value
	# 			   (read configObj documentation for type explanation)
	###################################################################
	def get(self, keys):
		"""
		Universal function for gathering data from a specific path
		in a configuration file.

		Parameters
		----------
		keys : str or list
			String path or list paths in order, keys of the json dictionary
			are represented as directories.

		Returns
		-------
		tuple or list or int or float
			Returns the value of the given path formatted appropriately
			in relation to what is defined by the configuration format.

		Notes
		-----
		- Paths to parents cannot return a value as their value is
		child directories.
		- Paths to FLEXIBLE parents can return a value as their children may
		necesitate indexing.

		Examples
		--------
		With the following config file:
		config.json:
		{
			'parent':
				'child': '0-2'
		}
		
		>>> yourConfigObj.get("parent/child")
		(0,2) - Returns the value properly formatted per config format spec (Type.RANGE_INT)
		"""

		keysList = self.__convertPath(keys) #Pass by value
		if self.checkExistence(keysList, self.dataLoaded, False):
			typeVal = self.__getType(keysList)

			actualValue = self.__getLocation(keysList)

			if actualValue == None or typeVal == None:
				return None
			else:
				if typeVal == dict:
					return dict
				elif len(typeVal.value) > 1:
					if typeVal == Type.RANGE_INT or typeVal == Type.RANGE_FLOAT:
						return self.convertRange(actualValue, varType=typeVal.value[1])
				else:
					return typeVal.value[0](actualValue)

		else:
			print("Key not found, if you believe this is incorrect try repairing the config file")

	def set(self, keys, value, saveChanges = True):
		"""
		Sets the value at a given path within the configuration file.

		Parameters
		----------
		keys : str or list
			String path or list paths in order, keys of the json dictionary
			are represented as directories.
		value : see config format
			Assuming value type matches that specified in config format, assigns this
			new value to the keys path in config.
		saveChanges : bool, Default=True
			When true, updated value is stored to .json file. 
			When False, only dictionary in memory is updated.

		Notes
		-----
		If path points to a flexible parent, value can be type dict.
		Afterwards, a repair will be run to ensure children within this dictionary
		align with format.
		"""

		keysList = self.__convertPath(keys)
		
		if self.checkExistence(keysList, self.dataLoaded, False):
			success = False
			expectedType = self.__getType(keysList)
			refDict = self.__getLocation(keysList[0:len(keysList)-1])
			
			if (expectedType == Type.FLEX_PARENT and type(value) == dict):
				refDict[keysList[-1]] = value
				self.repair()#fix any missing data in this dict
				success = True
			elif ((expectedType == Type.STRING and type(value) == str) or
				(expectedType == Type.LIST and type(value) == list) or
				(expectedType == Type.NUMBER_INT or expectedType == Type.NUMBER_FLOAT) and (type(value) == float or type(value) == int)):
					refDict[keysList[-1]] = expectedType.value[0](value)
					success = True
			elif ((expectedType == Type.RANGE_INT or expectedType == Type.RANGE_FLOAT) and type(value) == tuple):
					refDict[keysList[-1]] = self.createRangeStr(value, expectedType.value[1])
					success = True
			else:
				print(f"Unable to set value, mismatching expected value: {expectedType.value} and given value: {type(value)}")
			
			if saveChanges and success:
				self.saveConfig()

		else:
			print(f"ERROR: The config directory: {keys} does not exist, if you believe this is incorrect try repairing the config")

	def saveConfig(self, jsonLoc = None):
		"""
		Saves the configuration file to storage.

		Parameters
		----------
		jsonLoc : str, Default=None
			The string path in which the .json file will be saved.
			Only provide a value if you wish to override current .json location
			or if none has been provided yet.
		"""

		print("Attempting to save configObj")
		if (jsonLoc != None):
			self.jsonLoc = jsonLoc

		if (self.jsonLoc == None):
			print("No location given!")
			return

		with open(self.jsonLoc, 'w') as stream:
			dump = json.dump(self.dataLoaded, stream, indent=4, sort_keys=True)
			print("configObj Saved!")

	def repair(self, pastKeys=[]):
		"""
		Recursively iterates through a configuration file to ensure
		data and keys align with given config format.

		Parameters
		----------
		pastKeys : list, Default=[]
			Keeps track of past keys for recursion. Unless you have a reason to
			only repair a specific parent within the config file, you should leave default.

		Notes
		-----
		Missing keys and values are assigned None
		"""

		curDic = self.fileFormat
		if len(pastKeys) > 0:
			for key in pastKeys:
				curDic = curDic[key]

		if self.hasData():
			for key in curDic:
				if type(curDic[key]) == dict:
					self.repair(pastKeys+[key])
				else:
					self.checkExistence(pastKeys+[key], self.dataLoaded, True)

		else:
			print("Repair failed, no config file has been loaded. Use configObj.loadConfig() first")

	def checkExistence(self, keysRef, dataLoaded, repair=True, pastKeys=[]): #Checks if location currently exists, by default it will repair aka fix if location is missing
		"""
		Checks for existence of a path within configuration file.
		
		Parameters
		----------
		keysRef : str or list
			String or list path to location within configuration file.
			Follows file directory format.
		dataLoaded : dict
			For recursion, initial call should pass configObj.getDict()
		repair : bool, Default=True
			When true, if location doesn't exist it is added to config.
		pastKeys : list, Default=[]
			For recursion, leave default

		Returns
		-------
		bool
			True for existence of path, False if path did not exist
		"""

		keys = self.__convertPath(keysRef) #Pass by value
		if len(keys) == 0:
			return True #An empty key path returns true as this is the 'root' directory of the config file

		if keys[0][0] == '^': #Check if first remaining key is a flex parent
			keys[0] = keys[0][1:] #Remove its prefix
			if keys[0] in dataLoaded and dataLoaded[keys[0]] != None:
				if len(dataLoaded[keys[0]]) > 0:
					if keys[1][0] == '^': #Checks if next key is also flexible(This is important as we want checkExistence to remember this when we go into the scope of the key)
						keys[1] = list(dataLoaded[keys[0]].keys())
						for i in range(0,len(keys[1])):
							keys[1][i] = '^'+keys[1][i]
					else:
						keys[1] = list(dataLoaded[keys[0]].keys())
			else:
				keys = [keys[0]]
		
		if type(keys[0]) == list: #We know flex locations exists, otherwise we wouldn't have any
			for key in keys[0]:
				self.checkExistence([key]+keys[1:], dataLoaded, repair, pastKeys+[key])
		elif len(keys) == 1 and self.__isFlex(pastKeys):
			return True
		elif keys[0] in dataLoaded:
			if len(keys) == 1:
				return True
			if type(dataLoaded[keys[0]]) != dict:
				dataLoaded[keys[0]] = {}
			return self.checkExistence(keys[1:], dataLoaded[keys[0]], repair, pastKeys+[keys[0]])
		else:
			if repair:
				print(f"Missing {keys[0]}, repairing file and filling default value.")
				if (len(keys) == 1):
					dataLoaded[keys[0]] = None
					return False
				else:
					dataLoaded[keys[0]] = {}
					self.checkExistence(keys[1:], dataLoaded[keys[0]], repair, pastKeys+[keys[0]])
					return False
			else:
				print(f"Missing {keys[0]}, repair is {str(repair)}, no change will be made.")
				return False

	def convertRange(self, rangeStr, varType=int):
		"""
		Takes a range string from configuration file and returns
		the range tuple equivalent.

		Parameters
		----------
		rangeStr : str
			A string representing a range in configuration file.
			 "start-end" or "<num" or "num<"
		varType : type, Default=int
			Whether type of range is int (Type.RANGE_INT) or float (Type.RANGE_FLOAT)

		Returns
		-------
		tuple
			Formatted (start value, end value) where start/end=None
			represents -/+ infinity.

		See Also
		--------
		createRangeStr : Takes range tuple and produces range string
		"""

		startNum = None
		endNum = None

		if rangeStr != None:
			rangeStr = rangeStr.strip()
			if '-' in rangeStr:
				splitStr = rangeStr.split('-')
				#catch ValueError, incase they don't type a valid number
				if splitStr[0].strip() != '*':
					try:
						startNum = varType(float(splitStr[0]))
					except ValueError:
						print(f"{splitStr[0]} is not a valid integer, using default value *.")
				if splitStr[1].strip() != '*':
					try:
						endNum = varType(float(splitStr[1]))
					except ValueError:
						print(f"{splitStr[1]} is not a valid integer, using default value *.")
			elif rangeStr[0] == '<': #Less than num
				try:
					endNum = varType(float(rangeStr[1:]))
				except ValueError:
					print(f"{rangeStr[1:]} is not a valid integer, using default value *.")
			elif rangeStr[-1] == '<': #Greater than num
				try:
					startNum = varType(float(rangeStr[:len(rangeStr)-1]))
				except ValueError:
					print(f"{rangeStr[:len(rangeStr)-1]} is not a valid integer, using default value *.")

		return (startNum, endNum)

	def createRangeStr(self, rangeTup, typeVal=int):
		"""
		Produces range string from range tuple.
		
		Parameters
		----------
		rangeTup : tuple
			Range tuple (start number, end number) where start/end=None
			represents -/+ infinity.
		varType : type, Default=int
			Whether type of range is int (Type.RANGE_INT) or float (Type.RANGE_FLOAT)

		Returns
		-------
		str
			Range string represented "start-end" where start/end='*' 
			represents -/+ infinity.

		See Also
		--------
		convertRange : Takes range string and produces range tuple
		"""

		start = rangeTup[0]
		end = rangeTup[1]
		if start == None:
			start = '*'
		else:
			start = str(typeVal(start))

		if end == None:
			end = '*'
		else:
			end = str(typeVal(end))

		return f"{start}-{end}"

	def hasData(self):
		"""
		Returns true if data has been loaded to memory.
		
		See Also
		--------
		loadConfig() : loads in configuration file to memory
		"""
		return (self.dataLoaded != None)

	def getDict(self):
		"""Dict - Returns the configuration object stored in memory"""
		return self.dataLoaded

	#PRIVATE:
	#Returns expected type of input for a given path in config, [yupe]
	def __getType(self, keysRef):
		keys = self.__convertPath(keysRef) #Pass by value

		if not self.hasData or not self.checkExistence(keys, self.dataLoaded, False):
			print("Location doesn't exist or data has not been loaded yet. Try running 'repair()'")
			return None

		typeVal = self.fileFormat
		pastParentFlex = False
		while len(keys) > 0:
			key = keys.pop(0)
			if key in typeVal:
				typeVal = typeVal[key]
				pastParentFlex = False
			elif '^'+key in typeVal:
				typeVal = typeVal['^'+key]
				pastParentFlex = True
			elif len(keys) == 0 and pastParentFlex:
				typeVal == Type.FLEX_PARENT

		if type(typeVal) == dict:
			return Type.PARENT
		else:
			if type(typeVal) == str:
				typeVal = Type.convert(typeVal)

			return typeVal

	#Takes a path within a config file "root/configchild/configchild" and returns ["root", "configchild", "configchild"]
	def __convertPath(self, pathStr):
		if type(pathStr) == str:
			return pathStr.strip("/ ").split("/") #Remove leading and trailing /, then split by /
		elif type(pathStr) == list:
			return list(pathStr)
		else:
			print(f"Attempted to convertPath of {type(pathStr)}, convertPath requires a string or list!")
			return None

	#Checks if given REAL config path is a flex parent
	def __isFlex(self, pathStr):
		keys = self.__convertPath(pathStr)

		refFormat = self.fileFormat
		for key in keys:
			if key == keys[-1]: #We have reached the final key:
				if ('^'+key) in refFormat:
					return True
			else:
				if key in refFormat:
					refFormat = refFormat[key]
				elif ('^'+key) in refFormat:
					refFormat = refFormat['^'+key]

		return False

	################################################################
	# NAME: getLocation
	# Input: keys- dictionary key path to follow, in order
	# Output: dictionary containing children of final keys index
	# Description: Grabs the sub dictionary of a given key list
	################################################################
	def __getLocation(self, keys):
		if not self.hasData or not self.checkExistence(keys, self.dataLoaded, False):
			print("Location doesn't exist or data has not been loaded yet. Try running 'repair()'")
			return None

		curDic = self.dataLoaded
		if len(keys) > 0:
			for key in keys:
				curDic = curDic[key]

		return curDic


##################################################
# TESTING:
##################################################
def testsForLoadedConfig():
	newCfgObj = configObj("sampleconfig.json", CONFIG_FORMAT)

	print(newCfgObj.get(["desired-traits","age"]))
	print(newCfgObj.get(["desired-traits", "no-comorbidities"]))
	print(newCfgObj.get("desired-traits/selected-columns"))
	print(newCfgObj.getDict())
	print(newCfgObj.get("test/range"))
	print(newCfgObj.get("test/badrange"))

	#Expect errors:
	print(newCfgObj.get(["desired-traits", "doesn'texist"]))
	print(newCfgObj.get(["desired-traits"]))

	newCfgObj.set('desired-traits/ages', "error") #Should error
	newCfgObj.set('desired-traits/age', (10.1, 12.1))
	newCfgObj.set('desired-traits/age', (10, None))
	print(newCfgObj.get('desired-traits/age'))
	newCfgObj.set('desired-traits/selected-columns', ["yo", "here", "bye"])

def testsForDictConfig():
	"""Function designed to test config manager with input dictionaries"""

	testDict = {
		"desired-traits": {
			"age": '10-20',
			"selected-columns": ["this", "is", "columns"]
		},
		"datasets": {
			"dir1": {
				"10-20": {
					"runs": "1-3"
				}
			}
		}
	}

	testConfig = configObj("configFromDict.json", CONFIG_FORMAT, testDict)

	otherBidsDir = {
		"40-50": {
			"tasks": ["task1", "2", "3"]
		}
	}
	testConfig.set("datasets/dir2", otherBidsDir)


#TODO: Use enum class for types rather than strings
if __name__ == "__main__":
	#Simple Demo for testing
	print("Testing configObj from loaded config:")
	testsForLoadedConfig()
	print("----------------------------------------")
	print("Testing configObj from dictionary")
	testsForDictConfig()