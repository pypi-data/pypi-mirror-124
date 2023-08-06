"""Dhor"""
from __future__ import annotations
from typing import Any, Optional, Iterable
from copy import deepcopy

__all__ = ["Dhor"]


class Dhor:
    def __new__(self):
        raise NotImplementedError

    def __init__(self):
        """Initializes the instance of the class after it is created. Should never have a return value"""
        self.storage = {}

    def __repr__(self) -> str:
        """Default representation of the object as a string"""
        return "I am dhor"

    def __str__(self) -> str:
        """Creates a string representation of the class"""
        return self.__repr__()

    def __setitem__(self, index, val):
        """Set indices on the object"""
        self.storage[index] = val

    def __getitem__(self, index) -> Any:
        """Get value of index on the object"""
        return self.storage[index]

    def __delitem__(self, index):
        """Delete kvp of index on the object"""
        del self.storage[index]

    def __len__(self):
        """Return length of object storage"""
        return len(self.storage)

    def __contain__(self, index) -> bool:
        """Implements the in operator"""
        return index in self.storage

    def __add__(self, other: Dhor):
        """Implements the + operator"""
        dhor_clone = deepcopy(self)
        dhor_clone.storage = {**self.storage, **other.storage}
        return dhor_clone

    def __iadd__(self, other: Dhor):
        """Implements the += operator"""
        self.storage.update(other.storage)

    def __sub__(self, other: Dhor):  # ( - )
        """Implements the - operator"""
        dhor_clone = deepcopy(self)
        dhor_clone.storage = {
            key: other.storage[key] for key in other.storage if key not in self.storage
        }
        return dhor_clone

    def __isub__(self, other: Dhor):  # ( -= )
        """Implements the -= operator"""
        for key in other.storage:
            if key in self.storage:
                self.storage.__delitem__(key)

    def __mul__(self, other: Dhor):  # ( * )
        """Implements the * operator"""
        self.__add__(other)

    def __imul__(self, other: Dhor):  # ( *= )
        """Implements the *= operator"""
        self.__iadd__(other)

    def __truediv__(self, other: Dhor):  # ( \ )
        """Implements the \ operator"""
        self.__sub__(other)

    def __itruediv__(self, other: Dhor):  # ( \= )
        """Implements the \= operator"""
        self.__isub__(other)

    def __floordiv__(self, other: Dhor):  # ( \\ )
        r"""Implements the \\ operator"""
        self.__sub__(other)

    def __ifloordiv__(self, other: Dhor):  # ( \= )
        r"""Implements the \= operator"""
        self.__isub__(other)

    def __call__(self, storage: Optional[dict] = None) -> dict:
        """Implements function to be called when object is called as function"""
        if storage:
            assert isinstance(storage, dict), "Storage provided should be a dict"
            self.storage = storage
        return self.storage

    def __enter__(self) -> dict:
        """Initialization when used as a context manager"""
        return self.storage

    def __exit__(self):
        """Cleanup when used as a context manager"""
        self.storage = {}

    def __delattr__(self, name: str) -> None:
        raise NotImplementedError

    def __dir__(self) -> Iterable[str]:
        raise NotImplementedError

    def __format__(self, format_spec: str) -> str:
        raise NotImplementedError

    def __eq__(self, other: Dhor) -> bool:
        """Check for equality of two Dhor instances"""
        assert isinstance(
            other, Dhor
        ), "Comparison object should be an instance of Dhor as well!"
        return all(other.storage[key] == value for key, value in self.storage.items())

    def __ne__(self, other: Dhor) -> bool:
        """Check for equality of two Dhor instances"""
        return not self.__eq__(other)

    def __getattribute__(self, name: str) -> Any:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __init_subclass__(cls) -> None:
        raise NotImplementedError

    def __instancecheck__(self, instance: Any) -> bool:
        raise NotImplementedError
