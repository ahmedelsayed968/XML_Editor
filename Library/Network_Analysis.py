from UserData import DataBase
from Handling_files import read_file


class NetworkAnalysis:
    def __init__(self, file_string):
        # Initialize the graph of users using data from the database
        self.users = DataBase.get_users_info(file_string)
        self.user_id_dict = {user.id: user.name for user in self.users}
        self.graph_of_users = {user.id: user.followers for user in self.users}
        
        #to test only
        #self.graph_of_users={1: [1,6], 2: [2, 3,6], 3: [1,6],4:[1,2,3,5,6],5:[6],6:[]}
            
    def print_graph_of_users(self):
        print(self.graph_of_users)
        
    def most_influencer(self):
        # Find the users with the most followers
        influencers = []
        max_followers = 0
        for user in self.graph_of_users.keys():
            followers = len(self.graph_of_users[user])
            if followers > max_followers:
                influencers = [user]
                max_followers = followers
            elif followers == max_followers:
                influencers.append(user)
        return influencers

    def most_active(self):
        # Find the user who follows most users
        following_counts = {}
        for user_id, followers_id in self.graph_of_users.items():
            for follower_id in followers_id:
                if follower_id not in following_counts:
                    following_counts[follower_id] = 0
                following_counts[follower_id] += 1
        most_active = max(following_counts, key=lambda x: following_counts[x])
        return most_active


    def mutual_followers(self, user1, user2):
        try:
            #Handle exception if a user not exist in the graph
            followers1 = self.graph_of_users[user1]
            followers2 = self.graph_of_users[user2]
        
        except KeyError:
            print(f"One of the user IDs {user1} or {user2} is not in the graph of users.")
            return []
        
        # Find the mutual followers of two users
        mutual_followers = []
        for follower in followers1:
            if follower in self.graph_of_users and follower in followers2 and follower not in [user1, user2]:
                mutual_followers.append(follower)
        return mutual_followers


    def followers_of_followers(self, user_id):
        try:
            #catch an exception is user index not in the graph
            followers = self.graph_of_users[user_id]
        except KeyError:
            print(f"User with ID {user_id} not found in the graph")
            return []
        # Find the followers of followers of a user
        result = []
        for follower in followers:
            follower_of_follower = self.graph_of_users.get(follower, [])
            for f in follower_of_follower:
                if f not in result and f not in followers and f not in [user_id]:
                    result.append(f)
        return result
    
    
if __name__ == '__main__':
    # file_string = read_file(r"path")
    # network_analysis = NetworkAnalysis(file_string)
    # network_analysis.print_graph_of_users()
    # user_id_dict = network_analysis.user_id_dict
    # print(" User ID and Name mapping:")
    # print(user_id_dict)

    # print(f" Most Influencer users are: {[user_id_dict[user_id] for user_id in network_analysis.most_influencer()]}")
    # print(f" Most Active user is : {user_id_dict[network_analysis.most_active()]}")
    # print(f" Mutual followers between {3} and {4} are : {[user_id_dict[user_id] for user_id in network_analysis.mutual_followers(3, 4)]}")
    # print(f" Suggested users for user {6} : {[user_id_dict[user_id] for user_id in network_analysis.followers_of_followers(6)]}")
    pass