from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMClient:
    def generate(self, system_prompt: str, messages: list[str]) -> str:
        chat = [{"role": "system", "content": system_prompt}]
        for m in messages:
            chat.append({"role": "user", "content": m})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat,
            temperature=0.6
        )

        return response.choices[0].message.content
