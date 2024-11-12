import sys
from _typeshed import FileDescriptor, Unused, HasFileno
from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, NamedTuple, TypeVar

from typing_extensions import Self, TypeAlias, Generic

_EventMask: TypeAlias = int

T = TypeVar('T', bound=(HasFileno | int))

EVENT_READ: _EventMask
EVENT_WRITE: _EventMask


class SelectorKey(NamedTuple, Generic[T]):
    fileobj: T
    fd: FileDescriptor
    events: _EventMask
    data: Any


class BaseSelector(metaclass=ABCMeta):
    @abstractmethod
    def register(self, fileobj: T, events: _EventMask, data: Any = None) -> SelectorKey[T]: ...

    @abstractmethod
    def unregister(self, fileobj: T) -> SelectorKey[T]: ...

    def modify(self, fileobj: T, events: _EventMask, data: Any = None) -> SelectorKey[T]: ...

    @abstractmethod
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey[T], _EventMask]]: ...

    def close(self) -> None: ...

    def get_key(self, fileobj: T) -> SelectorKey[T]: ...

    @abstractmethod
    def get_map(self) -> Mapping[T, SelectorKey[T]]: ...

    def __enter__(self) -> Self: ...

    def __exit__(self, *args: Unused) -> None: ...


class _BaseSelectorImpl(BaseSelector, metaclass=ABCMeta):
    def register(self, fileobj: T, events: _EventMask, data: Any = None) -> SelectorKey[T]: ...

    def unregister(self, fileobj: T) -> SelectorKey[T]: ...

    def modify(self, fileobj: T, events: _EventMask, data: Any = None) -> SelectorKey[T]: ...

    def get_map(self) -> Mapping[T, SelectorKey[T]]: ...


class SelectSelector(_BaseSelectorImpl):
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey[T], _EventMask]]: ...


class _PollLikeSelector(_BaseSelectorImpl):
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey[T], _EventMask]]: ...


if sys.platform != "win32":
    class PollSelector(_PollLikeSelector): ...

if sys.platform == "linux":
    class EpollSelector(_PollLikeSelector):
        def fileno(self) -> int: ...


class DevpollSelector(_PollLikeSelector):
    def fileno(self) -> int: ...


if sys.platform != "win32":
    class KqueueSelector(_BaseSelectorImpl):
        def fileno(self) -> int: ...

        def select(self, timeout: float | None = None) -> list[tuple[SelectorKey[T], _EventMask]]: ...


# Not a real class at runtime, it is just a conditional alias to other real selectors.
# The runtime logic is more fine-grained than a `sys.platform` check;
# not really expressible in the stubs
class DefaultSelector(_BaseSelectorImpl):
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey[T], _EventMask]]: ...

    if sys.platform != "win32":
        def fileno(self) -> int: ...
