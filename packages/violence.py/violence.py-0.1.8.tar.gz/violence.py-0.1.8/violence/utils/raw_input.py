__version__ = "0.1.4"


def __convertio__(type, data):
	if type == int:
		try:    
			data = int(data)
		except: 
			pass
	if type == float:
		try:    
			data = float(data)
		except: 
			pass
	if type == bool:
		try:    
			data = bool(data)
		except: 
			pass
	if type == str:
		try:    
			data = str(data)
		except: 
			pass

	return data

def raw_input(type: type
	, string: str, on_error: str = None,
	cyclic: bool = False, ignore = False):

	data   = input(string)
	action = True

	data = __convertio__(type, data)

	if isinstance(data, type) != True:
		if on_error != None:
			print(on_error)

		if cyclic == True:
			while action:
				data = input(string)

				data = __convertio__(type, data)

				if isinstance(data, type):
					action = False
					
				if action == True: print(on_error)

			return type(data)
		else:
			if ignore == True:
				return str(data)

			return None 
	else:
		if type == float:
			data = type(data)

			if round(data) == data:
				return round(data)
				

		return type(data)
