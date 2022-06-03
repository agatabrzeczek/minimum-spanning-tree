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

def DeleteFHeavyEdges(networkx_graph, forest):

    networkx_forest = nx.Graph()

    for edge_id in forest:
        for edge in networkx_graph.edges:
            G_edge_id = networkx_graph.get_edge_data(edge[0], edge[1])["id"]
            if (edge_id == G_edge_id):
                edge_weight = networkx_graph.get_edge_data(edge[0], edge[1])["weight"]
                networkx_forest.add_edge(edge[0], edge[1], weight = edge_weight, id = edge_id)

    for edge in networkx_graph.edges:

        maximum_weight = 0
        weight_graph = networkx_graph.get_edge_data(edge[0], edge[1])["weight"]
        if (networkx_forest.has_node(edge[0]) and networkx_forest.has_node(edge[1])):
            if (nx.has_path(networkx_forest, edge[0], edge[1])):
                path = nx.shortest_path(networkx_forest, source=edge[0], target=edge[1])
                for i in range(0, (len(path)-1)):
                    weight_forest = networkx_forest.get_edge_data(path[i], path[i+1])["weight"]
                    if (weight_forest > maximum_weight):
                        maximum_weight = weight_forest
            else:
                maximum_weight = inf
        else:
            maximum_weight = inf
        if (weight_graph > maximum_weight):
            networkx_graph.remove_edge(edge[0], edge[1])

    return networkx_graph

def GetNetworkxGraph(edge_list):

    networkx_graph = nx.Graph()

    for i in range(0, len(edge_list)):
        edge = edge_list[i]
        if (edge[2] != None):
            networkx_graph.add_edge(edge[0], edge[1], weight = edge[2], id = i)
    
    return networkx_graph

def SelectRandomEdges(graph):
    #subgraph = graph.copy()

    for edge in graph.edges:
        decision = random.randrange(0, 2)
        if (decision == 1):
            graph.remove_edge(edge[0], edge[1])

    return graph

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

    all_done = False #if True the MST has been computed
    tree_edges = [] #we will be adding to this tree w each iteration
    while (all_done == False):
        done = False #if true the MSF of subgraph has been computed
        forest_edges = []
        boruvka_edges = []
        graph_before_random_selection = []
        while (done == False):
            G, new_tree_edges = BoruvkaStep(G) #first Boruvka step
            forest_edges += new_tree_edges

            G, new_tree_edges = BoruvkaStep(G) #second Boruvka step
            forest_edges += new_tree_edges

            if (len(boruvka_edges) == 0): #only done for the first iteration of loop
                boruvka_edges = forest_edges.copy()

            if (len(graph_before_random_selection) == 0): #only done for the first iteration of loop
                graph_before_random_selection = G.copy()

            G = SelectRandomEdges(G)

            if (len(G.edges) == 0):
                done = True

        tree_edges += boruvka_edges

        percentage = math.floor((len(tree_edges)/(len(original_G.nodes) - 1))*100)
        print(f"The MST is {percentage}% done.")

        if(len(tree_edges) == (len(original_G.nodes))-1):
            all_done = True

        G = DeleteFHeavyEdges(graph_before_random_selection, forest_edges)

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
if __name__ == "__main__":
    problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/lin318.tsp')

    G = problem.get_graph()

    for i in range(1, len(G.nodes)+1):
        G.remove_edge(i, i)

    counter = 0

    edge_list = list(G.edges)
    for i in range(0, len(edge_list)):
        edge = edge_list[i]
        if (i % 2 == 0):
            G.remove_edge(edge[0], edge[1])

    mst, ktime, b = Run(G)

    print(ktime)
    print(counter)