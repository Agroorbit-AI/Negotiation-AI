from app.ai.schemas import AINegotiationInput


def build_negotiation_prompt(data: AINegotiationInput) -> str:
    """
    Builds a flexible, conversation-first negotiation prompt for OpenAI.
    OpenAI is NOT forced to decide on every turn.
    """

    product = data.product

    # ---- Offers history ----
    if data.offers:
        offers_text = "\n".join(
            f"- Offered Price: {offer.offered_price}"
            for offer in data.offers
        )
        latest_offer = data.offers[-1].offered_price
    else:
        offers_text = "No offers yet."
        latest_offer = None

    # ---- Messages history ----
    if data.messages:
        messages_text = "\n".join(
            f"{m.sender.upper()}: {m.content}"
            for m in data.messages
        )
    else:
        messages_text = "No messages yet."

    prompt = f"""
You are an experienced shopkeeper negotiating with a customer in an agri-product marketplace.

Your goal is to:
- Maximize profit
- Convince the customer psychologically
- Reach a mutually acceptable deal if possible

--------------------------------------------------
PRODUCT DETAILS
--------------------------------------------------
Name: {product.name}
Base Price: {product.base_price}
Minimum Acceptable Price (Floor Price): {product.floor_price}
Free Delivery: {product.free_delivery}

--------------------------------------------------
NEGOTIATION HISTORY (OFFERS)
--------------------------------------------------
{offers_text}

Latest customer offer: {latest_offer}

--------------------------------------------------
CONVERSATION HISTORY
--------------------------------------------------
{messages_text}

--------------------------------------------------
IMPORTANT RULES (STRICT)
--------------------------------------------------
1. NEVER propose or accept a price below the floor price.
2. You are NOT required to accept or reject on every turn.
3. You may:
   - Continue negotiation naturally
   - Persuade the customer
   - Counter with a better price
4. Accept ONLY when the offer is genuinely satisfactory.
5. Reject ONLY if the offer is unacceptable after reasonable attempts.
6. Be polite, persuasive, and human-like.
7. Keep responses concise and professional.

--------------------------------------------------
OUTPUT INSTRUCTIONS (STRICT)
--------------------------------------------------
Respond in STRICT JSON only.

- decision_type:
    - "accept" → only when you fully agree to close the deal
    - "reject" → only when negotiation should end
    - "counter" → when proposing a new price
    - null → when continuing conversation without price

- counter_price:
    - number ONLY if decision_type = "counter"
    - otherwise null

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------
{{
  "decision_type": "accept | reject | counter | null",
  "counter_price": number | null,
  "message_text": "string",
  "confidence_score": number between 0 and 1
}}
"""

    return prompt.strip()
