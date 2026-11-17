from typing import Generator, List, Dict
from openai import OpenAI, OpenAIError


class PibotClient:
    def __init__(self, api_key: str, model: str = "gpt-6-luna"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def stream_response(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
    ) -> Generator[str, None, None]:
        """Streams response chunks from the OpenAI API."""
        payload = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]} for m in messages
        ]

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=payload,
                temperature=temperature,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except OpenAIError as e:
            yield f"\n\n⚠️ **OpenAI API Error:** `{str(e)}`"
        except Exception as e:
            yield f"\n\n⚠️ **Unexpected Error:** `{str(e)}`"
