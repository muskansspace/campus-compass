import json
from openai import OpenAI

from ai_engine.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    MODEL_ID,
)


class BedrockClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL
        )

    def generate(self, prompt):
        

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
                "error": str(e)
            }