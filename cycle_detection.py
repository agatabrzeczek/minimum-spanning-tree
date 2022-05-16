import networkx as nx

def DetectCycleForNode(vertex, visited, parent):
    visited.append(vertex)
    for neighbor in g.neighbors(vertex):
        if (neighbor not in visited):
            if (DetectCycleForNode(neighbor, visited, vertex)):
                return True
        elif (neighbor != parent and parent != None):
            return True
    return False

g = nx.Graph()
g.add_edge(1, 0)
g.add_edge(1, 2)
#g.add_edge(2, 0)
g.add_edge(0, 3)
g.add_edge(3, 4)

visited = []

print(g.nodes)

there_is_a_cycle = False

for node in g.nodes:
    if (DetectCycleForNode(node, visited, None)):
        there_is_a_cycle = True
        break

print(there_is_a_cycle)