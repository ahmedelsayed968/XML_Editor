class User(object):
    number_of_users = 0

    def __init__(self, name):
        self._Id = int()
        self._name = name
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
    def posts(self, post):
        self._posts = post

    @property
    def followers(self) -> list:
        return self._followers

    @followers.setter
    def followers(self, follower_id: list):
        self._followers = follower_id


if __name__ == '__main__':
    pass
