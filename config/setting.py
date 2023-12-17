##################################################################
# chat-E-AI Config File.                                        #
# Created by Fany, 2023                                          #
##################################################################


from AIs.OpenAI.AI_OpenAI_Model_Dicts import MODEL_DICTS_OPENAI
from AIs.OpenAI.tools.TIME import ToolTime
from AIs.OpenAI.tools.WWW_GARINASSET_COM import ToolWwwGarinassetCom
from AIs.OpenAI.tools.WTTR_IN import ToolWttrIn

# AI模块配置
"""Config Which You Want to Use."""
###################################
#  OpenAI                         #
###################################
# [OpenAI KEY]
"""OpenAI Key池。这是个数组，如果填入多个，例如["key1","key2"]，会轮询随机返回，简单负载均衡"""
"""默认3"""
OPENAI_API_KEYS = [""]

# [OpenAI Rate Limits]
"""指定Rate Limits限制（次数/分钟）。当OpenAI返回限制响应时，程序会自动等待。设定为0表示不限制。"""
"""默认3"""
OPENAI_API_RATE_LIMITS = 3

# [OpenAI模型]
"""编辑/chat-E-AI/AIs/OpenAI/AI_OpenAI_Model_Dicts.py"""
"""按文档说明，贡献补充其他模型"""
OPENAI_MODEL_DICTS = MODEL_DICTS_OPENAI["gpt-3.5-turbo-1106"]

# [OpenAI系统提示]
OPENAI_SYSTEM_CONTENT = '你是ChatGPT, 一个由OpenAI训练的大型语言模型, 你旨在回答并解决人们的任何问题，并且可以使用多种语言与人交流。'

# [OpenAI联网工具]
"""True or False"""
"""默认True"""
OPENAI_TOOLS_CONFIG = [
    {"enable": True, "Tool": ToolWwwGarinassetCom, "description": "嘉林数据-宏微观经济数据库"},
    {"enable": True, "Tool": ToolWttrIn, "description": "wttr.in-天气"},
    {"enable": True, "Tool": ToolTime, "description": "time-时间"},
]

# chat模块配置
"""Config Which You Want to Use."""
###################################
# ItChat                          #
###################################
CHAT_ItChat = 'ItChat'

# [ItChat记住登录]
"""默认True"""
ITCHAT_HOT_RELOAD = True

# [Itchat启用终端二维码]
"""默认2"""
ITCHAT_ENABLECMDQR = 2

# [ItChat-Debug模式]
"""True or False"""
"""默认False"""
SYSTEM_ITCHAT_DEBUG = False

# 系统配置 ###########################
"""Config Which You Want to want."""
####################################
# [启用OpenAI]
"""True or False"""
"""默认True"""
SYSTEM_OPENAI = True

# [启用ItChat]
"""True or False"""
"""默认True"""
SYSTEM_ITCHAT = True

# [ItChat呼叫暗号]
""""AI"表示回复AI开头的消息；""表示回复所有消息。"""
"""默认值：AI"""
SYSTEM_ITCHAT_CALL_CODE = "AI"

# [ItChat保留暗号]
""""如果不设置，当机器接管所有信息时，如果登录账号人工回复，机器也会响应回复。"""
"""默认值：AI"""
SYSTEM_ITCHAT_CALL_CODE_SELF = "AI"

# [ItChat私聊白名单]
"""{}表示全部；{"小明","小李"}表示只对小明、小李开放"""
"""默认全部"""
SYSTEM_ITCHAT_WHITELIST_FRIEND = {}

# [ItChat群聊白名单]
"""{}表示全部；{"AAA","BBB"}表示名称为AAA、BBB的群开放"""
"""默认全部"""
SYSTEM_ITCHAT_WHITELIST_GROUP = {}

# [上下文携带]
"""会话记录上下文对，0代表请求不携带历史会话记录。"""
"""默认3"""
USER_MESSAGES_LENGTH = 3

# [回复后缀]
USER_SUFFIX = "------------"
"""AI及工具来源"""
USER_SUFFIX_SOURCE = True
"""AI耗费"""
USER_SUFFIX_COST = True
