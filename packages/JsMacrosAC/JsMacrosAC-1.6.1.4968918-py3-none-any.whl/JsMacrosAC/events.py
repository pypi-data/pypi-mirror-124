from typing import TypeVar

from .EventContainer import EventContainer
from .BaseEvent import BaseEvent
from .EventFallFlying import EventFallFlying
from .EventDisconnect import EventDisconnect
from .EventEXPChange import EventEXPChange
from .EventCustom import EventCustom
from .EventRecvMessage import EventRecvMessage
from .EventAirChange import EventAirChange
from .EventBlockUpdate import EventBlockUpdate
from .CodeCompileEvent import CodeCompileEvent
from .EventResourcePackLoaded import EventResourcePackLoaded
from .EventItemDamage import EventItemDamage
from .EventDimensionChange import EventDimensionChange
from .EventItemPickup import EventItemPickup
from .EventJoinedTick import EventJoinedTick
from .EventOpenScreen import EventOpenScreen
from .EventTitle import EventTitle
from .EventDeath import EventDeath
from .EventSignEdit import EventSignEdit
from .EventSendMessage import EventSendMessage
from .EventTick import EventTick
from .EventSound import EventSound
from .EventKey import EventKey
from .EventProfileLoad import EventProfileLoad
from .EventBossbar import EventBossbar
from .EventEntityLoad import EventEntityLoad
from .EventDamage import EventDamage
from .EventPlayerLeave import EventPlayerLeave
from .EventChunkLoad import EventChunkLoad
from .EventChunkUnload import EventChunkUnload
from .EventHungerChange import EventHungerChange
from .EventArmorChange import EventArmorChange
from .EventRiding import EventRiding
from .EventPlayerJoin import EventPlayerJoin
from .EventJoinServer import EventJoinServer
from .EventEntityUnload import EventEntityUnload
from .EventEntityDamaged import EventEntityDamaged
from .EventHeldItemChange import EventHeldItemChange

File = TypeVar["java.io.File"]

