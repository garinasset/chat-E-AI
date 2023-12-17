import json
import logging

import requests
import pywttr
import urllib3

from models.ModelResponse import ResponseTool

# OpenAI Tools工具实现
# 必须实现一个TOOL_MODEL
# 必须有一个和TOOL_MODEL中函数名称对应的静态方法实现

loggerToolWttrIn = logging.getLogger("toolWttrIn")


class ToolWttrIn(object):
    TOOL_MODEL = {
        # 工具模型类型,必填，目前API支持 function
        "type": "function",
        "function": {
            # 函数名称，必填，The name of the get_weather to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
            "name": "get_weather",
            # 函数描述，必填，A description of what the get_weather does, used by the model to choose when and how to call the get_weather.
            "description": "获取给定地理位置的天气数据",
            # 函数参数，必填。
            "parameters": {
                "type": "object",
                # JSON键类型，及描述。
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "中文地理位置。",
                    },
                },
                "required": ["location"],
            },
        }
    }

    @staticmethod
    def get_weather(location: str) -> ResponseTool:
        language = pywttr.Language("zh-cn")
        response_tool = ResponseTool(answer="", source="wttr•in")

        """"疑难杂症处理"""
        if location in ["南极"]:
            loggerToolWttrIn.warning(f'This Entry Did Not Make a Request to the Weather Server Due to a Bug in the Weather Server, Which May Be Fix in the Future.')
            response_tool.answer = "亲爱的，我无法获取该地区的天气信息，你输入的地理位置是否过于宽泛呢？"
            return response_tool
        if location == "北极":
            location = "North Pole"

        """"正经处理"""
        try:
            weather_wttr = pywttr.get_weather(location=location, language=language)
            # print(weather_wttr)
            weather = f"当前{location}{weather_wttr.current_condition[0].lang_zh_cn[0].value}，" \
                      f"{weather_wttr.current_condition[0].temp_c}°C，" \
                      f"风速{weather_wttr.current_condition[0].windspeed_kmph}km/h，" \
                      f"湿度{weather_wttr.current_condition[0].humidity}%，" \
                      f"降水{weather_wttr.current_condition[0].precip_mm}mm。"
            response_tool.answer = weather
        except requests.exceptions.ConnectionError:
            loggerToolWttrIn.exception(f'requests.exceptions.ConnectionError')
            response_tool.answer = "亲爱的，我可能失去了天气服务的网络连接。"
        except urllib3.exceptions.MaxRetryError:
            loggerToolWttrIn.exception(f'urllib3.exceptions.MaxRetryError')
            response_tool.answer = "亲爱的，我遇到了障碍。\n\n这可能是有很多人在同时使用天气服务。"
        except requests.exceptions.SSLError:
            loggerToolWttrIn.exception(f'urllib3.exceptions.MaxRetryError')
            response_tool.answer = "亲爱的，我遇到了障碍。\n\n这可能是有很多人在同时使用天气服务。"
        except requests.exceptions.HTTPError:
            loggerToolWttrIn.exception(f'requests.exceptions.HTTPError')
            response_tool.answer = "亲爱的，我无法获取该地区的天气信息，大概是我们的尚没有收录该地区的天气情况。\n\n当然你也可以给我提供其他语言，这可能会增进我的理解。"
        except json.decoder.JSONDecodeError:
            loggerToolWttrIn.exception(f'json.decoder.JSONDecodeError')
            response_tool.answer = "亲爱的，我无法获取该地区的天气信息，你输入的地理位置是否过于宽泛呢？\n\n当然你也可以给我提供其他语言，这可能会增进我的理解。"
        return response_tool
