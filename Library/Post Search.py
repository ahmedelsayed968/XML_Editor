from UserData import DataBase
#from Handling_files import read_file

def search_word(users, word):
    result = []
    for user in users:
        for post in user.posts:
            if word in post.body :
                result.append(f"Name of user who published : {user.name}, post :{str(post.body)}")
            if word in post.topics :
                for i in range(len(post.topics)):
                    if word in post.topics[i]:
                        result.append(f"Name of user who published : {user.name}, topic :{str((post.topics)[i])}")
    return result


if __name__ == '__main__':
    # file_string = read_file("D:\Semester 7\DSA\Project DSA\XML_Editor\sample.xml")
    # users = DataBase.get_users_info(file_string)
    # search_result = search_word(users, "economy")
    # for post in search_result:
    #     print(post)
        
    pass