from cmath import inf
import random
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import math
import time

def BoruvkaStep(networkx_graph):
    #starting edges are edges at the start of whole program

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

    # for edge_to_be_contracted in edges_to_be_contracted:
    #     #edge_to_be_contracted = [edge_to_be_contracted[0], edge_to_be_contracted[1], networkx_graph.get_edge_data(edge_to_be_contracted[0], edge_to_be_contracted[1])["weight"]] #integration stub
    #     networkx_graph.remove_edge(edge_to_be_contracted[0], edge_to_be_contracted[1])

    for edge_to_be_contracted in edges_to_be_contracted:

        for edge in edges_to_be_contracted:
            if (edge == edge_to_be_contracted):
                break
            if (edge_to_be_contracted[0] in edge and max(edge) == edge_to_be_contracted[0]):
                edge_to_be_contracted[0] = min(edge)
            if (edge_to_be_contracted[1] in edge and max(edge) == edge_to_be_contracted[1]):
                edge_to_be_contracted[1] = min(edge)

        nodes_to_be_updated = []
        for edge in networkx_graph.edges: #gathering all the edges which have to be updated
            #edge_nodes = [edge[0], edge[1]]
            if (edge_to_be_contracted[0] == edge[0] or edge_to_be_contracted[1] == edge[0]):
                nodes_to_be_updated.append(edge[1])
            elif (edge_to_be_contracted[0] == edge[1] or edge_to_be_contracted[1] == edge[1]):
                nodes_to_be_updated.append(edge[0])

        for node in nodes_to_be_updated:
            compared_edges = []
            if (node in [edge_to_be_contracted[0], edge_to_be_contracted[1]]):
                continue
            # else:
            #     for edge in edges_to_be_updated:
            #         edge_nodes = [edge[0], edge[1]]
            #         if (node in edge_nodes):
            #             compared_edges.append(edge)
            # if (len(compared_edges) == 0): #DID
            #     pass
            #     for edge in networkx_graph.edges:
            #         edge_nodes = [edge[0], edge[1]]
            #         if (node in edge_nodes):
            #             if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
            #                 edge_weight = networkx_graph.get_edge_data(edge[0], edge[1])["weight"]
            #                 edge_id = networkx_graph.get_edge_data(edge[0], edge[1])["id"]
            #                 networkx_graph.remove_edge(edge_nodes)
            #                 networkx_graph.add_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node, weight = edge_weight, id = edge_id)
            # else:
            # if (len(compared_edges) == 2 and networkx_graph.get_edge_data(compared_edges[0][0], compared_edges[0][1])["weight"] == networkx_graph.get_edge_data(compared_edges[1][0], compared_edges[1][1])["weight"]):    
            #     for edge in networkx_graph.edges:
            #         edge_nodes = [edge[0], edge[1]]
            #         if (node in edge_nodes):
            #             if (max([edge_to_be_contracted[0], edge_to_be_contracted[1]]) in edge_nodes):
            #                 networkx_graph.remove_edge(edge_nodes[0], edge_nodes[1])
            if (True):
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
                # if (networkx_graph.has_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)):
                #     if (weight_of_2nd_edge < weight_of_1st_edge):
                #         networkx_graph.remove_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)
                #     #networkx_graph.add_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node, weight = weight_of_2nd_edge, id = id_of_2nd_edge)

                # if (networkx_graph.has_edge(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)):
                #     networkx_graph.remove_edge(max([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node)
                #     networkx_graph.add_edge(min([edge_to_be_contracted[0], edge_to_be_contracted[1]]), node, weight = weight_of_2nd_edge, id = id_of_2nd_edge)

        if (networkx_graph.has_edge(edge_to_be_contracted[0], edge_to_be_contracted[1])):
            networkx_graph.remove_edge(edge_to_be_contracted[0], edge_to_be_contracted[1])

    # for i in range(0, len(edge_list)):
    #     edge_list[i][2] = None

    # for edge in networkx_graph.edges:
    #     edge_id = networkx_graph.get_edge_data(edge[0], edge[1])["id"]
    #     edge_list[edge_id] = [edge[0], edge[1], networkx_graph.get_edge_data(edge[0], edge[1])["weight"]]

    return networkx_graph, tree_edges

def DeleteFHeavyEdges(networkx_graph, forest):

    networkx_forest = nx.Graph()

    for edge_id in forest:
        for edge in networkx_graph.edges:
            G_edge_id = networkx_graph.get_edge_data(edge[0], edge[1])["id"]
            if (edge_id == G_edge_id):
                edge_weight = networkx_graph.get_edge_data(edge[0], edge[1])["weight"]
                networkx_forest.add_edge(edge[0], edge[1], weight = edge_weight, id = edge_id)

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

    return networkx_graph

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
        #if (edge in [[13, 1, 350], [2, 3, 654], [12, 4, 1025], [9, 4, 490], [12, 9, 324], [9, 11, 2722], [13, 11, 841], [1, 11, 418], [12, 11, 3105], [2, 11, 2839], [3, 11, 2071], [4, 11, 1279], [14, 11, 1438], [12, 14, 1068], [4, 13, 317], [14, 4, 315], [3, 9, 314], [1, 7, 418], [1, 9, 1939], [9, 7, 2035], [13, 9, 1707], [14, 9, 868], [1, 12, 2280], [1, 2, 2255], [1, 3, 1369], [1, 4, 529], [1, 14, 605], [12, 7, 2292], [3, 12, 561], [13, 12, 2163], [2, 4, 368], [2, 9, 395], [11, 7, 924], [2, 7, 2515], [3, 7, 1582], [4, 7, 804], [14, 7, 481], [13, 7, 1108], [2, 13, 1715], [14, 2, 1407], [4, 3, 261], [13, 3, 999], [14, 13, 971], [14, 3, 439], [2, 12, 928]]):
            selected_edges.append(edge)
        else:
            selected_edges.append([edge[0], edge[1], None])

    return selected_edges

def Run(G):

    for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
        if (G.has_edge(i, i)):
            G.remove_edge(i, i)

    # edge_list = [] #converting networkx graph to list of edges
    # for edge in G.edges:
    #     edge_list.append([edge[0], edge[1], G.get_edge_data(edge[0], edge[1])["weight"]])
    # starting_edges = [x[:] for x in edge_list]
    # f_heavy_edge_indices = []

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

    # node_list = [] #deriving node list from edge list
    # for edge in edge_list:
    #     if (edge[0] not in node_list and edge[2] != None):
    #         node_list.append(edge[0])
    #     if (edge[1] not in node_list and edge[2] != None):
    #         node_list.append(edge[1])

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

            # done = True #first we assume that the forest is completed...
            # for edge in edge_list:
            #     if (edge[2] != None):
            #         done = False #...and if not, we reset the flag to False
            #         edge_list = SelectRandomEdges(edge_list)
            #         break

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

# debug = False

# problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

# G = problem.get_graph() #our starting graph

# tracemalloc.start()

# Run(G)