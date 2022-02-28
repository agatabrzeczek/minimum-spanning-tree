import matplotlib.pyplot as plt
import networkx as nx

def DrawGraph():
    global current_suplot

    subax2 = plt.subplot(subplot_layout[0], subplot_layout[1], current_suplot)

    pos = nx.spring_layout(G, seed=my_seed)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=350)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=T.edges, width=6, edge_color="green")
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'))

    current_suplot += 1

def ExamineEdge():
    T.add_edge(edges[0][0], edges[0][1], weight = edges[0][2]) #temporarily adding the edge to the MST

    if (len(nx.cycle_basis(T)) == 0):
        chosen_edges.append(edges[0])
        DrawGraph()
    else:
        T.remove_edge(edges[0][0], edges[0][1])

    edges.pop(0)

def GetWeight(edge):
    return edge[2]

def SortEdges():
    edge_list = []

    for edge_tuple in G.edges:
        edge = []
        edge.append(edge_tuple[0])
        edge.append(edge_tuple[1])
        edge.append(G[edge[0]][edge[1]]["weight"])
        edge_list.append(edge) #converting from networkx datatype to normal list

    edge_list.sort(key=GetWeight)

    return edge_list

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

edges = SortEdges()

chosen_edges = []

#setup for drawing
my_seed = 2
subplot_layout = (3, 3)
current_suplot = 1

DrawGraph()

while(len(chosen_edges) < len(G.nodes) - 1):
    ExamineEdge()

plt.show()