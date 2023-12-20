from embed.clients.itchat.itchat import ItchatClient
from common.log import LogUtils
from config.settings import SYSTEM_ITCHAT


def main():
    loggerSystem = LogUtils.new_logger("chat-E-AI")
    loggerSystem.info("⠋⠋⠋System Booting⠋⠋⠋")


    try:
        # Embedding Access
        if SYSTEM_ITCHAT:
            loggerSystem.info("Access Chat WeChat Use ITCHAT.")
            client = ItchatClient()
            client.startup()

    except Exception as e:
        loggerSystem.error(e)


if __name__ == "__main__":
    main()
