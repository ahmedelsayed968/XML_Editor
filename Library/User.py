import Post


class User(object):
    number_of_users = 0

    def __init__(self):
        self._Id = int()
        self._name = str()
        self._posts = []
        self._followers = []
        User.number_of_users += 1

    @property
    def id(self) -> int:
        return self._Id

    @id.setter
    def id(self, id: int):
        self._Id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def posts(self) -> list:
        return self._posts

    @posts.setter
    def posts(self, posts):
        self._posts = posts

    @property
    def followers(self) -> list:
        return self._followers

    @followers.setter
    def followers(self, followers: list):
        self._followers = followers


if __name__ == '__main__':
    pass
