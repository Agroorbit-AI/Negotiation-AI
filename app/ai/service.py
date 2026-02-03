from app.ai.llm import LLMClient
from app.ai.strategy import NegotiationStrategy
from app.ai.governance import AIGovernance

class AIDecision:
    def __init__(self, decision_type, message_text, counter_price=None):
        self.decision_type = decision_type
        self.message_text = message_text
        self.counter_price = counter_price


class AINegotiationService:

    def __init__(self):
        self.llm = LLMClient()
        self.strategy = NegotiationStrategy()
        self.gov = AIGovernance()

    def decide(self, ai_input):
        session = ai_input["session"]
        product = ai_input["product"]
        customer = ai_input["customer"]
        history = ai_input["history"]
        messages = ai_input["messages"]

        ok, error = self.gov.validate(session, messages[-1])
        if not ok:
            return AIDecision("reject", error)

        offer_price = ai_input.get("offer_price")

        decision, price = self.strategy.decide_price(
            product, customer, history, offer_price
        )

        system_prompt = f"""
You are an Indian B2B agro sales executive.
Product: {product.name}
Base price: {product.base_price}
Floor price: {product.floor_price}
Decision: {decision}
Target/Counter price: {price}
Respond naturally in Hinglish.
"""

        reply = self.llm.generate(system_prompt, messages)

        return AIDecision(decision, reply, price)
