# 会话实例中间件：1、管理微信会话；2、组织会话记录上下文。
from AIs.openai.chat import AIOpenAIChat
from structures.queue import MessagesQueue
from config.settings import USER_MESSAGES_LENGTH


class Session:
    def __init__(self, user):
        # 会话对象
        self.user = user
        # 会话记录上下文 @ 一个奇数队列。
        self.msgQueue = MessagesQueue((2 * USER_MESSAGES_LENGTH + 1))
        # AI实例
        self.ai = AIOpenAIChat()
