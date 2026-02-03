class NegotiationSessionRead(BaseModel):
    id: UUID
    customer_id: UUID
    product_id: UUID
    status: SessionStatus
    created_at: datetime

    class Config:
        from_attributes = True