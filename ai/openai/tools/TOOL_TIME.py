from datetime import datetime, timedelta

from common.log import LogUtils
from models.response import ResponseBase

"""开发者规范"""
"""开发Tools工具详细步骤："""
"""1、创建logger日志实例，用以记录潜在异常。参照：logger = LogUtils.new_logger("OpenAI-toolTime")"""
"""2、创建Tools工具类 例如class ToolTime(object):"""
"""3、创建一个名为"TOOL_MODEL"的字典，字典中可编辑的键值已在下方示例中注释列出，其他不可编辑。注意字典格式！"""
"""4、创建一个工具函数，返回值为ResponseBase模型。注意函数名和"TOOL_MODEL"字典中的name值保持一致，示例中为get_time，上下一致"""
"""5、实现工具函数，返回相应答复。"""
"""6、在/ai/openai/tools/tools.py中的OpenAITools类中的代码最下方增加case，以注册Tools工具类。观察规律，很好填写。"""
"""7、在/config/settings.py中的 OPENAI_TOOLS_CONFIG 数组中增加一条配置。"""
"""8、运行调试"""

logger = LogUtils.new_logger("OpenAI-toolTime")


class ToolTime(object):
    TOOL_MODEL = {
        "type": "function",
        "function": {

            # [必填：value可编辑]，注意所有Tools中保持唯一，且和下方的静态方法函数保持命名一致。
            "name": "get_time",

            # [必填：value可编辑]，工具功能介绍。
            "description": "获取指定地理位置的时间，如果未指定，默认为北京时间",

            "parameters": {
                "type": "object",

                # [必填：value]，联网工具参数。如果有参数，参照下方，自行配置增添所需参数，如果没有参数，则使用 "properties": {}, 。
                "properties": {
                    # [选填：key可编辑]，具体所需参数。
                    "location": {
                        # [必填：value可编辑]，参数类型
                        "type": "string",
                        # [必填：value可编辑]，参数描述。
                        "description": "中文地理位置。",
                    },
                    "offset_hours": {
                        # [必填：value可编辑]，参数类型
                        "type": "string",
                        # [必填：value可编辑]，参数描述。
                        "description": "该位置与UTC的小时偏移量，数字形式",
                    },
                },

                # [选填]，需要OpenAI必须返回的参数，则在下方数组中指定。如果不需要，则使用 "required": [], 。
                "required": ["location", "offset_hours"],
            },
        }
    }

    @staticmethod
    def get_time(location: str, offset_hours: str) -> ResponseBase:
        response_tool = ResponseBase(answer="", source="Time")

        # 获取当前时间（UTC）
        current_time = datetime.utcnow()

        # 计算指定偏移量的时间
        offset = timedelta(hours=int(offset_hours))
        target_time = current_time + offset

        # 格式化时间
        format_time = target_time.strftime("%Y-%m-%d, %A, %H:%M:%S")
        response_tool.answer = "{}时间，{}".format(location, format_time)

        return response_tool
