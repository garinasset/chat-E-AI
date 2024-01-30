from typing import Optional

from pydantic import BaseModel


class Send(BaseModel):
    user: Optional[str] = None
    content: Optional[str] = None
    action: Optional[bool] = False
