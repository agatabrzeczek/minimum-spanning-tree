# A comparative analysis of Minimum Spanning Tree algorithms

This repository contains source code that I wrote while working on my master's thesis. The objective of this thesis was to compare multiple Minimum Spanning Tree algorithms (which are graph algorithms).

The main library that I used here is NetworkX, and the graphs that I used were derived from TSPLIB and are available on this site:

http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/

In this project I compared 5 algorithms:
1. Kruskal's algorithm - out-of-the-box NetworkX implementation
2. Kruskal's algorithm - my own implementation
3. Boruvka's algorithm - my own implementation
4. Karger's algorithm - my own implementation
5. Biswas' algorithm - my own implementation

I compared the above algorithms by calculating time required to provide the Minimum Spanning Tree and memory resources used by the algorithms.
