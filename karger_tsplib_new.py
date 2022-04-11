from cmath import inf
import random
from numpy import maximum
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import sys

def BoruvkaStep(edge_list):
    #starting edges are edges at the start of whole program, original edges are edges at the start of boruvka step
    global starting_edges
    original_edges = [x[:] for x in edge_list] #copy list of lists

    node_list = [] #deriving node list from edge list
    for edge in edge_list:
        if (edge[0] not in node_list and edge[2] != None):
            node_list.append(edge[0])
        if (edge[1] not in node_list and edge[2] != None):
            node_list.append(edge[1])

    edges_to_be_contracted = []
    for node in node_list:
        weight = inf
        edge_to_be_contracted = []
        for edge in edge_list:
            if (node in [edge[0], edge[1]] and edge[2] != None):
                if (edge[2] < weight):
                    edge_to_be_contracted = edge.copy()
                    weight = edge[2]
        if (edge_to_be_contracted not in edges_to_be_contracted):
            edges_to_be_contracted.append(edge_to_be_contracted)

    for edge_to_be_contracted in edges_to_be_contracted:
        for i in range(0, len(edge_list)): #deleting edges to be contracted from edge list
            edge_nodes = [edge_list[i][0], edge_list[i][1]]
            if (edge_to_be_contracted[0] in edge_nodes):
                if (edge_to_be_contracted[1] in edge_nodes):
                    edge_list[i][2] = None

    tree_index_list = []
    for edge_to_be_contracted in edges_to_be_contracted:

        for i in range(0, len(original_edges)): #mapping edge
            edge_nodes = [original_edges[i][0], original_edges[i][1]]
            if (edge_to_be_contracted[0] in edge_nodes):
                if (edge_to_be_contracted[1] in edge_nodes):
                    edge_to_be_contracted = edge_list[i].copy()
                    tree_index_list.append(i)

        edges_to_be_updated = []
        for edge in edge_list: #gathering all the edges which have to be updated
            if (edge[2] != None):
                edge_nodes = [edge[0], edge[1]]
                if (edge_to_be_contracted[0] in edge_nodes):
                    if (edge_to_be_contracted[1] in edge_nodes):
                        edge[2] = None 
                    else:
                        edges_to_be_updated.append(edge)
                elif (edge_to_be_contracted[1] in edge_nodes):
                    edges_to_be_updated.append(edge)

        for node in node_list:
            compared_edges = []
            if (node in [edge_to_be_contracted[0], edge_to_be_contracted[1]]):
                continue
            else:
                for edge in edges_to_be_updated:
                    edge_nodes = [edge[0], edge[1]]
                    if (node in edge_nodes):
                        compared_edges.append(edge)
            if (len(compared_edges) == 0):
                continue
            else:
                if (len(compared_edges) == 2 and compared_edges[0][2] == compared_edges[1][2]): #if both edges have the same weight, just throw away the one with the greater node
                    for i in range(0, len(edge_list)):
                        edge_nodes = [edge_list[i][0], edge_list[i][1]]
                        if (node in edge_nodes):
                            if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                                edge_list[i][0] = min([edge_to_be_contracted[0], edge_to_be_contracted[1]])
                                edge_list[i][1] = node
                                edge_list[i][2] = None
                else:
                    if (len(compared_edges) == 1):
                        new_weight = compared_edges[0][2]
                    elif (compared_edges[0][2] < compared_edges[1][2]):
                        new_weight = compared_edges[0][2]
                    else:
                        new_weight = compared_edges[1][2]
                    for i in range(0, len(edge_list)): #updating edges
                        edge_nodes = [edge_list[i][0], edge_list[i][1]]
                        if (node in edge_nodes):
                            if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                                edge_list[i][0] = min([edge_to_be_contracted[0], edge_to_be_contracted[1]])
                                edge_list[i][1] = node
                                if (edge_list[i][2] != new_weight):
                                    edge_list[i][2] = None
                            elif (min([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                                if (edge_list[i][2] != new_weight):
                                    edge_list[i][2] = None

    tree_edges = []
    for edge in edges_to_be_contracted:
        for i in range(0, len(edge_list)):
            if (original_edges[i] == edge):
                tree_edges.append(starting_edges[i])

    if (debug == True):
        DrawGraph(G)

    return edge_list, tree_edges

def DeleteFHeavyEdges(graph, forest):

    networkx_forest = nx.Graph()
    for edge in forest:
        networkx_forest.add_edge(edge[0], edge[1], weight = edge[2])

    for edge in graph:
        if (edge[2] != None):
            maximum_weight = 0
            weight_graph = edge[2]
            if (nx.has_path(networkx_forest, edge[0], edge[1])):
                path = nx.shortest_path(networkx_forest, source=edge[0], target=edge[1])
                for i in range(0, (len(path)-1)):
                    weight_forest = networkx_forest.get_edge_data(path[i], path[i+1])["weight"]
                    if (weight_forest > maximum_weight):
                        maximum_weight = weight_forest
            else:
                maximum_weight = inf
            if (weight_graph > maximum_weight):
                edge[2] = None

    return graph

def DrawGraph(G): #DRAWING
    global current_suplot
    #global G
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

def SelectRandomEdges(edge_list):
    selected_edges = []

    for edge in edge_list:
        decision = random.randrange(0, 2)
        if (decision == 1):
            selected_edges.append(edge)
        else:
            selected_edges.append([edge[0], edge[1], None])

    return selected_edges

def Run(edge_list):
    node_list = [] #deriving node list from edge list
    for edge in edge_list:
        if (edge[0] not in node_list and edge[2] != None):
            node_list.append(edge[0])
        if (edge[1] not in node_list and edge[2] != None):
            node_list.append(edge[1])

    all_done = False #if True the MST has been computed
    tree_edges = [] #we will be adding to this tree w each iteration
    graph_before_random_selection = []
    while (all_done == False):
        done = False #if true the MSF of subgraph has been computed
        while (done == False):
            contracted_G, new_tree_edges = BoruvkaStep(edge_list) #first Boruvka step
            tree_edges += new_tree_edges

            edge_list = contracted_G
            contracted_G, new_tree_edges = BoruvkaStep(edge_list) #second Boruvka step
            tree_edges += new_tree_edges

            if (len(graph_before_random_selection) == 0):
                graph_before_random_selection = [x[:] for x in contracted_G]

            subgraph_H = SelectRandomEdges(contracted_G)

            done = True #first we assume that the tree is completed...
            for edge in contracted_G:
                if (edge[2] != None):
                    done = False #...and if not, we reset the flag to False
                    edge_list = subgraph_H
                    break
        
        contracted_G = DeleteFHeavyEdges(graph_before_random_selection, tree_edges)
        edge_list = contracted_G

        if (len(tree_edges) == (len(node_list) - 1)):
            print(tree_edges)
            all_done = True

debug = False

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/gr96.tsp')

G = problem.get_graph() #our starting graph
#original_G = G.copy()

for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
    if (G.has_edge(i, i)):
        G.remove_edge(i, i)

tracemalloc.start()

G_edges = [] #converting networkx graph to list of edges
for edge in G.edges:
    G_edges.append([edge[0], edge[1], G.get_edge_data(edge[0], edge[1])["weight"]])
starting_edges = [x[:] for x in G_edges]

G_nodes = G.nodes

#DRAWING:
if (debug == True):
    DrawGraph(G)

Run(G_edges)

#DRAWING:
if (debug == True):
    DrawGraph(G)