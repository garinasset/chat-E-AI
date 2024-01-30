# openai Tools工具实现
# 必须实现一个TOOL_MODEL
# 必须有一个和TOOL_MODEL中函数名称对应的静态方法实现
import pandas as pd
import requests

from common.log import LogUtils
from models.response import ResponseBase

logger = LogUtils.new_logger("OpenAI-toolWwwGarinassetCom")


class ToolWwwGarinassetCom(object):
    TOOL_MODEL = {
        # 工具类型，必填，强制function
        "type": "function",
        "function": {
            # 函数名称，必填，The name of the get_weather to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
            "name": "get_indicator_overview",
            # 函数描述，必填，A description of what the get_weather does, used by the model to choose when and how to call the get_weather.
            "description": "获取给定国家、行政区域的宏微观经济数据，行业数据，消费品市场价格数据，例如中国GDP，汽车产量，鸡蛋价格，如果没有给定行政区域，默认为中国大陆。",
            # 函数参数，必填。
            "parameters": {
                "type": "object",
                # JSON键类型，及描述。
                "properties": {
                    "region": {
                        "type": "string",
                        "description": "中文行政区域，例如，中国大陆、香港。",
                    },
                    "name": {
                        "type": "string",
                        "description": "中文指标名称，例如国内生产总值，GDP，鸡蛋价格。"
                    },
                },
                "required": ["region", "name"],
            },
        }
    }

    @staticmethod
    def _handle_datetime(name_property_json, data_latest_time) -> str:
        match name_property_json:
            case "月值":
                _date = pd.Timestamp(data_latest_time)
                _dateTime = "{}年{}月".format(_date.year, _date.month)
                return _dateTime
            case "累月值":
                _date = pd.Timestamp(data_latest_time)
                _dateTime = "{}年前{}月".format(_date.year, _date.month)
                return _dateTime
            case "季值":
                _date = pd.Timestamp(data_latest_time)
                _dateTime = "{}年{}季度".format(_date.year, _date.quarter)
                return _dateTime
            case "年值":
                _date = pd.Timestamp(data_latest_time)
                _dateTime = "{}年".format(_date.year)
                return _dateTime
            case _:
                _date = pd.Timestamp(data_latest_time)
                _dateTime = "{}年{}月{}日".format(_date.year, _date.month, _date.day)
                return _dateTime

    @staticmethod
    def _handle_element(element):
        _name_attribute = None
        _data_year_over_year_diff = None
        _currency = None
        _unit = None

        if element['names']['name_attribute_json'] is not None:
            _name_attribute = "(统计口径：{})".format(element['names']['name_attribute_json'][0])
        if element['currencies'] is not None:
            _currency = element['currencies']['currency_json'][0]
        if element['units'] is not None:
            _unit = element['units']['unit_json'][0]
        if element['data_year_over_year'] is not None:
            data_year_over_year = element['data_year_over_year']['data_latest_value']
            data_year_over_year_fixed = element['data_year_over_year_fixed']
            _data_year_over_year_diff = round(data_year_over_year - data_year_over_year_fixed, 2)
            if _data_year_over_year_diff is not None and _data_year_over_year_diff > 0:
                _data_year_over_year_diff = "，同比：+{}%。".format(_data_year_over_year_diff)
            else:
                _data_year_over_year_diff = "，同比：{}%。".format(_data_year_over_year_diff)
        _data_latest_time = element['data']['data_latest_time']
        _name_property_json = element['names']['name_property_json'][0]
        _dateTime = ToolWwwGarinassetCom._handle_datetime(data_latest_time=_data_latest_time,
                                                          name_property_json=_name_property_json)

        element_overview = "{}，{}{}{}为{}{}{}{}".format(
            _dateTime,
            element['regions']['region_json'][0],
            element['names']['name_json'][0],
            _name_attribute if _name_attribute else "",
            round(element['data']['data_latest_value'], 2),
            _unit if _unit else "",
            _currency if _currency else "",
            _data_year_over_year_diff if _data_year_over_year_diff else "。",
        )
        return element_overview

    @staticmethod
    def get_indicator_overview(region: str, name: str) -> ResponseBase:
        response_tool = ResponseBase(answer="", source="嘉林数据")
        # API请求
        query = "{} {}".format(region, name)
        url = "https://api.garinasset.com/www/v1/searches/indicators"
        params = {"q": query}
        response_api = None

        try:
            response_api = requests.get(url, params=params)
            # 检查响应状态码，如果不是 2xx，会引发异常
            response_api.raise_for_status()
            # 返回响应的 JSON 数据
            response_api = response_api.json()

            indicator_overview = ""

            data_list = response_api['data']
            if data_list:
                for index, element in enumerate(data_list):
                    if index == 0:
                        indicator_overview = ToolWwwGarinassetCom._handle_element(element)
                    elif index == 1:
                        indicator_overview = indicator_overview + "\n\n" + "相关数据：\n" + "\n" + ToolWwwGarinassetCom._handle_element(
                            element)
                    elif index == 6:
                        break
                    else:
                        indicator_overview = indicator_overview + "\n\n" + ToolWwwGarinassetCom._handle_element(element)
                response_tool.answer = indicator_overview
                return response_tool
            else:
                response_tool.answer = "亲爱的，我无法获取该项数据信息，大概是数据商尚没有收录该数据。\n\n当然也可能是我错误理解了你的问题。"
                return response_tool
        except requests.exceptions.HTTPError:
            _status_code = response_api.status_code
            if _status_code == 422:
                logger.warning(f"Exception(requests.exceptions.HTTPError{_status_code}) was encountered when get_indicator_overview({region},{name})")
                response_tool.answer = "亲爱的，我无法提供相关的数据服务，你是否需要修改问题呢？"
                return response_tool
            elif _status_code == 401:
                logger.warning(f"Exception(requests.exceptions.HTTPError[{_status_code}]) was encountered when get_indicator_overview({region},{name})")
                response_tool.answer = "亲爱的，你没有嘉林数据的访问权限，暂时无法给你提供数据响应。"
                return response_tool
            elif _status_code >= 500:
                logger.warning(f"Exception(requests.exceptions.HTTPError[{_status_code}]) was encountered when get_indicator_overview({region},{name})")
                response_tool.answer = "亲爱的，宏微观经济数据库正在升级，暂时无法给你提供响应。"
                return response_tool
            else:
                logger.warning(f"Exception(requests.exceptions.HTTPError[{_status_code}]) was encountered when get_indicator_overview({region},{name})")
                response_tool.answer = "亲爱的，我遇到了未知的网络故障，这需要一定的处理时间。"
                return response_tool
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Exception(requests.exceptions.ConnectionError was encountered when get_indicator_overview({region},{name})")
            response_tool.answer = "亲爱的，我可能失去了宏微观经济数据库服务的网络连接。"
            return response_tool
        except requests.exceptions.RequestException:
            logger.warning(f"Exception(requests.exceptions.RequestException was encountered when get_indicator_overview({region},{name})")
            response_tool.answer = "亲爱的，我明白我现在的处境，程序运行发生了故障哦。"
            return response_tool
