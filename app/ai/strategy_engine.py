# app/ai/strategy_engine.py

import re

# -----------------------------
# NLP extractors (from your POC)
# -----------------------------

def extract_price(text: str):
    nums = re.findall(r"\d{2,6}", text)
    return float(nums[0]) if nums else None


def extract_qty(text: str):
    patterns = [
        r"(\d+)\s*(bag|bags|packet|packets|pkt|quintal|qtl|kg|kgs)",
        r"(\d+)\s*(pahije|chahiye|havi|lene|ghya)"
    ]
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            return float(m.group(1))
    return None


# -----------------------------
# Psychology layer
# -----------------------------

def psychology_tags(customer, product):
    tags = []

    if customer.get("segment") == "vip":
        tags.append("Relationship Leverage")

    if customer.get("risk") == "high":
        tags.append("Risk Protection")

    if product.get("stock_pressure") == "high":
        tags.append("Scarcity Pressure")

    return tags


# -----------------------------
# CORE NEGOTIATION ENGINE
# -----------------------------

def negotiate(customer, product, history, offer, qty):
    """
    This is your REAL AI.
    Deterministic.
    Controls money.
    """

    last_price = history.get("last_price", product["ideal_price"])
    last_qty = history.get("last_quantity", 0)

    # Target logic (your POC logic, improved)
    target = max(
        last_price + 2,
        product["floor_price"],
        product["cost"] + 5
    )

    if qty and qty > last_qty:
        target -= 1  # reward bulk

    reasoning = {
        "last_price": last_price,
        "last_qty": last_qty,
        "target_price": target,
        "floor": product["floor_price"],
        "cost": product["cost"],
        "expected_margin": target - product["cost"]
    }

    # Decision rules
    if offer is None:
        decision = "ASK"

    elif offer >= target:
        decision = "ACCEPT"

    elif offer >= product["floor_price"]:
        decision = "COUNTER"

    else:
        decision = "REJECT"

    return decision, reasoning
