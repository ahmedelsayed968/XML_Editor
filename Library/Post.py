class Post(object):
    def __init__(self,topics,body):
        self._topics = topics
        self._body = body

    @property
    def topics(self) -> list:
        return self._topics

    @topics.setter
    def topics(self, topic: list):
        self._topics.append(topic)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body: str):
        self._body = body


if __name__ == '__main__':
    pass
