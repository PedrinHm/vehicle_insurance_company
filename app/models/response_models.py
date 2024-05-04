from pydantic import BaseModel

class CreditScoreResponse(BaseModel):
    credit_score: float | None
