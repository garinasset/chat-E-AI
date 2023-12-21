from ai.openai.tools.TOOL_TIME import ToolTime
from ai.openai.tools.WTTR_IN import ToolWttrIn
from ai.openai.tools.WWW_GARINASSET_COM import ToolWwwGarinassetCom
from ai.openai.tools.XUEQIU_COM import ToolXueqiuCom
from config.settings import OPENAI_TOOLS_CONFIG
from models.response import ResponseBase


class OpenAITools:

    @staticmethod
    def get_tools() -> list:
        tools = []
        for tool_config in OPENAI_TOOLS_CONFIG:
            if tool_config["enable"]:
                tool_class = tool_config["Tool"]
                tools.append(tool_class.TOOL_MODEL)
        return tools

    @staticmethod
    def handle(name_tool_call: str, parameter_variables) -> ResponseBase:
        """1、处理路由OpenAI响应的function.name决定。"""
        """2、工具函数参数及变量值也是由OpenAI响应决定，需要具体工具具体相应处理。"""
        match name_tool_call:
            # 1.宏微观经济数据、行业数据、消费品市场价格数据工具-处理
            case ToolWwwGarinassetCom.get_indicator_overview.__name__:
                region = parameter_variables.get("region")
                name = parameter_variables.get("name")
                toolResponse = ToolWwwGarinassetCom.get_indicator_overview(region=region, name=name)
                return toolResponse
            # 2.天气工具-处理
            case ToolWttrIn.get_weather.__name__:
                location = parameter_variables.get("location")
                toolResponse = ToolWttrIn.get_weather(location=location)
                return toolResponse
            # 3.时间工具-处理
            case ToolTime.get_time.__name__:
                location = parameter_variables.get("location")
                offset_hours = parameter_variables.get("offset_hours")
                toolResponse = ToolTime.get_time(location=location, offset_hours=offset_hours)
                return toolResponse
            # 4.股票信息-处理
            case ToolXueqiuCom.get_stock.__name__:
                name = parameter_variables.get("name")
                symbol = parameter_variables.get("symbol")
                toolResponse = ToolXueqiuCom.get_stock(name=name, symbol=symbol)
                return toolResponse
