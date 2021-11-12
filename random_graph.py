import matplotlib.pyplot as plt
import networkx as nx
from random import randrange

n=randrange(21)
m=randrange(61)
G1 = nx.gnm_random_graph(n, m, seed=None, directed=False)
G2 = nx.gnm_random_graph(n, m, seed=None, directed=False)
G3 = nx.gnm_random_graph(n, m, seed=None, directed=False)
G4 = nx.gnm_random_graph(n, m, seed=None, directed=False)

subax2 = plt.subplot(221)
nx.draw_shell(G1, with_labels=True, font_weight='bold')

subax2 = plt.subplot(222)
nx.draw_shell(G2, with_labels=True, font_weight='bold')

subax2 = plt.subplot(223)
nx.draw_shell(G3, with_labels=True, font_weight='bold')

subax2 = plt.subplot(224)
nx.draw_shell(G4, with_labels=True, font_weight='bold')

plt.show()