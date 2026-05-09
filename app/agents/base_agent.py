from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Base template for all Babo Claude agents.
    """
    name = "BaseAgent"
    weight = 1.0

    @abstractmethod
    async def analyze(self, symbol: str):
        """
        Abstract method for analysis.
        """
        pass
