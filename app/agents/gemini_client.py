import os
import random
import re
import time
from typing import Optional

from google import genai
from google.genai import types

from app.config.config_loader import ConfigLoader


class GeminiClient:
    """
    Shared Gemini client for AISES.

    Features:
    - Reads GEMINI_API_KEY from the environment
    - Reads model settings from config.json
    - Automatically spaces requests to respect free-tier limits
    - Respects Gemini's recommended retry delay
    - Retries temporary network and quota errors
    - Requests JSON responses for AISES parsers
    """

    # Shared across all GeminiClient objects in the same AISES run.
    # This prevents Requirement Generator, Mapper and Evaluator
    # from sending requests too quickly.
    _last_request_time: float = 0.0

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        max_retries: int = 5,
    ) -> None:
        config = ConfigLoader()

        self.model = model or config.get(
            "gemini_model",
            "gemini-3.5-flash-lite",
        )

        self.temperature = float(
            config.get(
                "gemini_temperature",
                0.1,
            )
        )

        self.max_output_tokens = int(
            config.get(
                "gemini_max_output_tokens",
                4096,
            )
        )

        self.timeout_ms = int(
            config.get(
                "gemini_timeout_ms",
                300000,
            )
        )

        # Your free tier currently permits 5 requests/minute.
        # 13 seconds gives a small safety margin.
        self.min_request_interval = float(
            config.get(
                "gemini_min_request_interval_seconds",
                13.0,
            )
        )

        self.max_retries = max(
            1,
            int(max_retries),
        )

        resolved_api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
        )

        if not resolved_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Set it as an environment variable before "
                "running AISES."
            )

        self.client = genai.Client(
            api_key=resolved_api_key,
            http_options=types.HttpOptions(
                timeout=self.timeout_ms,
            ),
        )

    def ask(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response text.
        """

        if not isinstance(prompt, str):
            raise TypeError(
                "Prompt must be a string."
            )

        prompt = prompt.strip()

        if not prompt:
            raise ValueError(
                "Prompt must not be empty."
            )

        last_error: Optional[Exception] = None

        for attempt in range(
            1,
            self.max_retries + 1,
        ):
            try:
                self._wait_for_rate_limit()

                print(
                    f"Gemini request "
                    f"(attempt {attempt}/{self.max_retries}, "
                    f"model={self.model}, "
                    f"prompt={len(prompt):,} characters)"
                )

                # Save the request time immediately before
                # contacting Gemini.
                GeminiClient._last_request_time = (
                    time.monotonic()
                )

                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=self.temperature,
                            max_output_tokens=(
                                self.max_output_tokens
                            ),
                            response_mime_type=(
                                "application/json"
                            ),
                        ),
                    )
                )

                text = getattr(
                    response,
                    "text",
                    None,
                )

                if not text or not text.strip():
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return text.strip()

            except Exception as error:
                last_error = error
                error_text = str(error)

                print(
                    f"Gemini request failed on attempt "
                    f"{attempt}: {error}"
                )

                if attempt >= self.max_retries:
                    break

                server_retry_delay = (
                    self._extract_retry_delay(
                        error_text
                    )
                )

                if server_retry_delay is not None:
                    # Add a safety margin to Google's
                    # recommended retry time.
                    delay = server_retry_delay + 2.0
                else:
                    # Exponential backoff for DNS,
                    # connection and temporary server errors.
                    delay = min(
                        2 ** attempt,
                        60,
                    ) + random.uniform(0.0, 1.0)

                print(
                    f"Retrying in {delay:.1f} seconds..."
                )

                time.sleep(delay)

        raise RuntimeError(
            "Gemini request failed after "
            f"{self.max_retries} attempts: "
            f"{last_error}"
        )

    def _wait_for_rate_limit(self) -> None:
        """
        Keep requests separated by the configured minimum
        interval.
        """

        if self.min_request_interval <= 0:
            return

        elapsed = (
            time.monotonic()
            - GeminiClient._last_request_time
        )

        remaining = (
            self.min_request_interval
            - elapsed
        )

        if (
            GeminiClient._last_request_time > 0
            and remaining > 0
        ):
            print(
                f"Waiting {remaining:.1f} seconds "
                "to respect Gemini rate limits..."
            )

            time.sleep(remaining)

    @staticmethod
    def _extract_retry_delay(
        error_text: str,
    ) -> Optional[float]:
        """
        Extract Gemini's retry delay from errors such as:

        Please retry in 41.42s
        'retryDelay': '41s'
        "retryDelay": "41s"
        """

        patterns = [
            r"Please retry in\s+([\d.]+)s",
            r"'retryDelay':\s*'([\d.]+)s'",
            r'"retryDelay":\s*"([\d.]+)s"',
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                error_text,
                re.IGNORECASE,
            )

            if match:
                try:
                    return float(
                        match.group(1)
                    )
                except ValueError:
                    return None

        return None

    def close(self) -> None:
        """
        Close the SDK client when the installed SDK supports it.
        """

        close_method = getattr(
            self.client,
            "close",
            None,
        )

        if callable(close_method):
            close_method()