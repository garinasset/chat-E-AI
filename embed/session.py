# 会话实例中间件：1、管理微信会话；2、组织会话记录上下文。
from ai.openai.chat import AIOpenAIChat
from config.settings import USER_MESSAGES_LENGTH, SYSTEM_AI
from structures.queue import MessagesQueue


class Session:
    def __init__(self, user):
        # 会话对象
        self.user = user
        # 会话记录上下文 @ 一个奇数队列。
        self.msgQueue = MessagesQueue((2 * USER_MESSAGES_LENGTH + 1))
        # AI实例
        self.ai = self.get_ai()

    @staticmethod
    def get_ai():
        match SYSTEM_AI:
            case 'OpenAI':
                return AIOpenAIChat()
            case _:
                return None
