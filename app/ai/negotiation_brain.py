from dataclasses import dataclass

MAX_TURNS = 6


@dataclass
class NegotiationInput:
    cost_price: float
    ideal_price: float
    floor_price: float
    last_price: float | None
    turn_count: int
    customer_offer: float


@dataclass
class NegotiationDecision:
    decision: str  # accept / counter / reject
    counter_price: float | None
    target_price: float
    reason: str


def decide_negotiation(input: NegotiationInput) -> NegotiationDecision:

    has_price = input.customer_offer is not None
    has_quantity = input.quantity is not None

    if not has_price and not has_quantity:
        return NegotiationDecision("ask_both", None, None, "Missing price and quantity")

    if not has_quantity:
        return NegotiationDecision("ask_quantity", None, None, "Missing quantity")

    if not has_price:
        return NegotiationDecision("ask_price", None, None, "Missing price")

    effective_floor = max(input.floor_price, input.cost_price)

    if input.last_price:
        target_price = max(input.ideal_price, input.last_price + 20)
    else:
        target_price = input.ideal_price

    if input.quantity >= 100:
        target_price -= 50
    elif input.quantity >= 50:
        target_price -= 25

    if target_price < effective_floor + 100:
        target_price = effective_floor + 100

    if input.customer_offer >= target_price:
        return NegotiationDecision("accept", None, target_price, "Good deal")

    if (
        input.turn_count >= MAX_TURNS
        and input.customer_offer < effective_floor
    ):
        return NegotiationDecision("reject", None, effective_floor, "Below viable price")

    if input.turn_count <= 2:
        counter = target_price
    elif input.turn_count <= 4:
        counter = max(
            (target_price + input.customer_offer) / 2,
            effective_floor + 50
        )
    else:
        counter = effective_floor + 30

    if counter < effective_floor:
        counter = effective_floor

    return NegotiationDecision(
        "counter",
        round(counter, 2),
        round(target_price, 2),
        "Negotiation in progress"
    )
