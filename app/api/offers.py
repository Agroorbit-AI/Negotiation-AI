from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferCreate, OfferResponse

router = APIRouter(prefix="/offers", tags=["Offers"])


@router.post("/", response_model=OfferResponse)
def create_offer(payload: OfferCreate, db: Session = Depends(get_db)):
    offer = Offer(
        session_id=payload.session_id,
        customer_id=payload.customer_id,
        offered_price=payload.offered_price,
        price=payload.price,
        quantity=payload.quantity,
    )

    db.add(offer)
    db.commit()
    db.refresh(offer)

    return offer
