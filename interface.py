from os import listdir
from os.path import isfile, join
import random
import tsplib95
import networkx as nx
import kruskal_tsplib
import kruskal_tsplib_networkx
import karger_tsplib#_kopia as karger_tsplib
#import karger_tsplib_dictionary as karger_tsplib
import boruvka_tsplib
import biswas_tsplib
import csv

def CalculateAverage(list):
    if (list[0] == 'not chosen'):
        return 'not applicable'
    else:
        return round(sum(list)/len(list), 3)

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
print("1. Kruskal (the networkx version)")
print("2. Kruskal (the authorial version)")
print("3. Boruvka")
print("4. Karger")
print("5. Biswas")
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
        if (chosen_problem not in range (1, 110)):
            print("This is not a valid choice. Please enter a number 1 - 109 or 'R'")
        else:
            chosen_problem_nos.append(chosen_problem)
            more_problems = input("Would you like to choose more problems? (Y, N) Default choice is no. ")
    except ValueError:
        if (chosen_problem != 'R' and chosen_problem != 'r'):
            print("This is not a valid choice. Please enter a number 1 - 109 or 'R'")
        else: 
            chosen_problem_nos.append(chosen_problem)
            more_problems = input("Would you like to choose more problems? (Y, N) Default choice is no. ")

no_of_iterations = input("Would you like to run those algorithms 1 time or 10 times? (1, 10) Default choice is 1. ")
if (no_of_iterations == '10'):
    no_of_iterations = 10
else:
    no_of_iterations = 1

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

kruskal_networkx_times_set = []
kruskal_networkx_memories_set = []
kruskal_times_set = []
kruskal_memories_set = []
karger_times_set = []
karger_memories_set = []
boruvka_times_set = []
boruvka_memories_set = []
biswas_times_set = []
biswas_memories_set = []

problem_parameters = []
for problem in chosen_problems:
    print("-----")
    print(f"Loading problem {problem}")
    problem = tsplib95.load(path + '/' + problem)

    G = problem.get_graph() #our starting graph
    T = nx.Graph() #our minimum spanning tree

    print(f"This problem has {len(G.nodes)} nodes and {len(G.edges)} edges.")
    problem_parameters.append([len(G.nodes), len(G.edges)])

    algorithm_header = []
    kruskal_networkx_times = []
    kruskal_networkx_memories = []
    kruskal_times = []
    kruskal_memories = []
    karger_times = []
    karger_memories = []
    boruvka_times = []
    boruvka_memories = []
    biswas_times = []
    biswas_memories = []

    for i in range(0, no_of_iterations):
        if ('1' in chosen_algorithms):
            print("-----")
            print("Running Kruskal's algorithm (the networkx version) for this problem")
            print(f"iteration no {i+1}")
            original_G = G.copy()
            kruskal_networkx_mst, kruskal_networkx_time, kruskal_networkx_memory = kruskal_tsplib_networkx.Run(G)
            G = original_G
            print("The result is:")
            print(kruskal_networkx_mst.edges)
            if (CheckMSTCorrectness(kruskal_networkx_mst, G)):
                print("This result is correct")
            else:
                print("This result is incorrect")
                exit()
            print(f"The Kruskal's algorithm (the networkx version) needed {kruskal_networkx_time} s to solve problem {problem.name}.")
            print(f"The peak memory consumption of Kruskal's algorithm (the networkx version) for problem {problem.name} is {kruskal_networkx_memory/1000} kB.")
            kruskal_networkx_times.append(kruskal_networkx_time)
            kruskal_networkx_memories.append(kruskal_networkx_memory/1000)
        else:
            kruskal_networkx_times.append("not chosen")
            kruskal_networkx_memories.append("not chosen")

        if ('2' in chosen_algorithms):
            print("-----")
            print("Running Kruskal's algorithm (the authorial version) for this problem")
            print(f"iteration no {i+1}")
            original_G = G.copy()
            kruskal_mst, kruskal_time, kruskal_memory = kruskal_tsplib.Run(G)
            G = original_G
            print("The result is:")
            print(kruskal_mst.edges)
            if (CheckMSTCorrectness(kruskal_mst, G)):
                print("This result is correct")
            else:
                print("This result is incorrect")
                exit()
            print(f"The Kruskal's algorithm (the authorial version) needed {kruskal_time} s to solve problem {problem.name}.")
            print(f"The peak memory consumption of Kruskal's algorithm (the authorial version) for problem {problem.name} is {kruskal_memory/1000} kB.")
            kruskal_times.append(kruskal_time)
            kruskal_memories.append(kruskal_memory/1000)
        else:
            kruskal_times.append("not chosen")
            kruskal_memories.append("not chosen")

        if ('3' in chosen_algorithms):
            print("-----")
            print("Running Boruvka's algorithm for this problem")
            print(f"iteration no {i+1}")
            original_G = G.copy()
            boruvka_mst, boruvka_time, boruvka_memory = boruvka_tsplib.Run(G)
            G = original_G
            print("The result is:")
            print(boruvka_mst.edges)
            if (CheckMSTCorrectness(boruvka_mst, G)):
                print("This result is correct")
            else:
                print("This result is incorrect")
                exit()
            print(f"The Boruvka's algorithm needed {boruvka_time} s to solve problem {problem.name}.")
            print(f"The peak memory consumption of Boruvka's algorithm for problem {problem.name} is {boruvka_memory/1000} kB.")
            boruvka_times.append(boruvka_time)
            boruvka_memories.append(boruvka_memory/1000)
        else:
            boruvka_times.append("not chosen")
            boruvka_memories.append("not chosen")

        if ('4' in chosen_algorithms):
            print("-----")
            print("Running Karger's algorithm for this problem")
            print(f"iteration no {i+1}")
            original_G = G.copy()
            karger_mst, karger_time, karger_memory = karger_tsplib.Run(G)
            G = original_G
            print("The result is:")
            print(karger_mst.edges)
            if (CheckMSTCorrectness(karger_mst, G)):
                print("This result is correct")
            else:
                print("This result is incorrect")
                exit()
            print(f"The Karger's algorithm needed {karger_time} s to solve problem {problem.name}.")
            print(f"The peak memory consumption of Karger's algorithm for problem {problem.name} is {karger_memory/1000} kB.")
            karger_times.append(karger_time)
            karger_memories.append(karger_memory/1000)
        else:
            karger_times.append("not chosen")
            karger_memories.append("not chosen")

        if ('5' in chosen_algorithms):
            print("-----")
            print("Running Biswas' algorithm for this problem")
            print(f"iteration no {i+1}")
            original_G = G.copy()
            biswas_mst, biswas_time, biswas_memory = biswas_tsplib.Run(G)
            G = original_G
            print("The result is:")
            print(biswas_mst.edges)
            if (CheckMSTCorrectness(biswas_mst, G)):
                print("This result is correct")
            else:
                print("This result is incorrect")
                exit()
            print(f"The Biswas' algorithm needed {biswas_time} s to solve problem {problem.name}.")
            print(f"The peak memory consumption of Biswas' algorithm for problem {problem.name} is {biswas_memory/1000} kB.")
            biswas_times.append(biswas_time)
            biswas_memories.append(biswas_memory/1000)
        else:
            biswas_times.append("not chosen")
            biswas_memories.append("not chosen")

    kruskal_networkx_times_set.append(kruskal_networkx_times)
    kruskal_networkx_memories_set.append(kruskal_networkx_memories)
    kruskal_times_set.append(kruskal_times)
    kruskal_memories_set.append(kruskal_memories)
    karger_times_set.append(karger_times)
    karger_memories_set.append(karger_memories)
    boruvka_times_set.append(boruvka_times)
    boruvka_memories_set.append(boruvka_memories)
    biswas_times_set.append(biswas_times)
    biswas_memories_set.append(biswas_memories)

