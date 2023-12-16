import logging

from E.itchat_E_OpenAI.ChatInstanceIEO import ChatInstanceIEO
from chats.WeChat.SDK import itchat
from chats.WeChat.SDK.itchat.content import TEXT
from config.setting import ITCHAT_HOT_RELOAD, ITCHAT_ENABLECMDQR, SYSTEM_ITCHAT_DEBUG, \
    USER_SUFFIX_COST, USER_SUFFIX, USER_SUFFIX_SOURCE, SYSTEM_ITCHAT_WHITELIST_GROUP, SYSTEM_ITCHAT_CALL_CODE, \
    SYSTEM_ITCHAT_CALL_CODE_SELF, SYSTEM_ITCHAT_WHITELIST_FRIEND
from utils.utils_string import UtilsString

loggerItchatEAI = logging.getLogger("itchatEOpenAI")


class ItchatEOpenAI:
    def __init__(self):
        itchat.auto_login(hotReload=ITCHAT_HOT_RELOAD, enableCmdQR=ITCHAT_ENABLECMDQR)
        # 获取登录用户
        self.userName = itchat.instance.storageClass.userName
        self.nickName = itchat.instance.storageClass.nickName
        loggerItchatEAI.info(f'Embedding Chat ITCHAT Successfully as {self.nickName}({self.userName}).')
        # 会话实例字典
        self.chatInstances = {}

    @staticmethod
    def util_gen_replay_suffix(response_answer, response):
        replay = response_answer
        if USER_SUFFIX_SOURCE or USER_SUFFIX_COST:
            if USER_SUFFIX_SOURCE:
                replay += f"\n\n#{response.source}"
            if USER_SUFFIX_COST:
                replay += f"\n{USER_SUFFIX}\n{response.aiCostCurrency} {round(response.aiCost,6)}"
        return replay

    def get_chat_instance(self, user_name) -> ChatInstanceIEO:
        if user_name in self.chatInstances:
            # 如果字典中已存在该用户ID的实例，则直接引用
            chat_instance = self.chatInstances[user_name]
            return chat_instance
        else:
            # 如果字典中不存在该用户ID的实例，则创建一个新的实例并存储在字典中
            chat_instance = ChatInstanceIEO(user_name)
            loggerItchatEAI.info(f'Create Chat Instance ({chat_instance.fromUserName})')
            self.chatInstances[user_name] = chat_instance
            return chat_instance

    def replay_text(self, msg_itchat, user_chat_instance):
        content_receive = msg_itchat.Text
        chat_instance = self.get_chat_instance(user_chat_instance)
        """获取会话实例"""

        chat_instance.messagesQueue.enqueue_user(message_content=content_receive)
        """会话实例user messages入列"""
        chat_instance.ai.messageContentUserAssistant = chat_instance.messagesQueue.queue
        """AI实例messages更新。"""

        response = chat_instance.ai.response()
        response_answer = response.answer

        chat_instance.messagesQueue.enqueue_assistant(message_content=response_answer)
        """assistant messages入列。"""
        chat_instance.ai.messageContentUserAssistant = chat_instance.messagesQueue.queue
        """会话实例中的OpenAI实例 messages更新。"""

        replay = ItchatEOpenAI.util_gen_replay_suffix(response_answer, response)
        return replay

    def start(self):
        @itchat.msg_register(TEXT, isFriendChat=True)
        def handler_friend_chat(msg_itchat):
            # 自发自收（微信可以自发自收，不是所有？待确定，I Can.）
            if msg_itchat.FromUserName == msg_itchat.ToUserName:
                """记录日志"""
                loggerItchatEAI.info(
                    f'Message Signal RX: {msg_itchat.FromUserName} {UtilsString.log_msg(msg_itchat.Text)}')
                userChatInstance = msg_itchat.User.NickName
                to_user_name = msg_itchat.FromUserName
                replay = self.replay_text(msg_itchat=msg_itchat, user_chat_instance=userChatInstance)
                itchat.send(replay, toUserName=to_user_name)
                loggerItchatEAI.info(
                    f'Message Signal TX: {to_user_name} {UtilsString.log_msg(replay)}')
            # 文件传输助手
            elif msg_itchat.ToUserName == 'filehelper':
                """记录日志"""
                loggerItchatEAI.info(
                    f'Message Signal RX: {msg_itchat.FromUserName} {UtilsString.log_msg(msg_itchat.Text)}')
                userChatInstance = 'filehelper'
                to_user_name = 'filehelper'
                replay = self.replay_text(msg_itchat=msg_itchat, user_chat_instance=userChatInstance)
                itchat.send(replay, toUserName=to_user_name)
                loggerItchatEAI.info(
                    f'Message Signal TX: {to_user_name} {UtilsString.log_msg(replay)}')
            else:
                is_whitelist = not SYSTEM_ITCHAT_WHITELIST_FRIEND or msg_itchat.NickName in SYSTEM_ITCHAT_WHITELIST_FRIEND
                is_call_code = (SYSTEM_ITCHAT_CALL_CODE and msg_itchat.Text.startswith(
                    SYSTEM_ITCHAT_CALL_CODE_SELF)) or msg_itchat.Text.startswith(SYSTEM_ITCHAT_CALL_CODE)
                if is_whitelist and is_call_code:
                    # 自发他收
                    if msg_itchat.FromUserName == self.userName:
                        if msg_itchat.Text.startswith(SYSTEM_ITCHAT_CALL_CODE_SELF):
                            loggerItchatEAI.info(
                                f'Message Signal RX: {msg_itchat.FromUserName} {UtilsString.log_msg(msg_itchat.Text)}')
                            msg_itchat.Text = msg_itchat.Text.lstrip(SYSTEM_ITCHAT_CALL_CODE_SELF)
                            userChatInstance = msg_itchat.FromUserName
                            to_user_name = msg_itchat.ToUserName
                            replay = self.replay_text(msg_itchat=msg_itchat, user_chat_instance=userChatInstance)
                            itchat.send(replay, toUserName=to_user_name)
                            loggerItchatEAI.info(
                                f'Message Signal TX: {to_user_name} {UtilsString.log_msg(replay)}')
                    # 第三方发（朋友）
                    else:
                        if msg_itchat.Text.startswith(SYSTEM_ITCHAT_CALL_CODE):
                            """记录日志"""
                            loggerItchatEAI.info(
                                f'Message Signal RX: {msg_itchat.FromUserName} {UtilsString.log_msg(msg_itchat.Text)}')
                            msg_itchat.Text = msg_itchat.Text.lstrip(SYSTEM_ITCHAT_CALL_CODE)
                            userChatInstance = msg_itchat.FromUserName
                            to_user_name = msg_itchat.FromUserName
                            replay = self.replay_text(msg_itchat=msg_itchat, user_chat_instance=userChatInstance)
                            itchat.send(replay, toUserName=to_user_name)
                            loggerItchatEAI.info(
                                f'Message Signal TX: {to_user_name} {UtilsString.log_msg(replay)}')

        @itchat.msg_register(TEXT, isGroupChat=True)
        def handler_group_chat(msg_itchat):
            is_whitelist = not SYSTEM_ITCHAT_WHITELIST_GROUP or msg_itchat.NickName in SYSTEM_ITCHAT_WHITELIST_GROUP
            is_call_code = (SYSTEM_ITCHAT_CALL_CODE and msg_itchat.Text.startswith(
                SYSTEM_ITCHAT_CALL_CODE_SELF)) or msg_itchat.Text.startswith(SYSTEM_ITCHAT_CALL_CODE)
            if is_whitelist and is_call_code or msg_itchat.IsAt:
                # 自发群收，带有关键字才响应，群ID作为会话实例Key
                if msg_itchat.FromUserName == self.userName and msg_itchat.Text.startswith(
                        SYSTEM_ITCHAT_CALL_CODE_SELF):
                    """记录日志"""
                    loggerItchatEAI.info(
                        f'Message Group RX: {msg_itchat.FromUserName} {UtilsString.log_msg(msg_itchat.Text)}')
                    msg_itchat.Text = msg_itchat.Text.lstrip(SYSTEM_ITCHAT_CALL_CODE_SELF)
                    userChatInstance = msg_itchat.ToUserName
                    to_user_name = msg_itchat.ToUserName
                    replay = self.replay_text(msg_itchat=msg_itchat, user_chat_instance=userChatInstance)
                    replay = "@" + msg_itchat.ActualNickName + "\n" + replay
                    itchat.send(replay, toUserName=to_user_name)
                    loggerItchatEAI.info(
                        f'Message Group TX: {to_user_name} {UtilsString.log_msg(replay)}')
                # 他发群收，@或者匹配非空关键字才响应，作为会话实例Key
                if msg_itchat.IsAt or (SYSTEM_ITCHAT_CALL_CODE and msg_itchat.Text.startswith(SYSTEM_ITCHAT_CALL_CODE)):
                    """记录日志"""
                    loggerItchatEAI.info(
                        f'Message Group RX: {msg_itchat.FromUserName} {UtilsString.log_msg(msg_itchat.Text)}')
                    msg_itchat.Text = msg_itchat.Text[msg_itchat.Text.find("\u2005") + 1:]
                    userChatInstance = msg_itchat.ActualNickName
                    to_user_name = msg_itchat.FromUserName
                    replay = self.replay_text(msg_itchat=msg_itchat, user_chat_instance=userChatInstance)
                    replay = "@" + msg_itchat.ActualNickName + "\n" + replay
                    itchat.send(replay, toUserName=to_user_name)
                    loggerItchatEAI.info(
                        f'Message Group TX: {to_user_name} {UtilsString.log_msg(replay)}')

        itchat.run(debug=SYSTEM_ITCHAT_DEBUG)
