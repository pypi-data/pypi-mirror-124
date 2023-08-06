from typing import TypeVar

from .EventContainer import EventContainer
from .BaseEvent import BaseEvent
from .FChat import FChat
from .FWrapper import FWrapper
from .FPlayer import FPlayer
from .FRequest import FRequest
from .FTime import FTime
from .FKeyBind import FKeyBind
from .FHud import FHud
from .FFS import FFS
from .FJsMacros import FJsMacros
from .FReflection import FReflection
from .FClient import FClient
from .FWorld import FWorld
from .FGlobalVars import FGlobalVars

File = TypeVar["java.io.File"]



Chat = FChat()
JavaWrapper = FWrapper()
Player = FPlayer()
Request = FRequest()
Time = FTime()
KeyBind = FKeyBind()
Hud = FHud()
FS = FFS()
JsMacros = FJsMacros()
Reflection = FReflection()
Client = FClient()
World = FWorld()
GlobalVars = FGlobalVars()
context = EventContainer()
file = File()
event = BaseEvent()
