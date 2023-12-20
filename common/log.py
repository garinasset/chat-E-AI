import logging

from config.develop import SYSTEM_LOG_LEVEL


class LogUtils:

    @staticmethod
    def new_logger(component_name):
        _logger = logging.getLogger(component_name)
        _is_logger_exist = len(_logger.handlers) > 0
        if _is_logger_exist:
            return _logger
        else:
            _logger.setLevel(SYSTEM_LOG_LEVEL)
            _formatter = logging.Formatter('%(asctime)s - %(levelname)s - [{}] - %(message)s'.format(component_name))
            _console_handler = logging.StreamHandler()
            _console_handler.setLevel(SYSTEM_LOG_LEVEL)
            _console_handler.setFormatter(_formatter)
            _logger.addHandler(_console_handler)
        return _logger


