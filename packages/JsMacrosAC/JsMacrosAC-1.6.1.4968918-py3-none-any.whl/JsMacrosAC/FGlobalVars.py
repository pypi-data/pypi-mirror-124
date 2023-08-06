from typing import overload
from typing import Mapping
from .BaseLibrary import BaseLibrary


class FGlobalVars(BaseLibrary):
	""""Global" variables for passing to other contexts.

An instance of this class is passed to scripts as the 'GlobalVars' variable.\n
	Since: 1.0.4 
	"""
	globalRaw: Mapping[str, object]

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def putInt(self, name: str, i: int) -> int:
		"""Put an Integer into the global variable space.\n
		Since: 1.0.4 

		Args:
			name: 
			i: 
		"""
		pass

	@overload
	def putString(self, name: str, str: str) -> str:
		"""put a String into the global variable space.\n
		Since: 1.0.4 

		Args:
			str: 
			name: 
		"""
		pass

	@overload
	def putDouble(self, name: str, d: float) -> float:
		"""put a Double into the global variable space.\n
		Since: 1.0.8 

		Args:
			d: 
			name: 
		"""
		pass

	@overload
	def putBoolean(self, name: str, b: bool) -> bool:
		"""put a Boolean into the global variable space.\n
		Since: 1.1.7 

		Args:
			b: 
			name: 
		"""
		pass

	@overload
	def putObject(self, name: str, o: object) -> object:
		"""put anything else into the global variable space.\n
		Since: 1.1.7 

		Args:
			name: 
			o: 
		"""
		pass

	@overload
	def getType(self, name: str) -> str:
		"""Returns the type of the defined item in the global variable space as a string.\n
		Since: 1.0.4 

		Args:
			name: 
		"""
		pass

	@overload
	def getInt(self, name: str) -> int:
		"""Gets an Integer from the global variable space.\n
		Since: 1.0.4 

		Args:
			name: 
		"""
		pass

	@overload
	def getString(self, name: str) -> str:
		"""Gets a String from the global variable space\n
		Since: 1.0.4 

		Args:
			name: 
		"""
		pass

	@overload
	def getDouble(self, name: str) -> float:
		"""Gets a Double from the global variable space.\n
		Since: 1.0.8 

		Args:
			name: 
		"""
		pass

	@overload
	def getBoolean(self, name: str) -> bool:
		"""Gets a Boolean from the global variable space.\n
		Since: 1.1.7 

		Args:
			name: 
		"""
		pass

	@overload
	def getObject(self, name: str) -> object:
		"""Gets an Object from the global variable space.\n
		Since: 1.1.7 

		Args:
			name: 
		"""
		pass

	@overload
	def remove(self, key: str) -> None:
		"""removes a key from the global varaible space.\n
		Since: 1.2.0 

		Args:
			key: 
		"""
		pass

	@overload
	def getRaw(self) -> Mapping[str, object]:
		pass

	pass


