from agent.base_agent import BaseAgent


class MockAgent(BaseAgent):

    def __init__(self, response_func=None):
        super().__init__()
        self.response_func = response_func
        self.input = None

    def tell(self, message: str):
        self.input = message

    def listen(self) -> str:
        if self.response_func:
            self.last_response = self.response_func(self.input)
        else:
            self.last_response = "boop"

        return self.last_response



