from cmath import inf
import random
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import math

def BoruvkaStep(edge_list, starting_edges):
    #starting edges are edges at the start of whole program, original edges are edges at the start of boruvka step
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
            edge_weight = original_edges[i][2]
            if (edge_to_be_contracted[0] in edge_nodes and edge_weight != None):
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
            if (len(compared_edges) == 0): #DID
                for i in range(0, len(edge_list)):
                    edge_nodes = [edge_list[i][0], edge_list[i][1]]
                    if (node in edge_nodes):
                        if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                            edge_list[i][0] = min([edge_to_be_contracted[0], edge_to_be_contracted[1]])
                            edge_list[i][1] = node
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

    return edge_list, tree_edges

def Run(G):

    for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
        if (G.has_edge(i, i)):
            G.remove_edge(i, i)

    edge_list = [] #converting networkx graph to list of edges
    for edge in G.edges:
        edge_list.append([edge[0], edge[1], G.get_edge_data(edge[0], edge[1])["weight"]])
    starting_edges = [x[:] for x in edge_list]

    node_list = [] #deriving node list from edge list
    for edge in edge_list:
        if (edge[0] not in node_list and edge[2] != None):
            node_list.append(edge[0])
        if (edge[1] not in node_list and edge[2] != None):
            node_list.append(edge[1])

    tree_edges = [] #we will be adding to this tree w each iteration
    done = False
    while (done == False):
        edge_list, new_tree_edges = BoruvkaStep(edge_list, starting_edges) #first Boruvka step
        tree_edges += new_tree_edges

        percentage = math.ceil((len(tree_edges)/(len(node_list) - 1))*100)
        print(f"The MST is {percentage}% done.")

        if(len(tree_edges) == (len(node_list))-1):
            done = True

    networkx_mst = nx.Graph()
    for edge in tree_edges:
        if (edge[2] != None):
            networkx_mst.add_edge(edge[0], edge[1], weight = edge[2])

    return networkx_mst

# debug = False

# problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

# G = problem.get_graph() #our starting graph

# tracemalloc.start()

# Run(G)