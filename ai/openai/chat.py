import datetime
import json
from collections import deque

import backoff as backoff
import openai
import requests
from dotenv import load_dotenv
from openai import OpenAI

from ai.openai.tools.tools import OpenAITools
from ai.openai.utils.key import OpenAIUtilsKey
from common.log import LogUtils
from config.settings import OPENAI_MODEL_DICTS, OPENAI_SYSTEM_CONTENT, OPENAI_API_RATE_LIMITS, OPENAI_BASE_URL
from models.openai import CreditSummary
from models.response import ResponseAI
from utils.calculate import UtilsCalculate
from utils.string import UtilsString

# 加载 .env 文件
load_dotenv()

# 日志logger
loggerOpenAI = LogUtils.new_logger("AI-OpenAI")


class AIOpenAIChat:
    def __init__(self):
        # 创建一个客户端实例
        self.client = OpenAI(
            api_key=OpenAIUtilsKey.get_key_in_env() if OpenAIUtilsKey.get_key_in_env() else OpenAIUtilsKey.get_key_in_config(),
            base_url=OPENAI_BASE_URL if OPENAI_BASE_URL else None
        )
        self.model = OPENAI_MODEL_DICTS["Name"]
        self.msgSys = OPENAI_SYSTEM_CONTENT
        self.cmdModel = False
        self.cmdString = ''
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
        if not self.cmdModel:
            """捕获openai.RateLimitError，回退重试。"""

            @backoff.on_exception(backoff.expo,
                                  openai.RateLimitError,
                                  max_time=60,
                                  jitter=(60 / OPENAI_API_RATE_LIMITS) if OPENAI_API_RATE_LIMITS != 0 else 0,
                                  raise_on_giveup=False,
                                  logger=loggerOpenAI)
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
        else:
            loggerOpenAI.info(f"Call CMD {self.cmdString}")
            match self.cmdString:
                case '系统提示':
                    _newMsgSys = str(self.msgUserAssi[-1]['content'])
                    self.responseAI.answer = (f"#系统提示 - 超级命令\n\n"
                                              f"系统提示词（新）：\n***\n“{UtilsString.get_omitted_text(str(self.msgSys))}”\n***\n\n"
                                              f"系统提示词（旧）：\n***\n“{UtilsString.get_omitted_text(_newMsgSys)}”\n***"
                                              )
                    self.msgSys = _newMsgSys
                    self.msgUserAssi.clear()

                case '账单查询':
                    if self.client.api_key.startswith("sess"):
                        _url = str(
                            OPENAI_BASE_URL + '/dashboard/billing/credit_grants' if OPENAI_BASE_URL else 'https://api.openai.com/dashboard/billing/credit_grants')
                        # 设置请求头部
                        _headers = {
                            'Authorization': f"Bearer {str(self.client.api_key)}"
                        }
                        # 发起 GET 请求
                        response = requests.get(_url, headers=_headers)
                        # 检查响应状态码
                        if response.status_code == 200:
                            # 请求成功，可以处理响应数据
                            _res = CreditSummary(**(response.json()))
                            _effectiveDate = datetime.datetime.fromtimestamp(_res.grants.data[0].effective_at).strftime(
                                "%Y-%m-%d")
                            _expiresDate = datetime.datetime.fromtimestamp(_res.grants.data[0].expires_at).strftime(
                                "%Y-%m-%d")
                            self.responseAI.answer = str(f"#账单查询 - 超级命令\n\n"
                                                         f"{UtilsString.get_omitted_text(str(self.client.api_key))}\n"
                                                         f"① 全部额度：$ {_res.total_granted}\n"
                                                         f"② 使用额度：$ {_res.total_used}\n"
                                                         f"③ 授权时间：{_effectiveDate}\n"
                                                         f"④ 过期时间：{_expiresDate}\n"
                                                         f"⑤ 剩余额度：$ {_res.total_available}"
                                                         )
                        else:
                            self.responseAI.answer = str(f"#账单查询 - 超级命令\n\n"
                                                         f"{UtilsString.get_omitted_text(str(self.client.api_key))}\n\n"
                                                         f"*错误*\n"
                                                         f"账单查询发生错误，这很大可能是因为你的网络问题，如果你确定网络正常，可以向我们反馈，以增进产品改进。"
                                                         )

                    else:
                        self.responseAI.answer = str(f"#账单查询 - 超级命令\n\n"
                                                     f"{UtilsString.get_omitted_text(str(self.client.api_key))}”\n\n"
                                                     f"*注意*\n"
                                                     f"你当前Key类型为API Key，但是账单查询仅支持Session Key，这里的支持有限是因为官方查询接口对API Key的支持不完备。"
                                                     )
                    self.msgUserAssi.pop()

                case '恢复出厂':
                    self.responseAI.answer = str(f"#恢复出厂 - 超级命令\n\n"
                                                 f"① 系统提示已重置。\n"
                                                 f"② 消息队列已清理。")
                    self.msgSys = OPENAI_SYSTEM_CONTENT
                    self.msgUserAssi.clear()
            self.cmdModel = False
            return