with open('measurements.csv', 'w', encoding='UTF8', newline='') as f:

    writer = csv.writer(f)
    header = ['time [s]']
    writer.writerow(header)
    for i in range(0, len(chosen_problems)):
        problem_header = [chosen_problems[i]]

        algorithm_header = ['Kruskal (networkx)', 'Kruskal (authorial)', 'Karger', 'Boruvka', 'Biswas']

        data = []
        #if (len(kruskal_times_set[0]) > 0 and len(karger_times_set[0]) > 0 and len(boruvka_times_set[0]) > 0):
        for j in range(0, no_of_iterations):
            data.append([kruskal_networkx_times_set[i][j], kruskal_times_set[i][j], karger_times_set[i][j], boruvka_times_set[i][j], biswas_times_set[i][j]])  

        average = [CalculateAverage(kruskal_networkx_times_set[i]), CalculateAverage(kruskal_times_set[i]), CalculateAverage(karger_times_set[i]), CalculateAverage(boruvka_times_set[i]), CalculateAverage(biswas_times_set[i]), '<- average']

        writer.writerow(problem_header)  
        writer.writerow(['no of nodes:', problem_parameters[i][0], 'no of edges:', problem_parameters[i][1]])
        writer.writerow(algorithm_header)

        for row in data:
            writer.writerow(row)

        writer.writerow(average)

    header = ['memory [kB]']
    writer.writerow(header)
    for i in range(0, len(chosen_problems)):
        problem_header = [chosen_problems[i]]
        data = []
        #if (len(kruskal_networkx_memories) > 0 and len(kruskal_memories) and len(karger_memories) > 0 and len(boruvka_memories) > 0):
        for j in range(0, no_of_iterations):
            data.append([kruskal_networkx_memories_set[i][j], kruskal_memories_set[i][j], karger_memories_set[i][j], boruvka_memories_set[i][j], biswas_memories_set[i][j]])  

        average = [CalculateAverage(kruskal_networkx_memories_set[i]), CalculateAverage(kruskal_memories_set[i]), CalculateAverage(karger_memories_set[i]), CalculateAverage(boruvka_memories_set[i]), CalculateAverage(biswas_memories_set[i]), '<- average']

        writer.writerow(problem_header)  
        writer.writerow(['no of nodes:', problem_parameters[i][0], 'no of edges:', problem_parameters[i][1]])
        writer.writerow(algorithm_header)

        for row in data:
            writer.writerow(row)

        writer.writerow(average)


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