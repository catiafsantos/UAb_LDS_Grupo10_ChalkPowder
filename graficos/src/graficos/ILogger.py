from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def log_info(self, mensagem: str) -> None:
        pass

    @abstractmethod
    def log_erro(self, mensagem: str) -> None:
        pass