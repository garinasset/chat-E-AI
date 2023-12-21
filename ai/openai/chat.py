import json
from collections import deque

import backoff as backoff
import openai
from dotenv import load_dotenv
from openai import OpenAI

from ai.openai.tools.tools import OpenAITools
from ai.openai.utils.key import OpenAIUtilsKey
from common.log import LogUtils
from config.settings import OPENAI_MODEL_DICTS, OPENAI_SYSTEM_CONTENT, OPENAI_API_RATE_LIMITS, OPENAI_BASE_URL
from models.response import ResponseAI
from utils.calculate import UtilsCalculate

# 加载 .env 文件
load_dotenv()

# 日志logger
loggerOpenAI = LogUtils.new_logger("openai-Chat")
loggerBackoff = LogUtils.new_logger("library-backoff")


class AIOpenAIChat:
    def __init__(self):
        # 创建一个客户端实例
        self.client = OpenAI(
            api_key=OpenAIUtilsKey.get_key_in_env() if OpenAIUtilsKey.get_key_in_env() else OpenAIUtilsKey.get_key_in_config(),
            base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else None
        )
        self.model = OPENAI_MODEL_DICTS["Name"]
        self.msgSys = OPENAI_SYSTEM_CONTENT
        self.msgUserAssi = deque()
        self.messages = []
        self.tools = OpenAITools.get_tools()
        self.responseAI = ResponseAI(
            answer="",
            source="OpenAI",
            aiCost=0,
            aiCostCurrency=OPENAI_MODEL_DICTS['UnitCurrency']
        )

    def __setattr__(self, name, value):
        """messageContentUserAssistant更新则更新messages"""
        if name == "msgUserAssi":
            messages_system = [{
                "role": "system",
                "content": self.msgSys
            }]
            self.messages = messages_system + list(value)
        # 执行默认赋值操作
        super().__setattr__(name, value)

    # 调用
    def response(self):
        self.responseAI = ResponseAI(
            answer="",
            source="OpenAI",
            aiCost=0,
            aiCostCurrency=OPENAI_MODEL_DICTS['UnitCurrency']
        )

        """捕获openai.RateLimitError，回退重试。"""
        def _backoff_jitter(rate) -> float:
            _jitter = (60 / OPENAI_API_RATE_LIMITS) if OPENAI_API_RATE_LIMITS!=0 else 0
            return _jitter

        @backoff.on_exception(backoff.expo,
                              openai.RateLimitError,
                              max_time=60,
                              jitter=_backoff_jitter,
                              raise_on_giveup=False,
                              logger=loggerBackoff)
        def inner_function():
            try:
                response_chat_completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
                # Cost模块
                prompt_tokens = response_chat_completion.usage.prompt_tokens
                completion_tokens = response_chat_completion.usage.completion_tokens
                self.responseAI.aiCost = self.responseAI.aiCost + UtilsCalculate.cal_token_cost(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    model=OPENAI_MODEL_DICTS)

                toolCalls = response_chat_completion.choices[0].message.tool_calls
                # loggerOpenAI.debug(toolCalls)
                """判断OpenAI响应中是否响应tool_calls调用"""
                if toolCalls is None:
                    """没有响应tool_calls调用，直接回答。"""
                    _answer = response_chat_completion.choices[0].message.content
                    self.responseAI.answer = _answer
                    return
                else:
                    self.messages.append({"role": "assistant",
                                          "tool_calls": toolCalls
                                          })
                    for i in range(len(toolCalls)):
                        """响应tool_calls调用，本地代码逻辑，交给相应工具处理。"""
                        nameToolCall = toolCalls[i].function.name
                        parameterVariables = json.loads(toolCalls[i].function.arguments)
                        """记录日志"""
                        loggerOpenAI.info(f'Call Tool {nameToolCall} {parameterVariables}')
                        toolResponse = OpenAITools.handle(name_tool_call=nameToolCall,
                                                          parameter_variables=parameterVariables)
                        self.messages.append({"role": "tool",
                                              "tool_call_id": toolCalls[i].id,
                                              "content": toolResponse.answer})
                        self.responseAI.source = self.responseAI.source + "\n#" + toolResponse.source
                    return inner_function()
            except openai.RateLimitError as e:
                """记录日志"""
                loggerOpenAI.warning(e.message)
                # 在捕获到 openai.RateLimitError 异常时执行特定的逻辑
                self.responseAI.answer = e.message
                raise
            except openai.APIConnectionError as e:
                """记录日志"""
                loggerOpenAI.warning(e.message)
                self.responseAI.answer = e.message
            except openai.APIStatusError as e:
                """记录日志"""
                loggerOpenAI.warning(e.message)
                self.responseAI.answer = e.message
            return

        return inner_function()
