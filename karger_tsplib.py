from cmath import inf
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc

def BoruvkaStep():
    global G
    nodes_to_be_removed = []
    for node in G.nodes:
        minimum_edge, minimum_weight = GetMinimumWeight(node)
        T.add_edge(minimum_edge[0], minimum_edge[1], weight=minimum_weight)
        nodes_to_be_removed.append(Contract(minimum_edge))

    print(nodes_to_be_removed)

    # for j in range(0, len(to_be_contracted)):
    #     try:
    #         new_G = nx.contracted_edge(G, to_be_contracted[j], self_loops=False)
    #     except ValueError: #sometimes the node label may be outdated due to contractions made in the graph
    #         for k in range(0, j):
    #             if (to_be_contracted[k][1] in to_be_contracted[j]):
    #                 if (to_be_contracted[k][1] == to_be_contracted[j][0]):
    #                     to_be_contracted[j] = (to_be_contracted[k][0], to_be_contracted[j][1])
    #                 elif (to_be_contracted[k][1] == to_be_contracted[j][1]):
    #                     to_be_contracted[j] = (to_be_contracted[j][0], to_be_contracted[k][0])
    #         new_G = nx.contracted_edge(G, to_be_contracted[j], self_loops=False)
    #     G = new_G
    #     if (debug == True):
    #         DrawGraph()

def Contract(edge):
    #print(G.edges(nbunch = [edge[0], edge[1]]))
    for j in range(1, len(G.nodes)+1):
        if (j == edge[0]):
            continue
        elif (j == edge[1]):
            continue
        if (G.has_edge(edge[0], j) and G.has_edge(edge[1], j)): #check this TODO
            if (G.get_edge_data(edge[0], j)["weight"] > G.get_edge_data(edge[1], j)["weight"]):
                G[edge[0]][j]['weight']=G[edge[1]][j]['weight']
            G.remove_edge(edge[1], j)

        # if(not G.has_edge(edge[0], j)):
        #     G.add_edge(edge[0], j, weight=)
            DrawGraph()
    return edge[1]

    #minimum_edge, minimum_weight = GetMinimumWeight([edge[0], edge[1]])
    #print(str(minimum_edge) + ", " + str(minimum_weight))

def DrawGraph(): #DRAWING
    global current_suplot
    global G
    my_seed = 6

    pos = nx.spring_layout(G, seed=my_seed)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=160)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=1)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'), font_size=4)

    plt.savefig('savefig/karger/boruvka_steps/subplot_' + str(current_suplot) + '.png', dpi=600)
    plt.clf()

    # posT = nx.spring_layout(original_G, seed=my_seed)
    # nx.draw_networkx_nodes(original_G, posT, node_size=160)
    # nx.draw_networkx_edges(original_G, posT, edgelist=original_G.edges, width=1)
    # nx.draw_networkx_edges(original_G, posT, edgelist=T.edges, width=1, edge_color="green")
    # nx.draw_networkx_labels(original_G, posT, font_size=8, font_family="sans-serif")
    # nx.draw_networkx_edge_labels(original_G, posT, nx.get_edge_attributes(original_G, 'weight'), font_size=4)

    plt.savefig('savefig/karger/mst/subplot_' + str(current_suplot) + '.png', dpi=600)
    plt.clf()

    current_suplot += 1

def ExamineEdge():
    global i

    T.add_edge(edges[0][0], edges[0][1], weight = edges[0][2]) #temporarily adding the edge to the MST

    if (len(nx.cycle_basis(T)) == 0):
        i += 1
        if (debug == True):
            DrawGraph() #DRAWING
    else:
        T.remove_edge(edges[0][0], edges[0][1])

    edges.pop(0)

