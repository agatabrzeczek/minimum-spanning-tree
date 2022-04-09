import networkx as nx
import tsplib95

tree_1 = nx.Graph()
edges_of_tree_1 = [(10, 20), (10, 4), (10, 13), (20, 2), (14, 18), (14, 22), (18, 15), (1, 28), (1, 24), (28, 6), (4, 15), (15, 19), (22, 17), (22, 11), (26, 29), (26, 5), (29, 3), (24, 27), (27, 8), (27, 16), (27, 23), (2, 21), (21, 5), (5, 9), (5, 6), (6, 12), (19, 25), (25, 7)]
tree_2 = nx.Graph()
edges_of_tree_2 = [(1, 28), (1, 24), (2, 21), (2, 20), (21, 5), (3, 29), (29, 26), (4, 15), (4, 10), (15, 19), (15, 18), (5, 9), (5, 6), (6, 12), (7, 25), (25, 19), (8, 27), (27, 16), (27, 23), (27, 24), (10, 20), (10, 13), (11, 22), (22, 17), (22, 14), (14, 18)]

for edge in edges_of_tree_1:
    tree_1.add_edge(edge[0], edge[1])

for edge in edges_of_tree_2:
    tree_2.add_edge(edge[0], edge[1])

print(nx.difference(tree_1, tree_2).edges)
print(nx.difference(tree_2, tree_1).edges)

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/bayg29.tsp')
G = problem.get_graph() #our starting graph

# for edge in G.edges:
#     print(str(edge[0]) + ", " + str(edge[1]) + ", " + str(G.get_edge_data(edge[0], edge[1])["weight"]))

for i in range(0, len(G.nodes)+1): #removing edges that connect a node to itself
    if (G.has_edge(i, i)):
        G.remove_edge(i, i)

sum = 0
for edge in nx.difference(tree_1, tree_2).edges:
    print(str(edge[0]) + "," + str(edge[1]) + "," + str(G.get_edge_data(edge[0], edge[1])["weight"]))
    sum += G.get_edge_data(edge[0], edge[1])["weight"]
print("sum for tree 1: " + str(sum))

sum = 0
for edge in nx.difference(tree_2, tree_1).edges:
    print(str(edge[0]) + "," + str(edge[1]) + "," + str(G.get_edge_data(edge[0], edge[1])["weight"]))
    sum += G.get_edge_data(edge[0], edge[1])["weight"]
print("sum for tree 2: " + str(sum))