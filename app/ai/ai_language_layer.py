# app/ai/ai_language_layer.py

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_message(
    decision: str,
    reasoning: dict,
    psychology: list,
    product_name: str,
    chat_history: list
):
    """
    Converts a deterministic decision into human language.
    OpenAI is NOT allowed to decide price.
    """

    system_prompt = f"""
You are an Indian B2B agro sales executive.
You negotiate naturally in Hindi, English, Marathi, Hinglish.
Product: {product_name}

Negotiation Rules:
- Decision: {decision}
- Target Price: {reasoning.get('target_price')}
- Floor Price: {reasoning.get('floor')}
- Psychology: {', '.join(psychology)}

If Decision is:
ASK → ask customer for price/quantity.
ACCEPT → agree and close deal.
COUNTER → propose target price.
REJECT → politely reject and give floor.

Never contradict the decision.
Never invent new prices.
Speak like a real human sales agent.
"""

    messages = [{"role": "system", "content": system_prompt}]

    for sender, msg in chat_history[-10:]:
        role = "user" if sender == "customer" else "assistant"
        messages.append({"role": role, "content": msg})

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6
    )

    return res.choices[0].message.content
