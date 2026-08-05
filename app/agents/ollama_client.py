import ollama

from app.config.config_loader import ConfigLoader


class OllamaClient:

    def __init__(self):

        config = ConfigLoader()

        self.model = config.get("ollama_model")

    def ask(self, prompt: str):

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]