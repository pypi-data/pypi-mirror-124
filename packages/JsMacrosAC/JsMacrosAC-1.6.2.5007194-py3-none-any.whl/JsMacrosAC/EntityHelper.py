from typing import overload
from typing import List
from typing import TypeVar
from typing import Generic
from .BaseHelper import BaseHelper
from .PositionCommon_Pos3D import PositionCommon_Pos3D
from .NBTElementHelper import NBTElementHelper

Entity = TypeVar["net.minecraft.entity.Entity"]
T = TypeVar("T")

class EntityHelper(Generic[T], BaseHelper):
	"""
	"""

	@overload
	def __init__(self, e: T) -> None:
		pass

	@overload
	def getPos(self) -> PositionCommon_Pos3D:
		"""

		Returns:
			entity position. 
		"""
		pass

	@overload
	def getX(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'x' value of the entity. 
		"""
		pass

	@overload
	def getY(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'y' value of the entity. 
		"""
		pass

	@overload
	def getZ(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'z' value of the entity. 
		"""
		pass

	@overload
	def getEyeHeight(self) -> float:
		"""
		Since: 1.2.8 

		Returns:
			the current eye height offset for the entitye. 
		"""
		pass

	@overload
	def getPitch(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'pitch' value of the entity. 
		"""
		pass

	@overload
	def getYaw(self) -> float:
		"""
		Since: 1.0.8 

		Returns:
			the 'yaw' value of the entity. 
		"""
		pass

	@overload
	def getName(self) -> str:
		"""

		Returns:
			the name of the entity. 
		"""
		pass

	@overload
	def getType(self) -> str:
		"""

		Returns:
			the type of the entity. 
		"""
		pass

	@overload
	def isGlowing(self) -> bool:
		"""
		Since: 1.1.9 

		Returns:
			if the entity has the glowing effect. 
		"""
		pass

	@overload
	def isInLava(self) -> bool:
		"""
		Since: 1.1.9 

		Returns:
			if the entity is in lava. 
		"""
		pass

	@overload
	def isOnFire(self) -> bool:
		"""
		Since: 1.1.9 

		Returns:
			if the entity is on fire. 
		"""
		pass

	@overload
	def getVehicle(self) -> "EntityHelper":
		"""
		Since: 1.1.8 [citation needed] 

		Returns:
			the vehicle of the entity. 
		"""
		pass

	@overload
	def getPassengers(self) -> List["EntityHelper"]:
		"""
		Since: 1.1.8 [citation needed] 

		Returns:
			the entity passengers. 
		"""
		pass

	@overload
	def getNBT(self) -> NBTElementHelper:
		"""
		Since: 1.2.8, was a String until 1.5.0 
		"""
		pass

	@overload
	def setGlowing(self, val: bool) -> "EntityHelper":
		"""Sets whether the entity is glowing.\n
		Since: 1.1.9 

		Args:
			val: 
		"""
		pass

	@overload
	def isAlive(self) -> bool:
		"""Checks if the entity is still alive.\n
		Since: 1.2.8 
		"""
		pass

	@overload
	def toString(self) -> str:
		pass

	@overload
	def create(self, e: Entity) -> "EntityHelper":
		pass

	pass


