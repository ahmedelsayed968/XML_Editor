from Dictionary import Dictionary
from UserData import DataBase
from Handling_files import read_file

def most_influencer(graph_of_users):
    influencers = []
    max_followers = 0
    for user in graph_of_users.keys:
        followers = len(graph_of_users.get(user))
        if followers > max_followers:
            influencers = [user]
            max_followers = followers
        elif followers == max_followers:
            influencers.append(user)
    return influencers
    

def most_active(graph_of_users):
    follower_counts = Dictionary()
    for user_id, followers_id in graph_of_users.items():
        for follower_id in followers_id:
            if not follower_counts.contains(follower_id):
                follower_counts.add(follower_id, 0)
            follower_counts.add(follower_id, follower_counts.get(follower_id) + 1)
    most_common_follower_id = max(follower_counts.keys, key=lambda x: follower_counts.get(x))
    return most_common_follower_id

def mutual_followers(user1, user2, graph_of_users):
    followers1 = graph_of_users.get(user1)
    followers2 = graph_of_users.get(user2)
    mutual_followers = []
    for follower in followers1:
        if graph_of_users.contains(follower) and followers2.count(follower) > 0 and follower not in [user1, user2]:
            mutual_followers.append(follower)
    return mutual_followers

def followers_of_followers(user_id, graph_of_users):
    result = []
    followers = graph_of_users.get(user_id)
    for follower in followers:
        follower_of_follower = graph_of_users.get(follower)
        if follower_of_follower:
            for f in follower_of_follower:
                if f not in result and f not in followers and f not in [user_id]:
                    result.append(f)
    return result    



if __name__ == '__main__':

    file_string = read_file() #Add file here
    
    users = DataBase.get_users_info(file_string)

    graph_of_users = Dictionary()
    
    for user in users:
        graph_of_users.add(user.id, user.followers)
    #for key in graph_of_users.keys:
    #    print(f"User ID: {key} Followers ID: {graph_of_users.get(key)}")
    
    # print(f" Most Influencer users are: {most_influencer(graph_of_users)}")
    
    # print(f" Most Active user is : {most_active(graph_of_users)}")
    
    # print(f" Mutual followers between {1} and {2} are : {mutual_followers(1,2, graph_of_users)}")
    
    # print(f" Suggested users : {followers_of_followers(1, graph_of_users)}")

