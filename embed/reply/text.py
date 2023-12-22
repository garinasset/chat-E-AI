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
            """获取session"""
            _sess = client.get_session(sess_user_name=_ceaMsg.UserToSession)
            """session 消息入列"""
            _sess.msgQueue.enqueue_user(message_content=_ceaMsg.Content)
            # AI sys messages更新。
            if _sess.ai.msgSysChck:
                if _ceaMsg.Content.startswith("###"):
                    _sess.ai.msgSys = _ceaMsg.Content[3:]
                    _sess.ai.msgSysChck = False
            else:
                if _ceaMsg.Content.startswith("$$$"):
                    _sess.ai.msgSys = OPENAI_SYSTEM_CONTENT
                    _sess.ai.msgSysChck = True
                    client.logger.info("AI System Role：" +  OPENAI_SYSTEM_CONTENT)
                    _sess.msgQueue.clear()
                    """session 消息重新入列"""
                    _sess.msgQueue.enqueue_user(message_content=_ceaMsg.Content)
                elif _ceaMsg.Content.startswith("###"):
                    _sess.ai.msgSys = _ceaMsg.Content[3:]
                    client.logger.info("AI System Role：" + _sess.ai.msgSys)
                else:
                    client.logger.info("AI System Role：" + _sess.ai.msgSys)
            # AI user messages更新。
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
