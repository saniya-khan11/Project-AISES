import os
from google import genai


def main() -> None:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY was not found. "
            "Set the environment variable and reopen the terminal."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "Return only valid JSON with status set to working "
            "and model set to gemini-2.5-flash."
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    print(response.text)


if __name__ == "__main__":
    main()