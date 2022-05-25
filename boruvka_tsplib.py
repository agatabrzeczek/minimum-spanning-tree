from cmath import inf
import random
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import math
import time

def BoruvkaStep(networkx_graph):

    edges_to_be_contracted = []
    for node in networkx_graph.nodes:
        minimum_weight = inf
        edge_to_be_contracted = []
        for edge in networkx_graph.edges:
            if (networkx_graph.has_edge(edge[0], edge[1])):
                if (node in [edge[0], edge[1]]):
                    weight = networkx_graph.get_edge_data(edge[0], edge[1])["weight"]
                    if (weight < minimum_weight):
                        edge_to_be_contracted = [edge[0], edge[1]]
                        minimum_weight = weight
        if (edge_to_be_contracted not in edges_to_be_contracted and edge_to_be_contracted != []):
            edges_to_be_contracted.append(edge_to_be_contracted)

    tree_edges = []
    for edge in edges_to_be_contracted:
        edge_id = networkx_graph.get_edge_data(edge[0], edge[1])["id"]
        tree_edges.append(edge_id)

    for edge_to_be_contracted in edges_to_be_contracted:

        for edge in edges_to_be_contracted:
            if (edge == edge_to_be_contracted):
                break
            if (edge_to_be_contracted[0] in edge and max(edge) == edge_to_be_contracted[0]):
                edge_to_be_contracted[0] = min(edge)
            if (edge_to_be_contracted[1] in edge and max(edge) == edge_to_be_contracted[1]):
                edge_to_be_contracted[1] = min(edge)

        nodes_to_be_updated = []
        for edge in networkx_graph.edges: #gathering all the nodes which have to be updated
            if (edge_to_be_contracted[0] == edge[0] or edge_to_be_contracted[1] == edge[0]):
                nodes_to_be_updated.append(edge[1])
            elif (edge_to_be_contracted[0] == edge[1] or edge_to_be_contracted[1] == edge[1]):
                nodes_to_be_updated.append(edge[0])

        for node in nodes_to_be_updated:
            if (node in [edge_to_be_contracted[0], edge_to_be_contracted[1]]):
                continue
            if (networkx_graph.has_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)):
                new_weight = networkx_graph.get_edge_data(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)["weight"]
                new_id = networkx_graph.get_edge_data(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)["id"]
            else:
                new_weight = inf
            if (networkx_graph.has_edge(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)):
                weight_of_2nd_edge = networkx_graph.get_edge_data(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)["weight"]
                if (weight_of_2nd_edge < new_weight):
                    new_weight = weight_of_2nd_edge
                    new_id = networkx_graph.get_edge_data(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)["id"]
            if (networkx_graph.has_edge(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)):
                networkx_graph.remove_edge(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)
            if (networkx_graph.has_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)):
                networkx_graph.remove_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)
            networkx_graph.add_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node, weight = new_weight, id = new_id)

        if (networkx_graph.has_edge(edge_to_be_contracted[0], edge_to_be_contracted[1])):
            networkx_graph.remove_edge(edge_to_be_contracted[0], edge_to_be_contracted[1])

    return networkx_graph, tree_edges

def Run(G):

    for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
        if (G.has_edge(i, i)):
            G.remove_edge(i, i)

    start_time = time.time()
    tracemalloc.start()

    edges = list(G.edges)
    for i in range(0, len(edges)):
        edge = edges[i]
        edge_weight = G.get_edge_data(edge[0], edge[1])["weight"]
        edge_id = i
        G.remove_edge(edge[0], edge[1])
        G.add_edge(edge[0], edge[1], weight = edge_weight, id = edge_id)

    original_G = G.copy()

    tree_edges = [] #we will be adding to this tree w each iteration
    done = False
    while (done == False):
        G, new_tree_edges = BoruvkaStep(G)
        tree_edges += new_tree_edges

        percentage = math.floor((len(tree_edges)/(len(original_G.nodes) - 1))*100)
        print(f"The MST is {percentage}% done.")

        if(len(tree_edges) == (len(original_G.nodes))-1):
            done = True

    networkx_mst = nx.Graph()
    for edge_id in tree_edges:
        for original_edge in original_G.edges:
            original_edge_id = original_G.get_edge_data(original_edge[0], original_edge[1])["id"]
            if (edge_id == original_edge_id):
                tree_edge_weight = original_G.get_edge_data(original_edge[0], original_edge[1])["weight"]
                networkx_mst.add_edge(original_edge[0], original_edge[1], weight = tree_edge_weight, id = edge_id)

    end_time = time.time()
    memory_consumption = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return networkx_mst, round(end_time - start_time, 3), memory_consumption

# debug = False

# problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

# G = problem.get_graph() #our starting graph

# tracemalloc.start()

# Run(G)