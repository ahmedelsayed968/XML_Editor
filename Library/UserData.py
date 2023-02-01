from User import User
import re
from Handling_files import read_file
from Post import Post
class DataBase:
    file_string = None

    def __init__(self):
        pass

    @classmethod
    def get_users_info(self, list_tokens):
        """
        input: take file as list of tokens
        return : list of users
        """
        if not DataBase.file_string:
            self.file_string = ''.join(list_tokens)  # to join list of tokens to string_file

        names = self.__get_names(self)  # return list of mentioned names in the file
        ids = self.__get_ids(self)  # return all ids mentioned
        users = self.__initialize_list_of_user(self, names, ids)  # initialize our list of users by names and ids
        list_of_followers = self.__followers(self)  # get the followers for each user

        for index, user in enumerate(users):  # to set followers for each user object
            user.followers = list(list_of_followers[index])

        posts = self.__get_posts(self)  # return all list of posts but with tags

        list_of_posts = self.__getPosts(self, posts)  # get list of posts filtered from the tags
        for index, posts in enumerate(list_of_posts):  # assign list of posts to each user
            users[index].posts = posts

        return users

    def __get_names(self):
        names = re.findall('<name>(.+?)[<?.+>|<\/?.+>]', DataBase.file_string, re.DOTALL)
        return names

    def __get_ids(self):
        ids = re.findall("<id>(.*?)</id>", DataBase.file_string, re.DOTALL)
        return ids

    def __initialize_list_of_user(self, names, ids):
        list_of_users = []
        for i in range(len(names)):
            list_of_users.append(User(str(names[i])))

        for i in range(len(names)):
            try:
                list_of_users[i].id = int(ids[i])
            except:
                print('Wrong format')
        return list_of_users

    def __followers(self):
        followers_list = self.__get_followers(self)
        list_of_followers = []
        for f in followers_list:
            followers_of_user = self.__filter_follower(self, f)
            followers_of_user = [int(i) for i in followers_of_user]
#             print(followers_of_user)
            list_of_followers.append(followers_of_user)
        return list_of_followers

    def __get_followers(self):
        followers = re.findall("<followers>(.*?)</followers>", DataBase.file_string)
        return followers

    def __filter_follower(self, followers):
        return re.findall('<follower><id>(.+?)[<?.+>|<\/?.+>]', followers)

    def __get_posts(self):
        return re.findall("<posts>(.*?)<\/posts>", DataBase.file_string, re.DOTALL)

    def __getPosts(self, posts):
        list_of_list_of_posts = []
        for post in posts:
            list_Posts = []
            body_of_each_post_for_user_i = self.__get_body(self, post)
            topics_of_i = self.__get_topics(self, post)
            for index, topics_of_post in enumerate(topics_of_i):
                topics_of_post_list = self.__filter_topics(self, topics_of_post)
                list_Posts.append(Post(topics_of_post_list, body_of_each_post_for_user_i[index]))
            list_of_list_of_posts.append(list_Posts)
        return list_of_list_of_posts

    def __get_body(self, post):
        list_bodies = re.findall('<body>(.+?)[<?.+>|<\/?.+>]', post)
        return list_bodies

    def __get_topics(self, posts):
        topics_per_post = re.findall('<topics>(.+?)</topics>', posts)
        return topics_per_post

    def __filter_topics(self, topics):
        return re.findall('<topic>(.+?)[<?.+>|<\/?.+>]', topics)


if __name__ == '__main__':
    # Test Code
    # file_string = read_file()
    # users = DataBase.get_users_info(file_string)
    # for user in users:
    #     print(f'Id: {user.id}, Name: {user.name}')
    #     print(f'#Followers: {len(user.followers)} , Followers ID -> {user.followers}')
    #     print(f'#Posts: {len(user.posts)} ')
    #     for index, post in enumerate(user.posts):
    #         print(f'body of Post #{index + 1}\n{post.body}')
    #         print(f'#Topics of Post #{index + 1}: {len(post.topics)}')
    #         print(f'Topics : {post.topics}')
    pass
