from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerOut)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    # 1. Check if customer already exists
    existing = (
        db.query(Customer)
        .filter(Customer.phone_number == data.phone_number)
        .first()
    )
    if existing:
        return existing

    # 2. CREATE CUSTOMER (THIS WAS BROKEN EARLIER)
    customer = Customer(
        name=data.name,                      # ✅ FIX
        phone_number=data.phone_number,      # ✅ FIX
        language_preference=data.language    # ✅ FIX
    )

    # 3. Save to DB
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer
