import os
import json
import logging
from collections import deque

import openai
from openai import OpenAI

from AIs.AI import AI
from AIs.OpenAI.tools.AI_OPENAI_TOOLS import AIOpenAITools
from config.setting import OPENAI_API_KEY, OPENAI_MODEL_DICTS, OPENAI_SYSTEM_CONTENT
from models.ModelResponse import Response
from utils.utils_calculate import UtilsCalculate

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

loggerOpenAI = logging.getLogger("OpenAI")


class AIOpenAI(AI):
    def __init__(self):
        # 创建一个客户端实例
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY") if os.environ.get("OPENAI_API_KEY") else OPENAI_API_KEY,
        )
        self.model = OPENAI_MODEL_DICTS["Name"]
        self.messageContentSystem = OPENAI_SYSTEM_CONTENT
        self.messageContentUserAssistant = deque()
        self.messages = []
        self.tools = AIOpenAITools.get_tools()

    def __setattr__(self, name, value):
        """messageContentUserAssistant更新则更新messages"""
        if name == "messageContentUserAssistant":
            messages_system = [{
                "role": "system",
                "content": self.messageContentSystem
            }]
            self.messages = messages_system + list(value)
        # 执行默认赋值操作
        super().__setattr__(name, value)

    # 调用
    def response(self) -> Response:
        # 响应模型初始化
        _response = Response(
            answer="",
            source="OpenAI",
            aiCost=0,
            aiCostCurrency=OPENAI_MODEL_DICTS['UnitCurrency']
        )

        def inner_function() -> Response:
            nonlocal _response
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
                _response.aiCost = _response.aiCost + UtilsCalculate.cal_token_cost(prompt_tokens=prompt_tokens,
                                                                                    completion_tokens=completion_tokens,
                                                                                    model=OPENAI_MODEL_DICTS)

                toolCalls = response_chat_completion.choices[0].message.tool_calls
                """判断OpenAI响应中是否响应tool_calls调用"""
                if toolCalls is None:
                    """没有响应tool_calls调用，直接回答。"""
                    answer = response_chat_completion.choices[0].message.content
                    _response.answer = answer
                    return _response
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
                        toolResponse = AIOpenAITools.handle(name_tool_call=nameToolCall,
                                                            parameter_variables=parameterVariables)
                        self.messages.append({"role": "tool",
                                              "tool_call_id": toolCalls[i].id,
                                              "content": toolResponse.answer})
                        _response.source = _response.source + "\n#" + toolResponse.source
                    return inner_function()
            except openai.APIConnectionError as e:
                """记录日志"""
                loggerOpenAI.error(e.message)

                _response.answer = e.message
                return _response
            except openai.APIStatusError as e:
                """记录日志"""
                loggerOpenAI.error(e.message)

                _response.answer = e.message
                return _response

        _response = inner_function()
        return _response
