from E.itchat_E_OpenAI.itchat_E_AI import ItchatEAI
from config.setting import SYSTEM_ITCHAT
from system_components.log import Log


def main():
    logInstanceChatEAI = Log("chat-E-AI")
    logInstanceChatEAI.logger.info("⠋⠋⠋System Booting⠋⠋⠋")

    logInstanceItchatEAI = Log("itchatEOpenAI")
    logInstanceOpenAI = Log("OpenAI")
    logInstanceBackoff = Log("backoff")
    logInstanceTool_WTTR_IN = Log("toolTime")
    logInstanceTool_WTTR_IN = Log("toolWttrIn")
    logInstanceTool_WWW_GARINASSET_COM = Log("toolWwwGarinassetCom")
    try:
        # TODO 检查配置

        # TODO KILL

        # 运行itchat-E-OpenAI
        if SYSTEM_ITCHAT:
            logInstanceItchatEAI.logger.info("Embedding Chat ITCHAT⠋⠋⠋")
            chatEAI = ItchatEAI()
            chatEAI.start()

    except Exception as e:
        logInstanceChatEAI.logger.error(e)


if __name__ == "__main__":
    main()
