import abc

class BaseAgent:

    def __init__(self, identifier: str):
        self.last_response = None
        self.id = identifier


    @abc.abstractmethod
    def tell(self, message: str):
        """Give this agent an input"""

    @abc.abstractmethod
    def listen(self) -> str:
        """Processes this agent for one step and returns the output"""
