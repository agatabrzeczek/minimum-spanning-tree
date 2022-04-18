from os import listdir
from os.path import isfile, join
import random
import tsplib95
import networkx as nx
import kruskal_tsplib
import karger_tsplib
import boruvka_tsplib

def CheckMSTCorrectness(mst, G):
    actual_mst = nx.minimum_spanning_tree(G, algorithm="boruvka", weight="weight")

    sum_1 = 0
    for edge in nx.difference(actual_mst, mst).edges:
        #print(str(edge[0]) + "," + str(edge[1]) + "," + str(G.get_edge_data(edge[0], edge[1])["weight"]))
        sum_1 += G.get_edge_data(edge[0], edge[1])["weight"]

    sum_2 = 0
    for edge in nx.difference(mst, actual_mst).edges:
        #print(str(edge[0]) + "," + str(edge[1]) + "," + str(G.get_edge_data(edge[0], edge[1])["weight"]))
        sum_2 += G.get_edge_data(edge[0], edge[1])["weight"]

    if (sum_1 == sum_2):
        return True
    else:
        return False

def GetProblemSize(problem):
    return problem[1]

print("Minimum spanning tree algorithms")
kruskal = False
karger = False

print("available algorithms:")
print("1. Kruskal")
print("2. Karger")
print("3. Boruvka")
chosen_algorithms = input("Which algorithms would you like to run? ")

print("available problems:")

path = '../../data/tsplib95/archives/problems/tsp'
problem_list = [f for f in listdir(path) if isfile(join(path, f))]
problem_size = ''
for i in range(0, len(problem_list)):
    problem = problem_list[i]
    #print(problem)
    flag = False #makes sure the no is a substring of file name, done because of xray14012_1.tsp
    for character in problem:
        if (character.isdigit()):
            flag = True
            problem_size += character
        elif (flag == True):
            break
    problem_list[i] = [problem_list[i], int(problem_size)]
    problem_size = ''

problem_list.sort(key=GetProblemSize)

for i in range(0, len(problem_list)):
    print(f"{i+1}. {problem_list[i][0]}")

chosen_problem_nos = []
more_problems = 'Y'
while (more_problems == 'Y' or more_problems == 'y'):
    chosen_problem = input("Please select a problem (Enter 'R' for random problem) ")
    try:
        chosen_problem = int(chosen_problem)
        #if (chosen_problem not in range (1, (len(problem_list)+1))):
        if (chosen_problem not in range (1, 93)):
            print("This is not a valid choice. Please enter a number 1 - 112 or 'R'")
        else:
            chosen_problem_nos.append(chosen_problem)
            more_problems = input("Would you like to choose more problems? (Y, N) Default choice is no. ")
    except ValueError:
        if (chosen_problem != 'R' and chosen_problem != 'r'):
            print("This is not a valid choice. Please enter a number 1 - 112 or 'R'")
        else: 
            chosen_problem_nos.append(chosen_problem)
            more_problems = input("Would you like to choose more problems? (Y, N) Default choice is no. ")

for i in range(0, len(chosen_problem_nos)):
    if (chosen_problem_nos[i] == 'R' or chosen_problem_nos[i] == 'r'):
        choose_random_problem = True
        while (choose_random_problem):
            random_problem = random.randrange(1, (len(problem_list)+1))
            if (random_problem not in chosen_problem_nos):
                chosen_problem_nos[i] = random_problem
                choose_random_problem = False #this prevents us from the same problem appearing twice in chosen_problem_nos

chosen_problems = []
for i in range(0, len(problem_list)):
    if ((i+1) in chosen_problem_nos):
        chosen_problems.append(problem_list[i][0])

for problem in chosen_problems:
    print(f"Loading problem {problem}")
    problem = tsplib95.load(path + '/' + problem)

    G = problem.get_graph() #our starting graph
    T = nx.Graph() #our minimum spanning tree

    if ('1' in chosen_algorithms):
        print("Running Kruskal algorithm for this problem")
        kruskal_mst = kruskal_tsplib.Run(G)
        print("The result is:")
        print(kruskal_mst.edges)
        if (CheckMSTCorrectness(kruskal_mst, G)):
            print("This result is correct")
        else:
            print("This result is incorrect")

    if ('2' in chosen_algorithms):
        print("Running Karger algorithm for this problem")
        karger_mst = karger_tsplib.Run(G)
        print("The result is:")
        print(karger_mst.edges)
        if (CheckMSTCorrectness(karger_mst, G)):
            print("This result is correct")
        else:
            print("This result is incorrect")

    if ('3' in chosen_algorithms):
        print("Running Boruvka algorithm for this problem")
        boruvka_mst = boruvka_tsplib.Run(G)
        print("The result is:")
        print(boruvka_mst.edges)
        if (CheckMSTCorrectness(boruvka_mst, G)):
            print("This result is correct")
        else:
            print("This result is incorrect")

# print(chosen_algorithms)
# print(chosen_problems)

# problem_sizes = []
# problem_size = ''
# for file in problems:
#     print(file)
#     flag = False #makes sure the no is a substring of file name, done because of xray14012_1.tsp
#     for character in file:
#         if (character.isdigit()):
#             flag = True
#             problem_size += character
#         elif (flag == True):
#             break
#     problem_sizes.append(problem_size)
#     print(problem_size)
#     problem_size =''

# print(problems)

# if ("1" in choice):
#     kruskal = True
# if ("2" in choice):
#     karger = True

# algorithms = [kruskal, karger]