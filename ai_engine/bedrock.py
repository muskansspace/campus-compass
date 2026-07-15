import json
from openai import OpenAI

from ai_engine.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    MODEL_ID,
)


class BedrockClient:
    """
    Handles communication with the AWS Bedrock
    OpenAI-compatible Responses API.
    """

    def __init__(self):
        """
        Initializes the Bedrock client using
        the configured API key and base URL.
        """

        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )

    def generate_text(self, prompt):
        """
        Sends a prompt to the configured model and returns the raw
        text response (no JSON parsing) — used for generating plain
        prose like the society info paragraph.
        """

        try:

            response = self.client.responses.create(
                model=MODEL_ID,
                input=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.output_text

        except Exception as e:
            print("Bedrock Error:", e)
            raise

    def generate(self, prompt):
        """
        Sends a prompt to the configured model
        and returns the generated JSON response.
        """

        try:

            response = self.client.responses.create(
                model=MODEL_ID,
                input=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return json.loads(response.output_text)

        except Exception as e:

            return {
                "error": f"Bedrock API Error: {str(e)}"
            }