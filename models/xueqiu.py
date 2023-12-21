from typing import Optional

from pydantic import BaseModel


class XueQiu(BaseModel):
    symbol: Optional[str] = None
    is_trade:Optional[bool] = False
    current: Optional[float] = None
    percent: Optional[float] = None
    market_capital: Optional[float] = None
    float_market_capital: Optional[float] = None
    amount: Optional[float] = None
    current_year_percent: Optional[float] = None
