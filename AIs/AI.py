from abc import ABC, abstractmethod


class AI(ABC):
    @abstractmethod
    def response(self) -> str:
        pass
