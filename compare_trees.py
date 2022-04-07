import networkx as nx
import tsplib95

tree_1 = nx.Graph()
edges_of_tree_1 = [(72, 73), (72, 71), (75, 76), (75, 1), (13, 14), (13, 12), (13, 15), (14, 74), (36, 37), (36, 35), (36, 38), (37, 18), (59, 60), (59, 58), (59, 61), (60, 41), (18, 17), (19, 31), (19, 20), (31, 30), (21, 25), (21, 22), (25, 24), (41, 40), (42, 54), (42, 43), (54, 53), (44, 48), (44, 45), (48, 47), (7, 8), (7, 6), (30, 
29), (53, 52), (17, 11), (40, 34), (63, 64), (63, 57), (64, 71), (3, 4), (3, 6), (3, 2), (9, 10), (9, 12), 
(10, 5), (15, 16), (26, 27), (26, 29), (32, 33), (33, 28), (38, 39), (49, 50), (49, 52), (55, 56), (56, 51), (61, 62), (20, 5), (43, 28), (65, 66), (66, 51), (6, 5), (29, 28), (52, 51), (1, 2), (1, 23), (11, 12), (24, 46), (34, 35), (47, 69), (57, 58), (22, 23), (45, 46), (67, 68), (67, 70), (68, 69)]
tree_2 = nx.Graph()
edges_of_tree_2 = [(1, 2), (1, 23), (1, 75), (3, 4), (3, 6), (5, 20), (5, 6), (5, 10), (20, 19), (6, 7), (7, 8), (9, 10), (9, 12), (11, 12), (11, 17), (12, 13), (13, 14), (13, 15), (14, 74), (15, 16), (17, 18), (18, 37), (37, 36), (19, 31), (31, 30), (21, 25), (21, 22), (25, 24), (22, 23), (24, 46), (26, 27), (26, 29), (28, 43), (28, 29), (28, 33), (43, 42), (29, 30), (32, 33), (34, 35), (34, 40), (35, 36), (36, 38), (38, 39), (40, 41), (41, 
60), (60, 59), (42, 54), (54, 53), (44, 48), (44, 45), (48, 47), (48, 49), (45, 46), (47, 69), (49, 50), (49, 52), (51, 66), (51, 52), (51, 56), (66, 65), (52, 53), (55, 56), (57, 58), (57, 63), (58, 59), (59, 61), (61, 62), (63, 64), (64, 72), (67, 68), (67, 70), (68, 69), (71, 72), (72, 73), (75, 76)]

for edge in edges_of_tree_1:
    tree_1.add_edge(edge[0], edge[1])

for edge in edges_of_tree_2:
    tree_2.add_edge(edge[0], edge[1])

print(nx.difference(tree_1, tree_2).edges)
print(nx.difference(tree_2, tree_1).edges)

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/pr76.tsp')
G = problem.get_graph() #our starting graph

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