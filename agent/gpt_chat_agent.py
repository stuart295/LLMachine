import os.path

from agent.base_agent import BaseAgent
import openai
import logging


class GptChatAgent(BaseAgent):

    _OPENAI_KEY_PATH = "./openai_key"

    def __init__(self, model="gpt-4"):
        super().__init__()
        self.model = model
        self.log = logging.Logger("GptChatAgent")
        self.set_api_key()
        self.messages = []

    def set_api_key(self):
        if openai.api_key:
            return

        if not os.path.exists(self._OPENAI_KEY_PATH):
            raise FileNotFoundError(f"{self._OPENAI_KEY_PATH} could not be found. Please create this file and add your OpenAI API key")

        with open(self._OPENAI_KEY_PATH) as f:
            openai.api_key = f.read().strip()

    def tell(self, message: str):
        """TODO"""

    def listen(self) -> str:
        """TODO"""
