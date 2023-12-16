from typing import Optional

from pydantic import BaseModel


class ResponseTool(BaseModel):
    answer: str
    source: str


class Response(ResponseTool):
    aiCost: float
    aiCostCurrency: str
