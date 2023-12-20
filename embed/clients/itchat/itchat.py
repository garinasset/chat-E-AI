from chat.WeChat.SDK import itchat
from chat.WeChat.SDK.itchat.content import TEXT
from common.log import LogUtils
from config.develop import ITCHAT_DEBUG
from config.settings import ITCHAT_HOT_RELOAD, ITCHAT_ENABLECMDQR
from embed.clients.itchat.messages.friend import handle_friend_message
from embed.clients.itchat.messages.group import handle_group_message
from embed.session import Session
from models.messages import MessageItchat


class ItchatClient:
    def __init__(self):
        itchat.auto_login(hotReload=ITCHAT_HOT_RELOAD, enableCmdQR=ITCHAT_ENABLECMDQR)
        self.logger = LogUtils.new_logger("client-ITCHAT")
        # 获取登录用户
        self.userName = itchat.instance.storageClass.userName
        self.nickName = itchat.instance.storageClass.nickName
        self.logger.info(f'WeChat Login Successfully as {self.nickName}({self.userName}).')
        # 会话实例字典
        self.sessionDicts = {}

    def get_session(self, sess_user_name) -> Session:
        if sess_user_name in self.sessionDicts:
            # 如果字典中已存在该用户ID的实例，则直接引用
            _session = self.sessionDicts[sess_user_name]
            return _session
        else:
            # 如果字典中不存在该用户ID的实例，则创建一个新的实例并存储在字典中
            _session = Session(sess_user_name)
            self.logger.info(f'Create Session ({_session.user})')
            self.sessionDicts[sess_user_name] = _session
            return _session

    def startup(self):
        # [TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM]
        @itchat.msg_register([TEXT], isFriendChat=True)
        def get_friend_msg(msg):
            # self.logger.debug(msg)
            _itcMsg = MessageItchat(**msg)
            # self.logger.debug({"MessageItchat":_itcMsg})
            _send = handle_friend_message(self,message=_itcMsg)
            if _send.action:
                itchat.send(msg=_send.content,toUserName=_send.user)
            else:
                pass


        @itchat.msg_register([TEXT], isGroupChat=True)
        def get_group_msg(msg):
            # self.logger.debug(msg)
            _itcMsg = MessageItchat(**msg)
            # self.logger.debug({"MessageItchat":_itcMsg})
            _send = handle_group_message(self,message=_itcMsg)
            if _send.action:
                itchat.send(msg=_send.content,toUserName=_send.user)
            else:
                pass
        itchat.run(debug=ITCHAT_DEBUG)



    # def handle_friend_message(self, message: MessageItchat):
    #     _callCodeSelf = ITCHAT_CALL_CODE_SELF
    #     _callCode = ITCHAT_CALL_CODE
    #     _whiteListFriend = ITCHAT_WHITELIST_FRIEND
    #     _ceaMsg = MessageCea.model_construct()
    #     match message.Type:
    #         case "System":
    #             pass
    #         case "Note":
    #             pass
    #         case "Text":
    #             _itcMsg = message
    #             # 标记待发送User.UserName
    #             _ceaMsg.UserToReply = _itcMsg.User.UserName if _itcMsg.User.UserName else _itcMsg.User.userName
    #             # 是否需要回复，如果是，完成其他标记
    #             if _itcMsg.FromUserName == self.userName:
    #                 """我发出"""
    #                 if _itcMsg.ToUserName == self.userName:
    #                     """发给本人账号"""
    #                     _ceaMsg.Action = True
    #                     _ceaMsg.UserToSession = self.nickName
    #                     _ceaMsg.Content = _itcMsg.Content
    #                     _ceaMsg.NickName = self.nickName
    #                 elif _itcMsg.ToUserName == 'filehelper':
    #                     """发给文件传输助手"""
    #                     _ceaMsg.Action = True
    #                     _ceaMsg.UserToSession = 'filehelper'
    #                     _ceaMsg.Content = _itcMsg.Content
    #                     _ceaMsg.NickName = self.nickName
    #                 else:
    #                     """发给朋友"""
    #                     _ceaMsg.Action = True if _itcMsg.Content.startswith(_callCodeSelf) else False
    #                     _ceaMsg.UserToSession = _ceaMsg.UserToReply
    #                     _ceaMsg.Content = _itcMsg.Content.lstrip(_callCodeSelf)
    #                     _ceaMsg.NickName = _itcMsg.User.NickName if _itcMsg.User.NickName else "朋友"
    #             else:
    #                 """朋友发出"""
    #                 _nickName = _itcMsg.User.NickName
    #                 if _nickName:
    #                     """有昵称"""
    #                     _ceaMsg.Action = True if _itcMsg.Content.startswith(_callCode) and (not _whiteListFriend or _nickName in _whiteListFriend) else False
    #                     _ceaMsg.UserToSession = _ceaMsg.UserToReply
    #                     _ceaMsg.Content = _itcMsg.Content.lstrip(_callCode)
    #                     _ceaMsg.NickName = _itcMsg.User.NickName
    #                 else:
    #                     """没有昵称"""
    #                     _ceaMsg.Action = True
    #                     _ceaMsg.UserToSession = _ceaMsg.UserToReply
    #                     _ceaMsg.Content = _itcMsg.Content.lstrip(_callCode)
    #                     _ceaMsg.NickName = '朋友'
    #         case _:
    #             pass
    #     self.reply_message(message=_ceaMsg)
    #
    # def handle_group_message(self, message: MessageItchat):
    #     _callCodeSelf = ITCHAT_CALL_CODE_SELF
    #     _callCode = ITCHAT_CALL_CODE
    #     _whiteListGroup = ITCHAT_WHITELIST_GROUP
    #     _ceaMsg = MessageCea.model_construct()
    #     match message.Type:
    #         case "System":
    #             pass
    #         case "Note":
    #             pass
    #         case "Text":
    #             _itcMsg = message
    #             # 标记待发送User.UserName
    #             _ceaMsg.UserToReply = _itcMsg.User.UserName if _itcMsg.User.UserName else _itcMsg.User.userName
    #             # 是否需要回复，如果是，完成其他标记
    #             if _itcMsg.FromUserName == self.userName:
    #                 """我人工在群中发出"""
    #                 if _itcMsg.Content.startswith(_callCodeSelf):
    #                     """携带内部暗号"""
    #                     _ceaMsg.Action = True
    #                     _ceaMsg.UserToSession = _ceaMsg.UserToReply
    #                     _ceaMsg.Content = _itcMsg.Content.lstrip(_callCodeSelf)
    #                     _ceaMsg.NickName = _itcMsg.ActualNickName
    #                     _ceaMsg.IsGroup = True
    #                 else:
    #                     pass
    #             else:
    #                 """群友发出"""
    #                 _grpName = _itcMsg.User.NickName
    #                 _memberNickName = _itcMsg.ActualNickName
    #                 if not _whiteListGroup or _grpName in _whiteListGroup:
    #                     """群在白名单"""
    #                     if _itcMsg.Content.startswith(_callCode):
    #                         """携带外部暗号"""
    #                         _ceaMsg.Action = True
    #                         _ceaMsg.UserToSession = _ceaMsg.UserToReply
    #                         _ceaMsg.Content = _itcMsg.Content.lstrip(_callCode)
    #                         _ceaMsg.NickName = _memberNickName
    #                         _ceaMsg.IsGroup = True
    #                     elif _itcMsg.IsAt:
    #                         """没有暗号，但被@"""
    #                         _ceaMsg.Action = True
    #                         _ceaMsg.UserToSession = _itcMsg.ActualNickName
    #                         _ceaMsg.Content = _itcMsg.Content[_itcMsg.Content.find("\u2005") + 1:]
    #                         _ceaMsg.NickName = _memberNickName
    #                         _ceaMsg.IsGroup = True
    #                 else:
    #                     pass
    #         case _:
    #             pass
    #     self.reply_message(message=_ceaMsg)
    #
    # def reply_message(self, message:MessageCea):
    #     _ceaMsg = message
    #     _action = _ceaMsg.Action
    #     if _action:
    #         # 记录日志
    #         self.logger.info(f'Message Signal RX: {_ceaMsg.UserToSession} {UtilsString.log_msg(_ceaMsg.Content)}')
    #         """messages前置处理"""
    #         _sess = self.get_session(sess_user_name=_ceaMsg.UserToSession)
    #         # 会话实例user messages入列
    #         _sess.msgQueue.enqueue_user(message_content=_ceaMsg.Content)
    #         # AI实例messages更新。
    #         _sess.ai.msgUserAssi = _sess.msgQueue.queue
    #         """AI调用"""
    #         _sess.ai.response()
    #         _rspAi = _sess.ai.responseAI
    #         _rspAns = _rspAi.answer
    #         """messages后置处理"""
    #         _sess.msgQueue.enqueue_assistant(message_content=_rspAns)
    #         """assistant messages入列。"""
    #         _sess.ai.msgUserAssi = _sess.msgQueue.queue
    #         """会话实例中的OpenAI实例 messages更新。"""
    #         # 添加前后缀
    #         # self.logger.debug({"MessageCea":_ceaMsg})
    #         _contentOutput = f'@{_ceaMsg.NickName}\n{EUtilsSuffix.add_suffix(_rspAi)}' if _ceaMsg.IsGroup else EUtilsSuffix.add_suffix(_rspAi)
    #         # 发送
    #         itchat.send(_contentOutput, toUserName=_ceaMsg.UserToReply)
    #         # 记录日志
    #         self.logger.info(f'Message Signal TX: {_ceaMsg.UserToSession} {UtilsString.log_msg(_contentOutput)}')
    #     else:
    #         pass
