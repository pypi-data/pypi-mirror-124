from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic

T = TypeVar("T")

class Mappings_MappedClass(Generic[T]):
	"""
	Since: 1.6.0 
	"""

	@overload
	def __init__(self, instance: T, tClass: Class) -> None:
		pass

	@overload
	def getFieldValue(self, fieldName: str) -> object:
		"""
		Since: 1.6.0 

		Args:
			fieldName: 
		"""
		pass

	@overload
	def getFieldValueAsClass(self, asClass: str, fieldName: str) -> object:
		"""
		Since: 1.6.0 

		Args:
			fieldName: 
			asClass: 
		"""
		pass

	@overload
	def setFieldValue(self, fieldName: str, fieldValue: object) -> None:
		"""
		Since: 1.6.0 

		Args:
			fieldName: 
			fieldValue: 
		"""
		pass

	@overload
	def setFieldValueAsClass(self, asClass: str, fieldName: str, fieldValue: object) -> None:
		"""
		Since: 1.6.0 

		Args:
			fieldName: 
			asClass: 
			fieldValue: 
		"""
		pass

	@overload
	def invokeMethod(self, methodNameOrSig: str, params: List[object]) -> object:
		"""
		Since: 1.6.0 

		Args:
			methodNameOrSig: 
			params: 
		"""
		pass

	@overload
	def invokeMethodAsClass(self, asClass: str, methodNameOrSig: str, params: List[object]) -> object:
		"""
		Since: 1.6.0 

		Args:
			methodNameOrSig: 
			asClass: 
			params: 
		"""
		pass

	pass


