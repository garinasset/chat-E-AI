from typing import List
from pydantic import BaseModel


class CreditGrant(BaseModel):
    object: str
    id: str
    grant_amount: float
    used_amount: float
    effective_at: float
    expires_at: float


class Grants(BaseModel):
    object: str
    data: List[CreditGrant]


class CreditSummary(BaseModel):
    object: str
    total_granted: float
    total_used: float
    total_available: float
    total_paid_available: float
    grants: Grants
