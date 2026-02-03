from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db.session import get_db
from app.models.customer import Customer
from app.models.product import Product
from app.models.negotiation import NegotiationSession, SessionStatus
from app.schemas.web_session import WebSessionStartRequest, WebSessionStartResponse

router = APIRouter(
    prefix="/web/session",
    tags=["Web Sessions"]
)

@router.post("/start", response_model=WebSessionStartResponse, status_code=status.HTTP_201_CREATED)
def start_web_session(payload: WebSessionStartRequest, db: Session = Depends(get_db)):

    # 1. Find or create customer
    customer = (
        db.query(Customer)
        .filter(Customer.phone_number == payload.phone_number)
        .first()
    )

    if not customer:
        customer = Customer(
            id=uuid4(),
            name=payload.name,
            phone_number=payload.phone_number,
            language_preference=payload.language
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # 2. Validate product
    product = (
        db.query(Product)
        .filter(Product.id == payload.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # 3. Create negotiation session (NO offered_price)
    session = NegotiationSession(
        id=uuid4(),
        customer_id=customer.id,
        product_id=product.id,
        status=SessionStatus.active,
        channel="web"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return WebSessionStartResponse(
        session_id=session.id,
        customer_id=customer.id,
        product_id=product.id,
        status=session.status
    )
