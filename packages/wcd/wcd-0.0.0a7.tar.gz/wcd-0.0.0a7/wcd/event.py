import asyncio as aio
import os

from enum import IntEnum, auto
from typing import Callable, Awaitable, Union

if os.environ.get("WCD_TRACEMALLOC", None) == "1":
    from .trace import take_snapshot


class ConnectionMode(IntEnum):
    ONE_SHOT = 99
    KEEP_CONNECTED = 100


class DaemonEvent(IntEnum):
    LIST = auto()
    SET = auto()
    GET = auto()
    NEXT = auto()
    PREV = auto()
    TOGGLE_CYCLE = auto()
    TOGGLE_RANDOM = auto()
    SHUFFLE = auto()
    REFRESH = auto()


EventHandler = Callable[[aio.StreamReader, aio.StreamWriter], Awaitable[None]]
_events: list[list[EventHandler]] = [[] for _ in DaemonEvent]

def register_event(event_type: Union[DaemonEvent, int]) -> Callable[[EventHandler], EventHandler]:
    def decorator(func: EventHandler) -> EventHandler:
        _events[event_type - 1].append(func)
        return func
    return decorator


def fire_event(event_type: Union[DaemonEvent, int], r: aio.StreamReader, w: aio.StreamWriter) -> Awaitable:
    tasks = [event(r, w) for event in _events[event_type - 1]]
    if os.environ.get("WCD_TRACEMALLOC", None) == "1":
        take_snapshot()
    return aio.gather(*tasks)

