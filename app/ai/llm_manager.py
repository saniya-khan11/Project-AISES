import time

from app.agents.ollama_client import OllamaClient
from app.ai.ai_response import AIResponse
from app.ai.response_parser import ResponseParser


class LLMManager:
    """
    Central manager for all LLM interactions.
    """

    def __init__(self):

        self.client = OllamaClient()
        self.parser = ResponseParser()

    def ask(self, prompt: str):

        response = AIResponse()

        start = time.time()

        try:

            # Ask Ollama
            raw = self.client.ask(prompt)

            # Parse JSON response
            parsed = self.parser.parse(raw)

            response.success = True
            response.raw_response = raw
            response.parsed_data = parsed

        except Exception as e:

            response.success = False
            response.errors.append(str(e))

        finally:

            response.execution_time = (
                time.time() - start
            )

        return response