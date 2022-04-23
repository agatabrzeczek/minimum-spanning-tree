import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import time
import math

def DrawGraph(): #DRAWING
    global current_suplot

    subax2 = plt.subplot(111)

    pos = nx.spring_layout(G, seed=my_seed)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=160)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=1)
    nx.draw_networkx_edges(G, pos, edgelist=T.edges, width=1, edge_color="green")
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'), font_size=4)

    plt.savefig('savefig/kruskal/subplot_' + str(current_suplot) + '.png', dpi=600)

    current_suplot += 1

def ExamineEdge(edge, T):

    T.add_edge(edge[0], edge[1], weight = edge[2]) #temporarily adding the edge to the MST

    if (len(nx.cycle_basis(T)) == 0):
        return True, T
    else:
        T.remove_edge(edge[0], edge[1])
        return False, T

def GetWeight(edge):
    return edge[2]

def Run(G):
    T = nx.Graph() #our minimum spanning tree

    for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
        if (G.has_edge(i, i)):
            G.remove_edge(i, i)

    percentage = 0

    start_time = time.time()
    tracemalloc.start()

    edges = SortEdges(G)

    i = 0
    while(i < len(G.nodes) - 1):
        added, T = ExamineEdge(edges[0], T)
        if (added == True):
            i += 1

            old_percentage = percentage
            percentage = math.floor((len(T.edges)/(len(G.nodes) - 1))*100)
            if (old_percentage != percentage):
                print(f"The MST is {percentage}% done.")

        edges.pop(0)

    end_time = time.time()
    memory_consumption = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return T, round(end_time - start_time, 3), memory_consumption

def SortEdges(G):
    edge_list = []

    for edge_tuple in G.edges:
        edge = []
        edge.append(edge_tuple[0])
        edge.append(edge_tuple[1])
        edge.append(G[edge[0]][edge[1]]["weight"])
        edge_list.append(edge) #converting from networkx datatype to normal list

    edge_list.sort(key=GetWeight)

    return edge_list

# debug = False

# problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

# G = problem.get_graph() #our starting graph
# T = nx.Graph() #our minimum spanning tree

# for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
#     if (G.has_edge(i, i)):
#         G.remove_edge(i, i)

# tracemalloc.start()

# i = 0

# #DRAWING:
# if (debug == True):
#     my_seed = 6
#     current_suplot = 1
#     DrawGraph()

# Run(G)

# print(tracemalloc.get_traced_memory())

# tracemalloc.stop()