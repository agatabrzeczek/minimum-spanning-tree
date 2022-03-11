import tsplib95
import matplotlib.pyplot as plt
import networkx as nx

def DrawGraph():
    global current_suplot

    subax2 = plt.subplot(111)

    pos = nx.spring_layout(G, seed=my_seed)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=1)
    nx.draw_networkx_edges(G, pos, edgelist=T.edges, width=1, edge_color="green")
    nx.draw_networkx_labels(G, pos, font_size=2, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'), font_size=2)

    plt.savefig('savefig/subplot_' + str(current_suplot) + '.png', dpi=600)

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

    for edge in edge_list:
        print(edge)

    return edge_list

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/gr17.tsp')

G = problem.get_graph() #our starting graph
T = nx.Graph() #our minimum spanning tree

for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
    if (G.has_edge(i, i)):
        G.remove_edge(i, i)

edges = SortEdges()

chosen_edges = []

#setup for drawing
my_seed = 6
current_suplot = 1

DrawGraph()

while(len(chosen_edges) < len(G.nodes) - 1):
    ExamineEdge()