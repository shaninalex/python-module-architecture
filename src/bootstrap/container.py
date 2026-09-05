from typing import Type, TypeVar, Union, Any

import punq

T = TypeVar("T")
K = TypeVar("K", bound=Union[Type[Any], str])


class Container:
    def __init__(self):
        self._impl = punq.Container()

    def register(self, key: K, *, instance: Any) -> None:
        """Register either a type or a string key"""
        self._impl.register(key, instance=instance)

    def resolve(self, key: K) -> Any:
        return self._impl.resolve(key)



