import logging


class Log:
    def __init__(self, component_name):
        self.logger = logging.getLogger(component_name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - [{}] - %(message)s'.format(component_name))
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
