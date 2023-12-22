from config.settings import ITCHAT_CALL_CODE_SELF, ITCHAT_CALL_CODE, ITCHAT_WHITELIST_GROUP, ITCHAT_BLACKLIST_GROUP
from embed.reply.text import EReplyText
from models.messages import MessageItchat, MessageCea
from models.send import Send

def handle_group_message(client, message: MessageItchat)->Send:
    _callCodeSelf = ITCHAT_CALL_CODE_SELF
    _callCode = ITCHAT_CALL_CODE
    _whiteListGroup = ITCHAT_WHITELIST_GROUP
    _blackListGroup = ITCHAT_BLACKLIST_GROUP
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
                """我人工在群中发出"""
                if _itcMsg.Content.startswith(_callCodeSelf):
                    """携带内部暗号"""
                    _ceaMsg.Action = True
                    _ceaMsg.UserToSession = _ceaMsg.UserToReply
                    _ceaMsg.Content = _itcMsg.Content.lstrip(_callCodeSelf)
                    _ceaMsg.NickName = _itcMsg.ActualNickName
                    _ceaMsg.IsGroup = True
                else:
                    pass
            else:
                """群友发出"""
                _grpName = _itcMsg.User.NickName
                _memberNickName = _itcMsg.ActualNickName
                if (not _whiteListGroup or _grpName in _whiteListGroup) and _grpName not in _blackListGroup:
                    """群在白名单"""
                    if _itcMsg.Content.startswith(_callCode):
                        """携带外部暗号"""
                        _ceaMsg.Action = True
                        # _ceaMsg.UserToSession = _itcMsg.ActualNickName
                        _ceaMsg.UserToSession = _ceaMsg.UserToReply
                        _ceaMsg.Content = _itcMsg.Content.lstrip(_callCode)
                        _ceaMsg.NickName = _memberNickName
                        _ceaMsg.IsGroup = True
                    elif _itcMsg.IsAt:
                        """没有暗号，但被@"""
                        _ceaMsg.Action = True
                        _ceaMsg.UserToSession = _itcMsg.ActualNickName
                        # _ceaMsg.UserToSession = _ceaMsg.UserToReply
                        _ceaMsg.Content = _itcMsg.Content[_itcMsg.Content.find("\u2005") + 1:]
                        _ceaMsg.NickName = _memberNickName
                        _ceaMsg.IsGroup = True
                else:
                    pass
        case _:
            pass
    _send = EReplyText.reply(client=client,message=_ceaMsg)
    return _send
