import tsplib95
import matplotlib.pyplot as plt
import networkx as nx

problem = tsplib95.load('data/test_data/test5.tsp')

G = problem.get_graph()

for i in range(1, len(G.nodes)+1):
    G.remove_edge(i, i)

print(nx.get_edge_attributes(G, 'weight'))

subax2 = plt.subplot(111)
my_pos = nx.circular_layout(G)
nx.draw_networkx_nodes(G, pos=my_pos)
nx.draw_networkx_labels(G, pos=my_pos)
nx.draw_networkx_edges(G, pos=my_pos)
nx.draw_networkx_edge_labels(G, my_pos, nx.get_edge_attributes(G, 'weight'))

plt.show()