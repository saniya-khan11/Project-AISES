from app.agents.ollama_client import OllamaClient


class BaseAgent:

    def __init__(self):

        self.client = OllamaClient()

    def ask(self, prompt):

        return self.client.ask(prompt)