from typing import overload
from typing import TypeVar
from .BaseLibrary import BaseLibrary
from .TextHelper import TextHelper
from .TextBuilder import TextBuilder
from .CommandBuilder import CommandBuilder
from .ChatHistoryManager import ChatHistoryManager

Logger = TypeVar["org.apache.logging.log4j.Logger"]

class FChat(BaseLibrary):
	"""Functions for interacting with chat.

An instance of this class is passed to scripts as the 'Chat' variable.
	"""

	@overload
	def __init__(self) -> None:
		pass

	@overload
	def log(self, message: object) -> None:
		"""Log to player chat.\n
		Since: 1.1.3 

		Args:
			message: 
		"""
		pass

	@overload
	def log(self, message: object, await_: bool) -> None:
		"""

		Args:
			await: should wait for message to actually be sent to chat to continue. 
			message: 
		"""
		pass

	@overload
	def say(self, message: str) -> None:
		"""Say to server as player.\n
		Since: 1.0.0 

		Args:
			message: 
		"""
		pass

	@overload
	def say(self, message: str, await_: bool) -> None:
		"""Say to server as player.\n
		Since: 1.3.1 

		Args:
			await: 
			message: 
		"""
		pass

	@overload
	def title(self, title: object, subtitle: object, fadeIn: int, remain: int, fadeOut: int) -> None:
		"""Display a Title to the player.\n
		Since: 1.2.1 

		Args:
			fadeOut: 
			fadeIn: 
			remain: 
			subtitle: 
			title: 
		"""
		pass

	@overload
	def actionbar(self, text: object, tinted: bool) -> None:
		"""Display the smaller title that's above the actionbar.\n
		Since: 1.2.1 

		Args:
			tinted: 
			text: 
		"""
		pass

	@overload
	def toast(self, title: object, desc: object) -> None:
		"""Display a toast.\n
		Since: 1.2.5 

		Args:
			title: 
			desc: 
		"""
		pass

	@overload
	def createTextHelperFromString(self, content: str) -> TextHelper:
		"""Creates a TextHelper for use where you need one and not a string.\n
		Since: 1.1.3 

		Args:
			content: 

		Returns:
			a new TextHelper 
		"""
		pass

	@overload
	def getLogger(self) -> Logger:
		"""
		Since: 1.5.2 
		"""
		pass

	@overload
	def getLogger(self, name: str) -> Logger:
		"""returns a log4j logger, for logging to console only.\n
		Since: 1.5.2 

		Args:
			name: 
		"""
		pass

	@overload
	def createTextHelperFromJSON(self, json: str) -> TextHelper:
		"""Create a TextHelper for use where you need one and not a string.\n
		Since: 1.1.3 

		Args:
			json: 

		Returns:
			a new TextHelper 
		"""
		pass

	@overload
	def createTextBuilder(self) -> TextBuilder:
		"""
		Since: 1.3.0 

		Returns:
			a new builder 
		"""
		pass

	@overload
	def createCommandBuilder(self, name: str) -> CommandBuilder:
		"""
		Since: 1.4.2 

		Args:
			name: name of command 
		"""
		pass

	@overload
	def getHistory(self) -> ChatHistoryManager:
		pass

	pass


