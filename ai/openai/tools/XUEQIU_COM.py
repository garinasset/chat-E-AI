import pysnowball
from timeout_decorator import timeout_decorator

from common.log import LogUtils
from models.response import ResponseBase
from models.xueqiu import XueQiu

logger = LogUtils.new_logger("toolXueqiuCom")

class ToolXueqiuCom(object):
    TOOL_MODEL = {
        # 工具模型类型,必填，目前API支持 function
        "type": "function",
        "function": {
            # 函数名称，必填
            "name": "get_stock",
            # 函数描述，必填
            "description": "获取给定股票代码的股票信息，如果获取不到股票代码询问市场及代码。",
            # 函数参数，必填。
            "parameters": {
                "type": "object",
                # JSON键类型，及描述。
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "股票名称",
                    },
                    "symbol": {
                        "type": "string",
                        "description": "股票代码，上海市场前缀有SH，例如：SH600104；深圳市场前有缀SZ，例如：SZ300315；香港市场代码为五位数字，没有前缀，不足五位前面补'0'，例如腾讯代码是‘00700’；其他市场保持原样，例如美国市场苹果：AAPL。",
                    },
                },
                "required": ["name", "symbol"],
            },
        }
    }

    @staticmethod
    @timeout_decorator.timeout(8)
    def get_stock(name: str, symbol: str) -> ResponseBase:
        response_tool = ResponseBase(answer="", source="xueqiu•com")
        _stock = ''
        try:
            _quote = pysnowball.quotec(symbols=symbol)
            _quoteD = _quote['data'][0]
            _xueQiu = XueQiu.model_construct()
            if _quoteD:
                _xueQiu = XueQiu(**_quoteD)
                _percent = ''
                if _xueQiu.percent:
                    _percent = ("下跌" + str(_xueQiu.percent) + '%,') if _xueQiu.percent <0 else ("上涨+" + str(_xueQiu.percent) + '%,')
                else:
                    _percent = ''

                _stock = "{},代码{}。{}{}{}{}{}{}{}".format(
                    name,
                    _xueQiu.symbol,
                    ("当前股价" + str(_xueQiu.current)) if _xueQiu.current else '当前股价未获得',
                    '(交易中),' if _xueQiu.is_trade else '(不在交易状态),',
                    _percent,
                    ("成交金额" + str(_xueQiu.amount)+ '。') if _xueQiu.amount else '。',
                    ("目前总市值" + str(_xueQiu.market_capital) + ',') if _xueQiu.market_capital else '',
                    ("流动市值"+ str(_xueQiu.float_market_capital) + '。') if _xueQiu.float_market_capital else '',
                    ("该股票年初至今涨跌" + str(_xueQiu.current_year_percent) + '%。') if _xueQiu.current_year_percent else '',
                )
            else:
                raise ValueError
            response_tool.answer = _stock
        except ValueError:
            logger.warning(f'Exception(ValueError) was encountered when get_stock({symbol})')
            response_tool.answer = "亲爱的，你能告诉我股票所在市场以及股票代码吗？这样可以增进我的理解。"
        except timeout_decorator.TimeoutError:
            logger.warning(f'Exception(timeout_decorator.TimeoutError) was encountered when get_stock({symbol})')
            response_tool.answer = "亲爱的，访问xueqiu•com服务超时，请在使用过程中保持节制。"
        return response_tool