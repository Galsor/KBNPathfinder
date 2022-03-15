from abc import ABC, abstractmethod
from typing import Union


class BaseConstraint(ABC):

    @abstractmethod
    @property
    def completion_rate(self) -> float:
        ...

    @abstractmethod
    @property
    def value(self) -> Union[int, float]:
        ...
