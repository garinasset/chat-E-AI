# 会话实例中间件：1、管理微信会话；2、组织会话记录上下文。
from AIs.OpenAI.AI_OpenAI import AIOpenAI
from utils.messages_queue import MessagesQueue
from config.setting import USER_MESSAGES_LENGTH


class ChatInstanceIEO:
    def __init__(self, from_user_name):
        # 会话对象
        self.fromUserName = from_user_name
        # 会话记录上下文 @ 一个奇数队列。
        self.messagesQueue = MessagesQueue((2 * USER_MESSAGES_LENGTH + 1))
        # AI实例
        self.ai = AIOpenAI()
