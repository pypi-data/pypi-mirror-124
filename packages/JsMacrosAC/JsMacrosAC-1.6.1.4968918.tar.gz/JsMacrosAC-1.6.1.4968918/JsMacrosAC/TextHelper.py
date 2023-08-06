from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

Text = TypeVar["net.minecraft.text.Text"]

class TextHelper(BaseHelper):
	"""
	Since: 1.0.8 
	"""

	@overload
	def __init__(self, json: str) -> None:
		pass

	@overload
	def __init__(self, t: Text) -> None:
		pass

	@overload
	def replaceFromJson(self, json: str) -> "TextHelper":
		"""replace the text in this class with JSON data.\n
		Since: 1.0.8 

		Args:
			json: 
		"""
		pass

	@overload
	def replaceFromString(self, content: str) -> "TextHelper":
		"""replace the text in this class with String data.\n
		Since: 1.0.8 

		Args:
			content: 
		"""
		pass

	@overload
	def getJson(self) -> str:
		"""
		Since: 1.2.7 

		Returns:
			JSON data representation. 
		"""
		pass

	@overload
	def getString(self) -> str:
		"""
		Since: 1.2.7 

		Returns:
			the text content. 
		"""
		pass

	@overload
	def toJson(self) -> str:
		"""
		Since: 1.0.8 
		"""
		pass

	@overload
	def toString(self) -> str:
		"""
		Since: 1.0.8, this used to do the same as TextHelper#getString() 

		Returns:
			String representation of text helper. 
		"""
		pass

	pass


