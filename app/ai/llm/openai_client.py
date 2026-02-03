import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_openai_llm(prompt: str) -> dict:
    """
    Calls OpenAI and returns STRICT JSON
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a negotiation AI. "
                    "You MUST respond ONLY in valid JSON with keys: "
                    "decision_type, counter_price, message_text, confidence_score."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content and response.choices[0].message.parsed
