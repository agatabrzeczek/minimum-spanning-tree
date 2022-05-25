import sys
import networkx as nx
import tracemalloc
import time
import math

def GetCycleForNode(g, vertex, visited, parent, the_cycle):
    visited.append(vertex)
    for neighbor in g.neighbors(vertex):
        if (neighbor not in visited):
            if (GetCycleForNode(g, neighbor, visited, vertex, the_cycle)):
                the_cycle.append(vertex)
                return the_cycle
        elif (neighbor != parent and parent != None and neighbor == visited[0]):
            the_cycle.append(vertex)
            return the_cycle
    return []

def Run(g):
    sys.setrecursionlimit(2000)

    for i in range(0, len(g.nodes)+1): #removing edges that connect a node to itself
        if (g.has_edge(i, i)):
            g.remove_edge(i, i)

    start_time = time.time()
    tracemalloc.start()

    percentage = 0
    no_of_edges_in_g = len(g.edges)
    no_of_edges_in_t = len(g.nodes) - 1
    no_of_edges_to_be_removed = no_of_edges_in_g - no_of_edges_in_t
    no_of_removed_edges = 0

    nodes_to_be_checked = list(g.nodes)
    while (len(g.edges) > (len(g.nodes) - 1)):

        maximum_degree_node = nodes_to_be_checked[0]

        for node in nodes_to_be_checked:
            if (g.degree(node) > g.degree(maximum_degree_node)):
                maximum_degree_node = node

        visited = []
        the_cycle = []
        the_cycle = GetCycleForNode(g, maximum_degree_node, visited, None, the_cycle)
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
            no_of_removed_edges += 1

            old_percentage = percentage
            percentage = math.floor((no_of_removed_edges/no_of_edges_to_be_removed)*100)
            if (old_percentage != percentage):
                print(f"The MST is {percentage}% done.")

            #print(f"removed edge {maximum_weight_edge}")

            the_cycle = GetCycleForNode(g, maximum_degree_node, [], None, [])
        nodes_to_be_checked.remove(maximum_degree_node)

    end_time = time.time()
    memory_consumption = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return g, round(end_time - start_time, 3), memory_consumption

