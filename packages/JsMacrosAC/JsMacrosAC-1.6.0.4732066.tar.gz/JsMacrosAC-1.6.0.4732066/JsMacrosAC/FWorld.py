from typing import overload
from typing import List
from typing import Mapping
from .BaseLibrary import BaseLibrary
from .PlayerEntityHelper import PlayerEntityHelper
from .PlayerListEntryHelper import PlayerListEntryHelper
from .BlockDataHelper import BlockDataHelper
from .ScoreboardsHelper import ScoreboardsHelper
from .EntityHelper import EntityHelper
from .BlockPosHelper import BlockPosHelper
from .BossBarHelper import BossBarHelper
from .TextHelper import TextHelper


class FWorld(BaseLibrary):
	"""Functions for getting and using world data.

An instance of this class is passed to scripts as the 'World' variable.
	"""
	serverInstantTPS: float
	server1MAverageTPS: float
	server5MAverageTPS: float
	server15MAverageTPS: float

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def isWorldLoaded(self) -> bool:
		"""returns whether a world is currently loaded\n
		Since: 1.3.0 
		"""
		pass

	@overload
	def getLoadedPlayers(self) -> List[PlayerEntityHelper]:
		"""

		Returns:
			players within render distance. 
		"""
		pass

	@overload
	def getPlayers(self) -> List[PlayerListEntryHelper]:
		"""

		Returns:
			players on the tablist. 
		"""
		pass

	@overload
	def getBlock(self, x: int, y: int, z: int) -> BlockDataHelper:
		"""

		Args:
			x: 
			y: 
			z: 

		Returns:
			The block at that position. 
		"""
		pass

	@overload
	def getScoreboards(self) -> ScoreboardsHelper:
		"""
		Since: 1.2.9 

		Returns:
			a helper for the scoreboards provided to the client. 
		"""
		pass

	@overload
	def getEntities(self) -> List[EntityHelper]:
		"""

		Returns:
			all entities in the render distance. 
		"""
		pass

	@overload
	def getDimension(self) -> str:
		"""
		Since: 1.1.2 

		Returns:
			the current dimension. 
		"""
		pass

	@overload
	def getBiome(self) -> str:
		"""
		Since: 1.1.5 

		Returns:
			the current biome. 
		"""
		pass

	@overload
	def getTime(self) -> float:
		"""
		Since: 1.1.5 

		Returns:
			the current world time. 
		"""
		pass

	@overload
	def getTimeOfDay(self) -> float:
		"""This is supposed to be time of day, but it appears to be the same as FWorld#getTime() to me...\n
		Since: 1.1.5 

		Returns:
			the current world time of day. 
		"""
		pass

	@overload
	def getRespawnPos(self) -> BlockPosHelper:
		"""
		Since: 1.2.6 

		Returns:
			respawn position. 
		"""
		pass

	@overload
	def getDifficulty(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			world difficulty as an Integer . 
		"""
		pass

	@overload
	def getMoonPhase(self) -> int:
		"""
		Since: 1.2.6 

		Returns:
			moon phase as an Integer . 
		"""
		pass

	@overload
	def getSkyLight(self, x: int, y: int, z: int) -> int:
		"""
		Since: 1.1.2 

		Args:
			x: 
			y: 
			z: 

		Returns:
			sky light as an Integer . 
		"""
		pass

	@overload
	def getBlockLight(self, x: int, y: int, z: int) -> int:
		"""
		Since: 1.1.2 

		Args:
			x: 
			y: 
			z: 

		Returns:
			block light as an Integer . 
		"""
		pass

	@overload
	def playSoundFile(self, file: str, volume: float) -> Clip:
		"""plays a sound file using javax's sound stuff.\n
		Since: 1.1.7 

		Args:
			volume: 
			file: 
		"""
		pass

	@overload
	def playSound(self, id: str) -> None:
		"""
		Since: 1.1.7 

		Args:
			id: 
		"""
		pass

	@overload
	def playSound(self, id: str, volume: float) -> None:
		"""
		Since: 1.1.7 

		Args:
			volume: 
			id: 
		"""
		pass

	@overload
	def playSound(self, id: str, volume: float, pitch: float) -> None:
		"""
		Since: 1.1.7 

		Args:
			volume: 
			id: 
			pitch: 
		"""
		pass

	@overload
	def playSound(self, id: str, volume: float, pitch: float, x: float, y: float, z: float) -> None:
		"""plays a minecraft sound using the internal system.\n
		Since: 1.1.7 

		Args:
			volume: 
			x: 
			y: 
			z: 
			id: 
			pitch: 
		"""
		pass

	@overload
	def getBossBars(self) -> Mapping[str, BossBarHelper]:
		"""
		Since: 1.2.1 

		Returns:
			a map of boss bars by the boss bar's UUID. 
		"""
		pass

	@overload
	def isChunkLoaded(self, chunkX: int, chunkZ: int) -> bool:
		"""Check whether a chunk is within the render distance and loaded.\n
		Since: 1.2.2 

		Args:
			chunkX: 
			chunkZ: 
		"""
		pass

	@overload
	def getCurrentServerAddress(self) -> str:
		"""
		Since: 1.2.2 

		Returns:
			the current server address as a string ( 'server.address/server.ip:port' ). 
		"""
		pass

	@overload
	def getBiomeAt(self, x: int, z: int) -> str:
		"""
		Since: 1.2.2 [Citation Needed] 

		Args:
			x: 
			z: 

		Returns:
			biome at specified location, only works if the block/chunk is loaded. 
		"""
		pass

	@overload
	def getServerTPS(self) -> str:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps with various timings. 
		"""
		pass

	@overload
	def getTabListHeader(self) -> TextHelper:
		"""
		Since: 1.3.1 

		Returns:
			text helper for the top part of the tab list (above the players) 
		"""
		pass

	@overload
	def getTabListFooter(self) -> TextHelper:
		"""
		Since: 1.3.1 

		Returns:
			text helper for the bottom part of the tab list (below the players) 
		"""
		pass

	@overload
	def getServerInstantTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps. 
		"""
		pass

	@overload
	def getServer1MAverageTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps over the previous 1 minute average. 
		"""
		pass

	@overload
	def getServer5MAverageTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps over the previous 5 minute average. 
		"""
		pass

	@overload
	def getServer15MAverageTPS(self) -> float:
		"""
		Since: 1.2.7 

		Returns:
			best attempt to measure and give the server tps over the previous 15 minute average. 
		"""
		pass

	pass


