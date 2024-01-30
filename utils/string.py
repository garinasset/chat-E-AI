class UtilsString:

    @staticmethod
    def log_msg(input_string) -> str:
        # 去除换行符
        processed_string = input_string.replace('\n', '')
        # 去除\u2005
        processed_string = processed_string.replace('\u2005', ' ')
        # 如果字符串长度大于16，使用省略号代替后面的部分
        if len(processed_string) > 16:
            processed_string = processed_string[:16] + '...'

        return processed_string

    @staticmethod
    def get_omitted_text(input_string) -> str:
        # 去除换行符
        processed_string = input_string.replace('\n', '')
        # 如果字符串长度大于16，使用省略号代替后面的部分
        if len(processed_string) > 16:
            processed_string = processed_string[:16] + '...'

        return processed_string
