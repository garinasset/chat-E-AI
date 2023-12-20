from pydantic import BaseModel


class ResponseBase(BaseModel):
    answer: str
    source: str


class ResponseAI(ResponseBase):
    aiCost: float
    aiCostCurrency: str
