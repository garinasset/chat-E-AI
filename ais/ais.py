from abc import ABC, abstractmethod


class AIS(ABC):
    @abstractmethod
    def response(self):
        pass
