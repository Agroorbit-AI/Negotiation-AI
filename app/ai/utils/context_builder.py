def build_ai_context(
    product,
    session,
    messages
) -> dict:
    last_customer_message = next(
        (m.message for m in reversed(messages) if m.sender == "customer"),
        ""
    )

    return {
        "product_name": product.name,
        "base_price": product.base_price,
        "floor_price": product.floor_price,
        "max_discount_percent": product.max_discount_percent,
        "unit": product.unit,
        "last_customer_message": last_customer_message,
    }
