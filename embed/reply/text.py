from config.settings import OPENAI_SYSTEM_CONTENT
from embed.utils.suffix import EUtilsSuffix
from models.messages import MessageCea
from models.send import Send
from utils.string import UtilsString

class EReplyText:
    @staticmethod
    def reply(client, message:MessageCea) -> Send:
        _ceaMsg = message
        _action = _ceaMsg.Action
        _send =  Send.model_construct()
        if _action:
            # 记录日志
            client.logger.info(f'Message Signal RX: {_ceaMsg.UserToSession} {UtilsString.log_msg(_ceaMsg.Content)}')
            """messages前置处理"""
            _sess = client.get_session(sess_user_name=_ceaMsg.UserToSession)
            # 会话实例user messages入列
            _sess.msgQueue.enqueue_user(message_content=_ceaMsg.Content)
            # AI实例messages更新。
            _sess.ai.msgSys = _ceaMsg.Content[3:] if _ceaMsg.Content.startswith("###") else OPENAI_SYSTEM_CONTENT
            _sess.ai.msgUserAssi = _sess.msgQueue.queue
            """AI调用"""
            _sess.ai.response()
            _rspAi = _sess.ai.responseAI
            _rspAns = _rspAi.answer
            """messages后置处理"""
            _sess.msgQueue.enqueue_assistant(message_content=_rspAns)
            """assistant messages入列。"""
            _sess.ai.msgUserAssi = _sess.msgQueue.queue
            """会话实例中的OpenAI实例 messages更新。"""
            # 添加前后缀
            # client.logger.debug({"MessageCea":_ceaMsg})
            _contentOutput = f'@{_ceaMsg.NickName}\n{EUtilsSuffix.add_suffix(_rspAi)}' if _ceaMsg.IsGroup else EUtilsSuffix.add_suffix(_rspAi)
            # 返回
            _send.content = _contentOutput
            _send.user = _ceaMsg.UserToReply
            _send.action = True
            # client.logger.debug(_send)
            # 记录日志
            client.logger.info(f'Message Signal TX: {_ceaMsg.UserToSession} {UtilsString.log_msg(_contentOutput)}')
        else:
            pass
        return _send