def GetMinimumWeight(nodes): #returns the edge that has minimum weight out of all edges incident to the passed node(s)
    minimum_weight = inf
    for edge in G.edges(nbunch=nodes):
        if (G.get_edge_data(edge[0], edge[1])["weight"] < minimum_weight):
            minimum_weight = G.get_edge_data(edge[0], edge[1])["weight"]
            minimum_edge = edge
    return minimum_edge, minimum_weight

def GetWeight(u, v):
    return G.get_edge_data(u, v)["weight"]

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

debug = True

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

G = problem.get_graph() #our starting graph
original_G = G
T = nx.Graph() #our minimum spanning tree

for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
    if (G.has_edge(i, i)):
        G.remove_edge(i, i)

tracemalloc.start()

current_suplot = 1

#DRAWING:
if (debug == True):
    DrawGraph()

BoruvkaStep()

#DRAWING:
if (debug == True):
    DrawGraph()

# edges_with_node = []
# lightest_edges = []

# for i in range (1, 102):
#     for edge in edges:
#         if (edge[0] == i or edge[1] == i):
#             edges_with_node.append(edge)
#     edges_with_node.sort(key=GetWeight)
#     lightest_edges.append(edges_with_node[0])
#     edges_with_node = []

# for item in lightest_edges:
#     print(item)

# A = (1, 69)
# B = (2, 57)
# C = (79, 3, 77, 76, 50)
# D = (4, 56, 23, 39, 67, 75, 22, 41, 74)
# E = (17, 84, 5, 60, 18, 52, 83)
# F = (6, 94, 13, 95)
# G = (7, 82, 48, 47, 36, 49)
# H = (46, 8, 45)
# I = (9, 51)
# J = (10, 62)
# K = (64, 11, 19)
# L = (12, 80, 68)
# M = (38, 14, 44)
# N = (15, 43)
# O = (16, 61)
# P = (66, 20, 30, 70)
# Q = (21, 73, 72)
# R = (24, 29)
# S = (31, 88)
# T = (32, 90, 63)
# U = (33, 81)
# V = (34, 78)
# W = (35, 71, 65)
# X = (100, 37, 98)
# Y = (40, 58)
# Z = (42, 87)
# AA = (53, 101)
# AB = (54, 55, 25)
# AC = (93, 59, 92, 97, 99, 96)
# AD = (85, 91)

# graph = (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, AA, AB, AC, AD)

# dict = {
#   A: "A",
#   B: "B",
#   C: "C",
#   D: "D",
#   E: "E",
#   F: "F",
#   G: "G",
#   H: "H",
#   I: "I",
#   J: "J",
#   K: "K",
#   L: "L",
#   M: "M",
#   N: "N",
#   O: "O",
#   P: "P",
#   Q: "Q",
#   R: "R",
#   S: "S",
#   T: "T",
#   U: "U",
#   V: "V",
#   W: "W",
#   X: "X",
#   Y: "Y",
#   Z: "Z",
#   AA: "AA",
#   AB: "AB",
#   AC: "AC",
#   AD: "AD"
# }

# test2 = []

# for i in range(0, len(graph)):
#     for j in range(0, len(graph)):
#         test = []
#         if (i != j):
#             for element in graph[i]:
#                 for other_element in graph[j]:
#                     for edge in edges:
#                         if ((edge[0] == element and edge[1] == other_element) or (edge[0] == other_element and edge[1] == element)):
#                             test.append(edge)
#             test.sort(key=GetWeight)
#             test2.append([str(dict[graph[i]]), str(dict[graph[j]]), test[0]])

# i = 0    

# test3 = []

# for item in dict:
#     for thing in test2:
#         if (thing[0] == dict[item]):
#             test3.append(thing)

#     test3.sort(key=Test)
#     print(test3[0])
#     test3 = []

# for thing in test2:
#     if (thing[0] == 'A'):
#         test3.append(thing)

# test3.sort(key=Test)
# print(test3)

# while(i < len(G.nodes) - 1):
#     ExamineEdge()

print(tracemalloc.get_traced_memory())

tracemalloc.stop()