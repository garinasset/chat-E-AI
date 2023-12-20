from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    UserName: Optional[str] = None
    NickName: Optional[str] = None
    userName: Optional[str] = None
    Province: Optional[str] = None
    City: Optional[str] = None
    Sex: Optional[int] = None