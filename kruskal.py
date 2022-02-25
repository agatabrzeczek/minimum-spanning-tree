import matplotlib.pyplot as plt
import networkx as nx

def DrawGraph():
    global current_suplot

    subax2 = plt.subplot(subplot_layout[0], subplot_layout[1], current_suplot)

    pos = nx.spring_layout(G, seed=my_seed)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_graph, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_tree, width=6, edge_color="green")
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'))

    current_suplot += 1

def FindLightestEdge(edge_list):

    while (True):
        lightest_edge = ['', '', float("inf")] #initial value

        for edge in edge_list: #finding the lightest edge
            if (edge[2] < lightest_edge[2]):
                lightest_edge = edge

        T.add_edge(lightest_edge[0], lightest_edge[1], weight = lightest_edge[2]) #adding edge to a tree (we haven't checked if it's going to create a cycle yet)

        for i in range(0, len(edge_list)): #it doesn't matter if the edge creates a cycle or not - it is not going to be taken into consideration anymore
            if (edge_list[i] == lightest_edge):
                edges.pop(i)
                break

        if(len(nx.cycle_basis(T)) > 0):
            T.remove_edge(lightest_edge[0], lightest_edge[1]) #if the edge that we just added created a cycle - remove it from the tree
        else:
            break #if the edge that we just added didn't create a cycle this is the end of our search

    return lightest_edge

G = nx.Graph() #our starting graph
T = nx.Graph() #our minimum spanning tree

G.add_edge("a", "b", weight=2)
G.add_edge("a", "c", weight=3)
G.add_edge("a", "d", weight=3)
G.add_edge("b", "c", weight=4)
G.add_edge("b", "e", weight=3)
G.add_edge("c", "d", weight=5)
G.add_edge("c", "e", weight=1)
G.add_edge("d", "f", weight=7)
G.add_edge("e", "f", weight=8)
G.add_edge("f", "g", weight=9)

edges = []

for edge_tuple in G.edges:
    edge = []
    edge.append(edge_tuple[0])
    edge.append(edge_tuple[1])
    edge.append(G[edge[0]][edge[1]]["weight"])
    edges.append(edge) #converting from networkx datatype to normal list

#setup
my_seed = 2
subplot_layout = (3, 3)
current_suplot = 1
edges_in_tree = []
edges_in_graph = edges[:]

while(True):

    DrawGraph()

    edges_in_tree.append(FindLightestEdge(edges))

    if (nx.number_of_nodes(G) == nx.number_of_nodes(T)):
        break

DrawGraph()

plt.show()