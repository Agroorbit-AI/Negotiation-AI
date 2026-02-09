from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import re

from app.db.session import get_db
from app.models.message import ConversationMessage
from app.models.negotiation import NegotiationSession, SessionStatus
from app.models.offer import Offer
from app.schemas.message import MessageCreate, MessageResponse

from app.ai.negotiation_brain import decide_negotiation, NegotiationInput
from app.ai.ai_language_layer import generate_ai_message

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

def extract_offer(text: str):
    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    if not numbers:
        return None
    return float(numbers[0])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):

    session = (
        db.query(NegotiationSession)
        .filter(NegotiationSession.id == payload.session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Negotiation session not found"
        )

    if session.status in [SessionStatus.completed, SessionStatus.cancelled]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Negotiation session is already closed"
        )

    # Save CUSTOMER message
    customer_message = ConversationMessage(
        negotiation_id=session.id,
        sender=payload.sender.lower(),
        message=payload.message
    )
    db.add(customer_message)
    db.commit()
    db.refresh(customer_message)

    # Trigger AI only for customer
    if payload.sender.lower() == "customer":

        product = session.product
        customer_offer = extract_offer(payload.message)

        # No offer
        if customer_offer is None:
            ai_text = "Thanks for your interest. Could you please share your expected price so I can check what’s possible?"

            ai_message = ConversationMessage(
                negotiation_id=session.id,
                sender="ai",
                message=ai_text
            )
            db.add(ai_message)
            db.commit()
            db.refresh(ai_message)

            # ✅ RETURN AI MESSAGE
            return MessageResponse(
                id=ai_message.id,
                session_id=ai_message.negotiation_id,
                sender=ai_message.sender,
                message=ai_message.message,
                created_at=ai_message.created_at
            )

        last_offer = (
            db.query(Offer)
            .filter(Offer.session_id == session.id)
            .order_by(Offer.created_at.desc())
            .first()
        )

        last_price = float(last_offer.price) if last_offer else None

        turn_count = (
            db.query(ConversationMessage)
            .filter(ConversationMessage.negotiation_id == session.id)
            .filter(ConversationMessage.sender == "customer")
            .count()
        )

        brain_input = NegotiationInput(
            cost_price=product.base_price * 0.8,
            ideal_price=product.base_price,
            floor_price=product.floor_price,
            last_price=last_price,
            turn_count=turn_count,
            customer_offer=customer_offer
        )

        decision_obj = decide_negotiation(brain_input)

        past_messages = (
            db.query(ConversationMessage)
            .filter(ConversationMessage.negotiation_id == session.id)
            .order_by(ConversationMessage.created_at.asc())
            .all()
        )

        chat_history = [(m.sender, m.message) for m in past_messages]

        ai_text = generate_ai_message(
            decision=decision_obj.decision,
            reasoning={
                "base_price": product.base_price,
                "target_price": decision_obj.counter_price or decision_obj.target_price,
                "floor_price": product.floor_price,
                "quantity": quantity
            },
            psychology=["friendly", "persuasive", "indian_sales"],
            product_name=product.name,
            chat_history=chat_history
        )
        
        ai_message = ConversationMessage(
            negotiation_id=session.id,
            sender="ai",
            message=ai_text
        )
        db.add(ai_message)

        if decision_obj.decision == "accept":
            session.status = SessionStatus.completed
            session.final_price = decision_obj.target_price

        elif decision_obj.decision == "reject":
            session.status = SessionStatus.cancelled

        elif decision_obj.decision == "counter":
            ai_offer = Offer(
                session_id=session.id,
                customer_id=session.customer_id,
                offered_price=customer_offer,
                price=decision_obj.counter_price,
                quantity=1
            )
            db.add(ai_offer)

        db.commit()
        db.refresh(ai_message)

        # ✅ RETURN AI MESSAGE
        return MessageResponse(
            id=ai_message.id,
            session_id=ai_message.negotiation_id,
            sender=ai_message.sender,
            message=ai_message.message,
            created_at=ai_message.created_at
        )

    # Non-customer fallback
    return MessageResponse(
        id=customer_message.id,
        session_id=customer_message.negotiation_id,
        sender=customer_message.sender,
        message=customer_message.message,
        created_at=customer_message.created_at
    )


@router.get("/{session_id}", response_model=list[MessageResponse])
def get_messages(session_id: UUID, db: Session = Depends(get_db)):

    messages = (
        db.query(ConversationMessage)
        .filter(ConversationMessage.negotiation_id == session_id)
        .order_by(ConversationMessage.created_at.asc())
        .all()
    )

    return [
        MessageResponse(
            id=m.id,
            session_id=m.negotiation_id,
            sender=m.sender,
            message=m.message,
            created_at=m.created_at
        )
        for m in messages
    ]
