from embed.utils.suffix import EUtilsSuffix
from models.messages import MessageCea
from models.send import Send
from utils.string import UtilsString


class EReplyText:
    @staticmethod
    def reply(client, message: MessageCea) -> Send:
        _ceaMsg = message
        _action = _ceaMsg.Action
        _send = Send.model_construct()
        if _action:
            # 记录日志
            client.logger.info(f'Message Signal RX: {_ceaMsg.UserToSession} {UtilsString.log_msg(_ceaMsg.Content)}')
            """获取session"""
            _sess = client.get_session(sess_user_name=_ceaMsg.UserToSession)
            # CMD命令检测
            if _ceaMsg.Content.startswith("#系统提示"):
                _ceaMsg.Content = _ceaMsg.Content[5:]
                _sess.ai.cmdModel = True
                _sess.ai.cmdString = '系统提示'
                client.logger.info("CMD - AI System Role：" + UtilsString.get_omitted_text(_ceaMsg.Content))
            elif _ceaMsg.Content.startswith("#账单查询"):
                _ceaMsg.Content = _ceaMsg.Content[5:]
                _sess.ai.cmdModel = True
                _sess.ai.cmdString = '账单查询'
                client.logger.info("CMD - Billing")
            elif _ceaMsg.Content.startswith("#恢复出厂"):
                _ceaMsg.Content = _ceaMsg.Content[5:]
                _sess.ai.cmdModel = True
                _sess.ai.cmdString = '恢复出厂'
                client.logger.info("CMD - AI Factory Reset")
            """user messages入列"""
            _sess.msgQueue.enqueue_user(message_content=_ceaMsg.Content)
            # AI user messages更新。
            _sess.ai.msgUserAssi = _sess.msgQueue.queue
            """AI调用"""
            _sess.ai.response()
            _rspAi = _sess.ai.responseAI
            """messages后置处理"""
            _rspAns = _rspAi.answer
            if not _rspAns.startswith("CMD"):
                """assistant messages入列。"""
                _sess.msgQueue.enqueue_assistant(message_content=_rspAns)
                """会话实例中的OpenAI实例 messages更新。"""
                _sess.ai.msgUserAssi = _sess.msgQueue.queue
            # 添加前后缀
            # client.logger.debug({"MessageCea":_ceaMsg})
            _contentOutput = f'@{_ceaMsg.NickName}\n{EUtilsSuffix.add_suffix(_rspAi)}' if _ceaMsg.IsGroup else EUtilsSuffix.add_suffix(
                _rspAi)
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
