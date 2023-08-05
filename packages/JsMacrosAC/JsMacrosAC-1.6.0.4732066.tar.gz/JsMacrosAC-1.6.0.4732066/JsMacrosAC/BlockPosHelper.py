from typing import overload
from typing import TypeVar
from .BaseHelper import BaseHelper

BlockPos = TypeVar["net.minecraft.util.math.BlockPos"]

class BlockPosHelper(BaseHelper):
	"""
	Since: 1.2.6 
	"""

	@overload
	def __init__(self, b: BlockPos) -> None:
		pass

	@overload
	def getX(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			the 'x' value of the block. 
		"""
		pass

	@overload
	def getY(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			the 'y' value of the block. 
		"""
		pass

	@overload
	def getZ(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			the 'z' value of the block. 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	pass


