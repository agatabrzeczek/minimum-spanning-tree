from cmath import inf
import random
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import math
import time

def BoruvkaStep(edge_list, starting_edges):
    #starting edges are edges at the start of whole program, original edges are edges at the start of boruvka step
    
    networkx_graph = GetNetworkxGraph(edge_list)

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
        if (edge_to_be_contracted not in edges_to_be_contracted):
            edges_to_be_contracted.append(edge_to_be_contracted)

    for edge_to_be_contracted in edges_to_be_contracted:
        edge_to_be_contracted = [edge_to_be_contracted[0], edge_to_be_contracted[1], networkx_graph.get_edge_data(edge_to_be_contracted[0], edge_to_be_contracted[1])["weight"]] #integration stub
        networkx_graph.remove_edge(edge_to_be_contracted[0], edge_to_be_contracted[1])

    original_edges = [x[:] for x in edge_list] #integration stub

    for i in range(0, len(edge_list)): #integration stub
        edge = edge_list[i]
        if not(networkx_graph.has_edge(edge[0], edge[1])):
            edge_list[i][2] = None

    node_list = list(networkx_graph.nodes) #integration stub

    for edge_to_be_contracted in edges_to_be_contracted:

        #TODO change this to new version
        for i in range(0, len(original_edges)): #mapping nodes of edges to be contracted
            edge_nodes = [original_edges[i][0], original_edges[i][1]]
            edge_weight = original_edges[i][2]
            if (edge_to_be_contracted[0] in edge_nodes and edge_weight != None):
                if (edge_to_be_contracted[1] in edge_nodes):
                    edge_to_be_contracted = edge_list[i].copy()

        for edge in edge_list: #integration stub
            edge_nodes = [edge[0], edge[1]]
            if (edge_to_be_contracted[0] in edge_nodes and edge_to_be_contracted[1] in edge_nodes):
                edge[2] = None 

        #networkx_graph = GetNetworkxGraph(edge_list) #integration stub

        edges_to_be_updated = []
        for edge in networkx_graph.edges: #gathering all the edges which have to be updated
            edge_nodes = [edge[0], edge[1]]
            if (edge_to_be_contracted[0] in edge_nodes or edge_to_be_contracted[1] in edge_nodes):
                edges_to_be_updated.append(edge)

        #integration stub
        for i in range(0, len(edges_to_be_updated)):
            edge = edges_to_be_updated[i]
            edges_to_be_updated[i] = [edge[0], edge[1], networkx_graph.get_edge_data(edge[0], edge[1])["weight"]]

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
                for edge in networkx_graph.edges:
                    edge_nodes = [edge[0], edge[1]]
                    if (node in edge_nodes):
                        if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                            edge_weight = networkx_graph.get_edge_data(edge[0], edge[1])["weight"]
                            edge_id = networkx_graph.get_edge_data(edge[0], edge[1])["id"]
                            networkx_graph.remove_edge(edge_nodes)
                            networkx_graph.add_edge(edge[0], edge[1], weight = edge_weight, id = edge_id)
            else:
                if (len(compared_edges) == 2 and compared_edges[0][2] == compared_edges[1][2]): #if both edges have the same weight, just throw away the one with the greater node
                    for i in range(0, len(edge_list)):
                        edge_nodes = [edge_list[i][0], edge_list[i][1]]
                        if (node in edge_nodes):
                            if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                                edge_list[i][0] = min([edge_to_be_contracted[0], edge_to_be_contracted[1]])
                                edge_list[i][1] = node
                                edge_list[i][2] = None
                                #networkx_graph = GetNetworkxGraph(edge_list)
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
                                    #networkx_graph = GetNetworkxGraph(edge_list)
                            elif (min([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
                                if (edge_list[i][2] != new_weight):
                                    edge_list[i][2] = None
                                    #networkx_graph = GetNetworkxGraph(edge_list)

        #networkx_graph = GetNetworkxGraph(edge_list)

    tree_edges = []
    for edge in edges_to_be_contracted:
        for i in range(0, len(edge_list)):
            #if (original_edges[i] == [edge[0], edge[1], networkx_graph.get_edge_data(edge[0], edge[1])["weight"]] or original_edges[i] == [edge[1], edge[0], networkx_graph.get_edge_data(edge[0], edge[1])["weight"]]):
            if (original_edges[i][2] != None and ([original_edges[i][0], original_edges[i][1]] == [edge[0], edge[1]] or [original_edges[i][0], original_edges[i][1]] == [edge[1], edge[0]])):
                tree_edges.append(starting_edges[i])

    return edge_list, tree_edges

def DeleteFHeavyEdges(graph, forest):

    networkx_forest = GetNetworkxGraph(forest)
    networkx_graph = GetNetworkxGraph(graph)

    #for i in range(0, len(graph.edges)):
    for edge in networkx_graph.edges:

        #edge = graph[i]
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

    for i in range(0, len(graph)):
        edge = graph[i]
        if not(networkx_graph.has_edge(edge[0], edge[1])):
            graph[i][2] = None

    return graph

def GetNetworkxGraph(edge_list):

    networkx_graph = nx.Graph()

    #for edge in edge_list:
    for i in range(0, len(edge_list)):
        edge = edge_list[i]
        if (edge[2] != None):
            networkx_graph.add_edge(edge[0], edge[1], weight = edge[2], id = i)
    
    return networkx_graph

def SelectRandomEdges(edge_list):
    selected_edges = []

    for edge in edge_list:
        decision = random.randrange(0, 2)
        if (decision == 1):
        #if (edge in [[12, 4, 8], [3, 4, 32], [1, 4, 10]]):
            selected_edges.append(edge)
        else:
            selected_edges.append([edge[0], edge[1], None])

    return selected_edges

def Run(G):

    for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
        if (G.has_edge(i, i)):
            G.remove_edge(i, i)


    edge_list = [] #converting networkx graph to list of edges
    for edge in G.edges:
        edge_list.append([edge[0], edge[1], G.get_edge_data(edge[0], edge[1])["weight"]])
    starting_edges = [x[:] for x in edge_list]
    f_heavy_edge_indices = []

    node_list = [] #deriving node list from edge list
    for edge in edge_list:
        if (edge[0] not in node_list and edge[2] != None):
            node_list.append(edge[0])
        if (edge[1] not in node_list and edge[2] != None):
            node_list.append(edge[1])

    start_time = time.time()
    tracemalloc.start()

    all_done = False #if True the MST has been computed
    tree_edges = [] #we will be adding to this tree w each iteration
    while (all_done == False):
        done = False #if true the MSF of subgraph has been computed
        forest_edges = []
        boruvka_edges = []
        graph_before_random_selection = []
        while (done == False):
            edge_list, new_tree_edges = BoruvkaStep(edge_list, starting_edges) #first Boruvka step
            forest_edges += new_tree_edges

            edge_list, new_tree_edges = BoruvkaStep(edge_list, starting_edges) #second Boruvka step
            forest_edges += new_tree_edges

            if (len(boruvka_edges) == 0): #only done for the first iteration of loop
                boruvka_edges = forest_edges.copy()

            if (len(graph_before_random_selection) == 0): #only done for the first iteration of loop
                graph_before_random_selection = [x[:] for x in edge_list]

            done = True #first we assume that the forest is completed...
            for edge in edge_list:
                if (edge[2] != None):
                    done = False #...and if not, we reset the flag to False
                    edge_list = SelectRandomEdges(edge_list)
                    break

        tree_edges += boruvka_edges

        percentage = math.floor((len(tree_edges)/(len(node_list) - 1))*100)
        print(f"The MST is {percentage}% done.")

        if(len(tree_edges) == (len(node_list))-1):
            all_done = True
        
        edge_list = DeleteFHeavyEdges(graph_before_random_selection, forest_edges)

    networkx_mst = nx.Graph()
    for edge in tree_edges:
        if (edge[2] != None):
            networkx_mst.add_edge(edge[0], edge[1], weight = edge[2])

    end_time = time.time()
    memory_consumption = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return networkx_mst, round(end_time - start_time, 3), memory_consumption

# debug = False

# problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

# G = problem.get_graph() #our starting graph

# tracemalloc.start()

# Run(G)