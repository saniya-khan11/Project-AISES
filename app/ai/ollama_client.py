import requests


class OllamaClient:
    """
    Lightweight client for communicating with a local Ollama server.
    """

    def __init__(
        self,
        model="llama3.1:8b",
        host="http://localhost:11434",
        timeout=300,
    ):
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    # ==========================================================
    # Generate Response
    # ==========================================================

    def generate(self, prompt):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:

            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            return data.get("response", "").strip()

        except requests.exceptions.ConnectionError:

            raise RuntimeError(
                "Unable to connect to Ollama. "
                "Ensure Ollama is running (ollama serve)."
            )

        except requests.exceptions.Timeout:

            raise RuntimeError(
                "Ollama request timed out."
            )

        except requests.exceptions.RequestException as ex:

            raise RuntimeError(
                f"Ollama request failed: {ex}"
            )