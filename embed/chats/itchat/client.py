from chat.WeChat.SDK import itchat
from chat.WeChat.SDK.itchat.content import TEXT
from common.log import LogUtils
from config.develop import ITCHAT_DEBUG
from config.settings import ITCHAT_HOT_RELOAD, ITCHAT_ENABLECMDQR
from embed.chats.itchat.messages.friend import handle_friend_message
from embed.chats.itchat.messages.group import handle_group_message
from embed.session import Session
from models.messages import MessageModelItchat


class ClientItchat:
    def __init__(self):
        self.client = itchat
        self.client.auto_login(hotReload=ITCHAT_HOT_RELOAD, enableCmdQR=ITCHAT_ENABLECMDQR)
        self.logger = LogUtils.new_logger("WeChat")
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
            _itcMsg = MessageModelItchat(**msg)
            # self.logger.debug({"MessageItchat":_itcMsg})
            _send = handle_friend_message(self, message=_itcMsg)
            if _send.action:
                itchat.send(msg=_send.content, toUserName=_send.user)
            else:
                pass

        @itchat.msg_register([TEXT], isGroupChat=True)
        def get_group_msg(msg):
            # self.logger.debug(msg)
            _itcMsg = MessageModelItchat(**msg)
            # self.logger.debug({"MessageItchat":_itcMsg})
            _send = handle_group_message(self, message=_itcMsg)
            if _send.action:
                itchat.send(msg=_send.content, toUserName=_send.user)
            else:
                pass

        self.client.run(debug=ITCHAT_DEBUG)

    def logout(self):
        self.client.logout()
