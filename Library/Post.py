class Post(object):
    def __init__(self):
        self._topics = []
        self._body = str()

    @property
    def topics(self) -> list:
        return self._topics

    @topics.setter
    def topics(self, topics: list):
        self._topics = topics

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body: str):
        self._body = body


if __name__ == '__main__':
    pass
