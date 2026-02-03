from pydantic import BaseModel, Field
from typing import Optional, Literal


class LLMNegotiationOutput(BaseModel):
    decision_type: Literal["accept", "reject", "counter"]
    counter_price: Optional[float] = Field(default=None)
    message_text: str
    confidence_score: float

    class Config:
        from_attributes = True
