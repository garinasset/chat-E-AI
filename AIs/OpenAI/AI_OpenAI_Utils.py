import logging
import os
import random

from config.setting import OPENAI_API_KEYS
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

loggerOpenAI = logging.getLogger("OpenAI")


class AIOpenAIUtils:

    @staticmethod
    def get_key_in_config():
        _list_keys = OPENAI_API_KEYS
        if not _list_keys:
            loggerOpenAI.error("The OpenAI Keys Configure Item Were Not Found in The Configuration File.")
        else:
            if len(_list_keys) == 1 and _list_keys[0] == "":
                loggerOpenAI.error("The OpenAI Key Has Not Been Configured in The Configuration File.")
            else:
                return random.choice(_list_keys)
        return

    @staticmethod
    def get_key_in_env():
        _list_keys = os.environ.get('OPENAI_API_KEYS').split(",")
        if not _list_keys:
            return None
        else:
            if len(_list_keys) == 1 and _list_keys[0] == "":
                return None
            else:
                return random.choice(_list_keys)


AIOpenAIUtils.get_key_in_config()
