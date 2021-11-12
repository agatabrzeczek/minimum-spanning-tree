import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
#G.add_path([3, 5, 4, 1, 0, 2, 7, 8, 9, 6])
#G.add_path([3, 0, 6, 4, 2, 7, 1, 9, 8, 5])

nx.add_path(G, [3, 5, 4, 1, 0, 2, 7, 8, 9, 6])
nx.add_path(G, [3, 0, 6, 4, 2, 7, 1, 9, 8, 5])
subax2 = plt.subplot(122)
nx.draw_shell(G, with_labels=True, font_weight='bold')

plt.show()