from typing import Generator, List, Dict
from openai import OpenAI, OpenAIError
from core.config import MODEL_NAME, TEMPERATURE


class PibotClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = MODEL_NAME
        self.temperature = TEMPERATURE

    def stream_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
    ) -> Generator[str, None, None]:
        """Streams response chunks from gpt-6-luna locked at temperature 1.0."""
        payload = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]} for m in messages
        ]

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=payload,
                temperature=self.temperature,  # Strictly locked at 1.0
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except OpenAIError as e:
            yield f"\n\n⚠️ **API Communication Error:** `{str(e)}`"
        except Exception as e:
            yield f"\n\n⚠️ **Unexpected System Error:** `{str(e)}`"
