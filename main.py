import signal

from embed.chats.itchat.client import ClientItchat
from common.log import LogUtils
from config.settings import SYSTEM_CHAT, SYSTEM_AI

loggerSystem = LogUtils.new_logger("SYSTEM")


def sigterm_handler(signum, frame):
    raise SystemExit("接收到 SIGTERM 信号")


# 注册 SIGTERM 信号处理器
signal.signal(signal.SIGTERM, sigterm_handler)


class MainClass:
    def __init__(self):
        self.get_ai()
        self.chat = self.get_chat()

    @staticmethod
    def get_chat():
        match SYSTEM_CHAT:
            case 'ITCHAT':
                loggerSystem.info("Access Chat WeChat(ITCHAT).")
                return ClientItchat()
            case _:
                return None

    @staticmethod
    def get_ai():
        match SYSTEM_AI:
            case 'OpenAI':
                loggerSystem.info("Access AI OpenAI.")
                return None
            case _:
                return None

    def main(self):
        self.chat.startup()


if __name__ == "__main__":
    try:
        loggerSystem.info("⠋⠋⠋System Booting⠋⠋⠋")
        instance = MainClass()
        instance.main()
    except KeyboardInterrupt:
        loggerSystem.warning("System Quit as 「Ctrl C」")
    except SystemExit:
        loggerSystem.warning("System Quit as 「SystemExit」")
    except Exception:
        loggerSystem.error("System Error in 「instance.main()」 in 「main.py」")
