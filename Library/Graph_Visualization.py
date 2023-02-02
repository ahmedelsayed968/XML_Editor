#Graph Visualization
from UserData import DataBase
from Handling_files import read_file
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

class GraphVisualizer:
    def __init__(self, users):
        #  Read the XML file using the read_file method and store the result in a variable
        # self.file_string = read_file(file_path)

        #  Get the user information using the DataBase class
        self.users = users

        
        self.user_id_dict = {user.id: f"{user.id}\n{user.name}" for user in self.users}
        self.graph = {user.id: user.followers for user in self.users}

    def draw_graph(self):
        
        G = nx.DiGraph(self.graph)

        pos = nx.spring_layout(G)
        # Draw the nodes, edges, and labels using networkx's draw functions
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, node_shape='o', alpha=0.5)
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=1, arrowstyle='<|-', arrowsize=15, connectionstyle='arc3,rad=0.07')
        nx.draw_networkx_labels(G, pos, labels=self.user_id_dict, font_size=7, font_color='black')
        plt.show()
        # renderer = fig.canvas.get_renderer()

        # Draw the plot
        # fig.draw(renderer)

        # Get the binary representation of the image as a NumPy array
        # img = np.frombuffer(renderer.tostring_rgb(), dtype=np.uint8)
        # img = img.reshape(renderer.height, renderer.width, 3)
        # return img

# if __name__ == "__main__":
    # users_graph = GraphVisualizer(r"path")
    # users_graph.draw_graph()
    # pass
