import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import time
import math

def DetectCycleForNode(graph, vertex, visited, parent):
    visited.append(vertex)

    for neighbor in GetNeighbors(graph, vertex):
        if (neighbor not in visited):
            if (DetectCycleForNode(graph, neighbor, visited, vertex)):
                return True
        elif (neighbor != parent and parent != None):
            return True

    return False

def ExamineEdge(edge, T):

    T.add_edge(edge[0], edge[1], weight = edge[2]) #temporarily adding the edge to the MST

    if (IsThereACycle(T) == False):
        return True, T
    else:
        T.remove_edge(edge[0], edge[1])
        return False, T

def GetNeighbors(graph, vertex):
    neighbors = []

    for edge in graph.edges:
        if (vertex in edge):
            if (edge[0] == vertex):
                neighbors.append(edge[1])
            else:
                neighbors.append(edge[0])

    return neighbors

def GetWeight(edge):
    return edge[2]

def IsThereACycle(graph):
    visited = []

    there_is_a_cycle = False

    for node in graph.nodes:
        if (DetectCycleForNode(graph, node, visited, None)):
            there_is_a_cycle = True
            return True

    return False

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