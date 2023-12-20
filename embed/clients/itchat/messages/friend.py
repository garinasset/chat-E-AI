from config.settings import ITCHAT_CALL_CODE_SELF, ITCHAT_CALL_CODE, ITCHAT_WHITELIST_FRIEND
from embed.reply.text import EReplyText
from models.messages import MessageItchat, MessageCea
from models.send import Send


def handle_friend_message(client, message: MessageItchat) -> Send:
    _callCodeSelf = ITCHAT_CALL_CODE_SELF
    _callCode = ITCHAT_CALL_CODE
    _whiteListFriend = ITCHAT_WHITELIST_FRIEND
    _ceaMsg = MessageCea.model_construct()
    match message.Type:
        case "System":
            pass
        case "Note":
            pass
        case "Text":
            _itcMsg = message
            # 标记待发送User.UserName
            _ceaMsg.UserToReply = _itcMsg.User.UserName if _itcMsg.User.UserName else _itcMsg.User.userName
            # 是否需要回复，如果是，完成其他标记
            if _itcMsg.FromUserName == client.userName:
                """我发出"""
                if _itcMsg.ToUserName == client.userName:
                    """发给本人账号"""
                    _ceaMsg.Action = True
                    _ceaMsg.UserToSession = client.nickName
                    _ceaMsg.Content = _itcMsg.Content
                    _ceaMsg.NickName = client.nickName
                elif _itcMsg.ToUserName == 'filehelper':
                    """发给文件传输助手"""
                    _ceaMsg.Action = True
                    _ceaMsg.UserToSession = 'filehelper'
                    _ceaMsg.Content = _itcMsg.Content
                    _ceaMsg.NickName = client.nickName
                else:
                    """发给朋友"""
                    _ceaMsg.Action = True if _itcMsg.Content.startswith(_callCodeSelf) else False
                    _ceaMsg.UserToSession = _ceaMsg.UserToReply
                    _ceaMsg.Content = _itcMsg.Content.lstrip(_callCodeSelf)
                    _ceaMsg.NickName = _itcMsg.User.NickName if _itcMsg.User.NickName else "朋友"
            else:
                """朋友发出"""
                _nickName = _itcMsg.User.NickName
                if _nickName:
                    """有昵称"""
                    _ceaMsg.Action = True if _itcMsg.Content.startswith(_callCode) and (
                                not _whiteListFriend or _nickName in _whiteListFriend) else False
                    _ceaMsg.UserToSession = _ceaMsg.UserToReply
                    _ceaMsg.Content = _itcMsg.Content.lstrip(_callCode)
                    _ceaMsg.NickName = _itcMsg.User.NickName
                else:
                    """没有昵称"""
                    _ceaMsg.Action = True
                    _ceaMsg.UserToSession = _ceaMsg.UserToReply
                    _ceaMsg.Content = _itcMsg.Content.lstrip(_callCode)
                    _ceaMsg.NickName = '朋友'
        case _:
            pass
    _send = EReplyText.reply(client=client, message=_ceaMsg)
    return _send

