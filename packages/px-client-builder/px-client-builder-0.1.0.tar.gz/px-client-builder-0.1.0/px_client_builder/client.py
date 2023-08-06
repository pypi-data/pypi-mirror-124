from functools import cached_property
from typing import TypeVar, Generic, Type


__all__ = 'Client', 'NestedClient'


class Client:
    def __init__(self, *_, **kw):
        self.kw = kw


T = TypeVar('T', bound=Client)


class NestedClient(Generic[T], Client):
    root: T
    parent: T

    def __init__(self, *_, parent: T = None, **kw):
        assert parent is not None, 'Nested client must have a parent relation.'

        super().__init__(**kw)

        self.root = parent
        self.parent = parent

        if isinstance(parent, NestedClient) or hasattr(parent, 'root'):
            self.root = parent.root

    @classmethod
    def as_property(cls: Type[T], **kw) -> T:
        prop: T = cached_property(lambda self: cls(parent=self, **{**self.kw, **kw}))

        return prop
