import tsplib95
import networkx as nx
import tracemalloc
import time
import math

def GetCycleForNode(vertex, visited, parent, the_cycle):
    visited.append(vertex)
    for neighbor in g.neighbors(vertex):
        if (neighbor not in visited):
            if (GetCycleForNode(neighbor, visited, vertex, the_cycle)):
                the_cycle.append(vertex)
                return the_cycle
        elif (neighbor != parent and parent != None and neighbor == visited[0]):
            the_cycle.append(vertex)
            return the_cycle
    return []

g = nx.Graph()
g.add_edge('A', 'B', weight = 1)
g.add_edge('A', 'D', weight = 2)
g.add_edge('A', 'E', weight = 3)
g.add_edge('B', 'C', weight = 5)
g.add_edge('B', 'E', weight = 5)#3
g.add_edge('B', 'F', weight = 1)
g.add_edge('C', 'D', weight = 4)#5
g.add_edge('C', 'F', weight = 2)
g.add_edge('D', 'E', weight = 4)

while (len(g.edges) > (len(g.nodes) - 1)):

    maximum_degree_node = list(g.nodes)[0]

    for node in g.nodes:
        if (g.degree(node) > g.degree(maximum_degree_node)):
            maximum_degree_node = node

    visited = []
    the_cycle = []
    the_cycle = GetCycleForNode(maximum_degree_node, visited, None, the_cycle)
    while (len(the_cycle) > 0):

        maximum_weight_edge = [the_cycle[-1], the_cycle[0]]

        for i in range(0, len(the_cycle)):
            weight = g.get_edge_data(the_cycle[i-1], the_cycle[i])["weight"]
            maximum_edge_weight = g.get_edge_data(maximum_weight_edge[0], maximum_weight_edge[1])["weight"]
            if (weight > maximum_edge_weight):
                maximum_weight_edge = [the_cycle[i-1], the_cycle[i]]

        quatity_of_most_expensive_edges = 0
        maximum_edge_weight = g.get_edge_data(maximum_weight_edge[0], maximum_weight_edge[1])["weight"]
        for i in range(0, len(the_cycle)):
            weight = g.get_edge_data(the_cycle[i-1], the_cycle[i])["weight"]
            if (maximum_edge_weight == weight):
                quatity_of_most_expensive_edges += 1

        if (quatity_of_most_expensive_edges > 1):
            maximum_weight_edges = []
            for i in range(0, len(the_cycle)):
                weight = g.get_edge_data(the_cycle[i-1], the_cycle[i])["weight"]
                if (maximum_edge_weight == weight):
                    maximum_weight_edges.append([the_cycle[i-1], the_cycle[i]])

            maximum_degree_sum_edge = maximum_weight_edges[0]
            for edge in maximum_weight_edges:
                degree_sum = g.degree(edge[0]) + g.degree(edge[1])
                maximum_degree_sum = g.degree(maximum_degree_sum_edge[0]) + g.degree(maximum_degree_sum_edge[1])
                if (degree_sum > maximum_degree_sum):
                    maximum_degree_sum_edge = edge

            maximum_weight_edge = maximum_degree_sum_edge

        g.remove_edge(maximum_weight_edge[0], maximum_weight_edge[1])
        print(g.edges)

        the_cycle = GetCycleForNode(maximum_degree_node, [], None, [])