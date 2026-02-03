from sqlalchemy.orm import Session

from app.ai.schemas import (
    AINegotiationInput,
    ProductContext,
    OfferContext,
    MessageContext,
    CustomerPurchaseHistory,
)

from app.models.negotiation import NegotiationSession
from app.models.offer import Offer
from app.models.message import ConversationMessage
from app.models.product import Product


MAX_MESSAGES_FOR_AI = 8


def build_ai_input(
    db: Session,
    session: NegotiationSession,
) -> AINegotiationInput:

    # 1️⃣ Product
    product = (
        db.query(Product)
        .filter(Product.id == session.product_id)
        .first()
    )

    if not product:
        raise ValueError("Product not found for negotiation session")

    # 🔢 Max discount %
    if product.base_price > 0:
        max_discount_percent = round(
            ((product.base_price - product.floor_price) / product.base_price) * 100,
            2,
        )
    else:
        max_discount_percent = 0.0

    # 2️⃣ Offers
    offers = (
        db.query(Offer)
        .filter(Offer.session_id == session.id)
        .order_by(Offer.created_at.asc())
        .all()
    )

    offers_ctx = [
        OfferContext(
            offered_price=o.offered_price,
            created_at=o.created_at,
        )
        for o in offers
    ]

    # 3️⃣ Messages (last N)
    messages = (
        db.query(ConversationMessage)
        .filter(ConversationMessage.negotiation_id == session.id)
        .order_by(ConversationMessage.created_at.desc())
        .limit(MAX_MESSAGES_FOR_AI)
        .all()
    )

    messages_ctx = [
        MessageContext(
            sender=m.sender,
            content=m.message,
            created_at=m.created_at,
        )
        for m in reversed(messages)
    ]

    # 4️⃣ Customer history (Phase-2 stub)
    customer_history = CustomerPurchaseHistory()

    # 5️⃣ Offer intelligence
    latest_offer = offers_ctx[-1].offered_price if offers_ctx else None
    best_offer = max((o.offered_price for o in offers_ctx), default=None)

    # 6️⃣ Final AI input
    return AINegotiationInput(
        session_id=session.id,
        customer_id=session.customer_id,
        product=ProductContext(
            product_id=product.id,
            name=product.name,
            category=product.category,
            unit=product.unit,                       # ✅ FIXED
            base_price=product.base_price,
            floor_price=product.floor_price,
            max_discount_percent=max_discount_percent,
            free_delivery=True,
        ),
        customer_history=customer_history,
        offers=offers_ctx,
        messages=messages_ctx,
        latest_offer=latest_offer,
        best_offer=best_offer,
        total_attempts=len(offers_ctx),
    )
