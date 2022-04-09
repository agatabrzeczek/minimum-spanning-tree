from cmath import inf
import random
import tsplib95
import matplotlib.pyplot as plt
import networkx as nx
import tracemalloc
import sys

def BoruvkaStep(G):
    edges = []
    for edge in G.edges:
        edges.append([edge[0], edge[1], G.get_edge_data(edge[0], edge[1])["weight"]])

    edges_to_be_contracted = []
    for node in G.nodes:
        weight = inf
        edge_to_be_contracted = []
        for edge in edges:
            if (node in [edge[0], edge[1]]):
                if (edge[2] < weight):
                    edge_to_be_contracted = edge
                    weight = edge[2]
        if (edge_to_be_contracted not in edges_to_be_contracted):
            edges_to_be_contracted.append(edge_to_be_contracted)

    for edge_to_be_contracted in edges_to_be_contracted:
        for i in range(0, len(edges)):
            if (edges[i] == edge_to_be_contracted):
                edges[i] = None

    for edge_to_be_contracted in edges_to_be_contracted:
        edges_to_be_updated = []
        for edge in edges:
            if (edge != None):
                edge_nodes = [edge[0], edge[1]]
                if (edge_to_be_contracted[0] in edge_nodes):
                    edges_to_be_updated.append(edge)
                elif (edge_to_be_contracted[1] in edge_nodes):
                    edges_to_be_updated.append(edge)

        for item in edges_to_be_updated:
            print(item)
        print('------')

    if (debug == True):
        DrawGraph(G)

    return G, None

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

def Run(G):
    G, T = BoruvkaStep(G)

debug = False

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/burma14.tsp')

G = problem.get_graph() #our starting graph
original_G = G.copy()

for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
    if (G.has_edge(i, i)):
        G.remove_edge(i, i)

tracemalloc.start()

#DRAWING:
if (debug == True):
    DrawGraph(G)

Run(G)

#DRAWING:
if (debug == True):
    DrawGraph(G)