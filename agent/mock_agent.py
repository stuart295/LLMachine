from agent.base_agent import BaseAgent


class MockAgent(BaseAgent):

    def __init__(self, response_func=None):
        super().__init__()
        self.response_func = response_func


