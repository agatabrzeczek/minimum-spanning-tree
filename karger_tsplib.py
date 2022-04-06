from cmath import inf
import random
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import sys

def BoruvkaStep(G):
    global node_mapping
    #global G
    nodes_to_be_removed = []
    edges_to_be_contracted = []
    for node in G.nodes:
        edges_to_be_contracted.append(GetMinimumEdge(node))

    for edge in edges_to_be_contracted:
        if (G.has_edge(edge[0], edge[1])):
            remapped_edge = RemapEdge(edge)
            #print(remapped_edge_candidates)
            T.add_edge(remapped_edge[0], remapped_edge[1], weight=original_G.get_edge_data(remapped_edge[0], remapped_edge[1])["weight"])
            G.remove_edge(edge[0], edge[1])

    for edge in edges_to_be_contracted:

        node_to_be_removed = Contract(edge)

        if (G.has_node(node_to_be_removed)):
            G.remove_node(node_to_be_removed)

            if (debug == True):
                DrawGraph()

        #G.remove_nodes_from(nodes_to_be_removed)

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
    global node_mapping

    # while (True):
    #     if (mapped_edge[0] in node_mapping):
    #         mapped_edge[0] = node_mapping[mapped_edge[0]]
    #     else:
    #         break

    mapped_edge = MapEdge(edge)

    # while (True):
    #     if (mapped_edge[1] in node_mapping):
    #         mapped_edge[1] = node_mapping[mapped_edge[1]]
    #     else:
    #         break

    if (mapped_edge[0] == mapped_edge[1]): #if this edge has already been contracted, return
        return None
    #print(G.edges(nbunch = [edge[0], edge[1]]))
    #if (mapped_edge[0] in G.nodes and mapped_edge[1] in G.nodes):
    for j in (original_G.nodes):
        if (j in (edge[0], edge[1], mapped_edge[0], mapped_edge[1])):
            continue
        if (G.has_edge(mapped_edge[0], j) and G.has_edge(mapped_edge[1], j)):
            if (G.get_edge_data(min(mapped_edge), j)["weight"] > G.get_edge_data(max(mapped_edge), j)["weight"]):
                G[min(mapped_edge)][j]['weight']=G[max(mapped_edge)][j]['weight']
            G.remove_edge(max(mapped_edge), j)

    if (not ([max(mapped_edge), min(mapped_edge)] in node_mapping)): #DID removed indentation
        node_mapping.append([max(mapped_edge), min(mapped_edge)])

            # if(not G.has_edge(edge[0], j)):
            #     G.add_edge(edge[0], j, weight=)

    return max(mapped_edge)

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

    posT = nx.spring_layout(original_G, seed=my_seed)
    nx.draw_networkx_nodes(original_G, posT, node_size=160)
    #nx.draw_networkx_edges(original_G, posT, edgelist=original_G.edges, width=1)
    nx.draw_networkx_edges(original_G, posT, edgelist=T.edges, width=1, edge_color="green")
    nx.draw_networkx_labels(original_G, posT, font_size=8, font_family="sans-serif")
    nx.draw_networkx_edge_labels(original_G, posT, nx.get_edge_attributes(original_G, 'weight'), font_size=4)

    plt.savefig('savefig/karger/mst/subplot_' + str(current_suplot) + '.png', dpi=600)
    plt.clf()

    pos = nx.spring_layout(G, seed=my_seed)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=160)
    nx.draw_networkx_edges(G, pos, edgelist=H.edges, width=1)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(H, 'weight'), font_size=4)

    plt.savefig('savefig/karger/random_selection/subplot_' + str(current_suplot) + '.png', dpi=600)
    plt.clf()

    current_suplot += 1

def GetMinimumEdge(nodes): #returns the edge that has minimum weight out of all edges incident to the passed node(s)
    minimum_weight = inf
    for edge in G.edges(nbunch=nodes):
        if (G.get_edge_data(edge[0], edge[1])["weight"] < minimum_weight):
            minimum_weight = G.get_edge_data(edge[0], edge[1])["weight"]
            minimum_edge = edge
    return minimum_edge

def MapEdge(edge):
    mapped_edge = [edge[0], edge[1]]
    while (True):
        j = 1
        for k in range(0, len(node_mapping)):
            if (node_mapping[k][0] == mapped_edge[0]):
                mapped_edge[0] = node_mapping[k][1]
                j *= 0
            elif (node_mapping[k][0] == mapped_edge[1]):
                mapped_edge[1] = node_mapping[k][1]
                j *= 0
            else:
                j *= 1
        if (j == 1):
            break
    return mapped_edge

def RemapEdge(edge):
    remapped_edge_candidates = [[edge[0]], [edge[1]]]
    while (True):
        j = 1
        for k in range(0, len(node_mapping)):
            if (node_mapping[k][1] in remapped_edge_candidates[0] and not(node_mapping[k][0] in remapped_edge_candidates[0])):
                remapped_edge_candidates[0].append(node_mapping[k][0])
                j *= 0
            elif (node_mapping[k][1] in remapped_edge_candidates[1] and not(node_mapping[k][0] in remapped_edge_candidates[1])):
                remapped_edge_candidates[1].append(node_mapping[k][0])
                j *= 0
            elif (node_mapping[k][0] in remapped_edge_candidates[0] and not(node_mapping[k][1] in remapped_edge_candidates[0])):
                remapped_edge_candidates[0].append(node_mapping[k][1])
                j *= 0
            elif (node_mapping[k][0] in remapped_edge_candidates[1] and not(node_mapping[k][1] in remapped_edge_candidates[1])):
                remapped_edge_candidates[1].append(node_mapping[k][1])
                j *= 0
            else:
                j *= 1
        if (j == 1):
            break
    
    for node_1 in remapped_edge_candidates[0]:
        for node_2 in remapped_edge_candidates[1]:
            if (G.get_edge_data(edge[0], edge[1])["weight"] == original_G.get_edge_data(node_1, node_2)["weight"]):
                remapped_edge = (node_1, node_2)
    
    return remapped_edge

def RunIteration(graph):
    #print(str(len(T.edges)) + " out of " + str(len(original_G.nodes) - 1))
    BoruvkaStep(graph)
    BoruvkaStep(graph)
    subgraph = SelectEdgesRandomly(graph)
    if (len(T.edges) == (len(original_G.nodes) - 1)):
        print(T.edges)
        print(tracemalloc.get_traced_memory())
        tracemalloc.stop()
        exit()
    RunIteration(subgraph)

def SelectEdgesRandomly(G):
    for edge in G.edges:
        decision = random.randrange(0, 2)
        decision = 1
        #print(decision)
        if (decision == 1):
            H.add_edge(edge[0], edge[1], weight=G.get_edge_data(edge[0], edge[1])["weight"])

    if (debug == True):
        DrawGraph()

    return H

debug = False

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/swiss42.tsp')

G = problem.get_graph() #our starting graph
T = nx.Graph() #our minimum spanning tree
H = nx.Graph() #after random selection

for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
    if (G.has_edge(i, i)):
        G.remove_edge(i, i)

original_G = G.copy()

tracemalloc.start()

current_suplot = 1
node_mapping = []

#DRAWING:
if (debug == True):
    DrawGraph()

RunIteration(G)

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