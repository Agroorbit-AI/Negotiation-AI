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
    """
    Professional negotiation rules:

    - Never kill a deal just because of time.
    - Kill only if:
        * many turns
        * customer not improving
        * offer below economic floor
    """

    # -------------------------
    # 1. Dynamic target
    # -------------------------
    if input.last_price:
        target_price = max(input.ideal_price, input.last_price + 20)
    else:
        target_price = input.ideal_price

    # -------------------------
    # 2. Accept good deal
    # -------------------------
    if input.customer_offer >= target_price:
        return NegotiationDecision(
            decision="accept",
            counter_price=None,
            target_price=target_price,
            reason="Offer meets or exceeds target"
        )

    # -------------------------
    # 3. Smart rejection rule
    # -------------------------
    effective_floor = max(input.floor_price, input.cost_price)

    if (
        input.turn_count >= MAX_TURNS
        and input.last_price is not None
        and input.customer_offer <= input.last_price
        and input.customer_offer < effective_floor
    ):
        return NegotiationDecision(
            decision="reject",
            counter_price=None,
            target_price=target_price,
            reason="Too many rounds with no improvement and below viable price"
        )

    # -------------------------
    # 4. Counter strategy
    # -------------------------
    if input.turn_count <= 2:
        counter = target_price
    elif input.turn_count <= 5:
        counter = (target_price + effective_floor) / 2
    else:
        counter = effective_floor + 10

    return NegotiationDecision(
        decision="counter",
        counter_price=round(counter, 2),
        target_price=target_price,
        reason="Negotiation in progress"
    )
