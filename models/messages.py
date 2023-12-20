from typing import Optional, Union, Callable

from pydantic import BaseModel

from models.user import User


class MessageItchat(BaseModel):
    FromUserName: str
    ToUserName: str
    Type: str
    User: Optional[User]
    Content: Optional[str] = None
    Text: Union[list[str], str, Callable]
    ActualNickName: Optional[str] = None
    IsAt: Optional[bool] = False

class MessageCea(BaseModel):
    UserToReply: Optional[str] = None
    UserToSession: Optional[str] = None
    Content: Optional[str] = None
    Action: Optional[bool] = False
    NickName: Optional[str] = None
    IsGroup: Optional[bool] = False