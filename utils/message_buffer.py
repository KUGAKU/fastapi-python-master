class MessageBufferManager:
    def __init__(self):
        self._message_buffer = []

    def add_to_buffer(self, data: str):
        self._message_buffer.append(data)

    def get_joined_buffer(self):
        return str.join("", self._message_buffer)
