import networkx as nx
import tsplib95

problem = tsplib95.load('../../data/tsplib95/archives/problems/tsp/rat99.tsp')

G = problem.get_graph() #our starting graph

MST = nx.minimum_spanning_tree(G, algorithm="boruvka", weight="weight")

print(MST.edges)