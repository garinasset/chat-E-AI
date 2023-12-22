# 会话记录上下文类，先进先出队列，可定义长度
from collections import deque


class MessagesQueue:
    def __init__(self, max_length):
        self.maxLength = max_length
        self.queue = deque()

    # 添加元素
    def enqueue(self, message):
        if len(self.queue) >= self.maxLength:
            self.queue.popleft()  # 如果队列已满，移除最早的消息
        self.queue.append(message)

    # 添加元素
    def enqueue_user(self, message_content):
        if len(self.queue) >= self.maxLength:
            self.queue.popleft()  # 如果队列已满，移除最早的消息
        message = {"role": "user", "content": message_content}
        self.queue.append(message)

    # 添加元素
    def enqueue_assistant(self, message_content):
        if len(self.queue) >= self.maxLength:
            self.queue.popleft()  # 如果队列已满，移除最早的消息
        message = {"role": "assistant", "content": message_content}
        self.queue.append(message)

    # 弹出元素，先进的先出
    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None
    # 清空队列
    def clear(self):
        self.queue.clear()

    def is_empty(self):
        return len(self.queue) == 0

    def get_length(self):
        return len(self.queue)

    def __str__(self):
        return str(list(self.queue))
