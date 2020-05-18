import matplotlib.pyplot as plt
import networkx as nx
import random
import operator
import math


class Map:
    def __init__(self, cities, distance_matrix):
        self.cities = cities
        self.distances = distance_matrix
        self.pheromones = []
        self.local_pheromones = []
        for i in range(0, len(cities)):
            self.pheromones.append([1] * len(self.cities))
            self.local_pheromones.append([0] * len(self.cities))
        for i in range(0, len(cities)):
            self.pheromones[i][i] = 0

    def update_pheromone_local(self, fro, to, val):
        self.local_pheromones[fro][to] += val

    def update_pheromones_global(self):
        for i in range(0, len(self.cities)):
            for j in range(0, len(self.cities)):
                self.pheromones[i][j] = (1 - evaporation_factor) * self.pheromones[i][j] + self.local_pheromones[i][j]
        self.reset_locals()

    def get_pheromone(self, fro, to):
        return self.pheromones[fro][to]

    def get_distance(self, fro, to):
        return self.distances[fro][to]

    def reset_locals(self):
        self.local_pheromones.clear()
        for i in range(0, len(self.cities)):
            self.local_pheromones.append([0] * len(self.cities))


class Ant:
    def __init__(self, current, unvisited):
        self.current = current
        self.unvisited = unvisited
        self.trail_length = 0

    def travel_next(self):
        prob = [0] * len(self.unvisited)
        prob_list = [0] * len(self.unvisited)
        fro = ord(self.current) - 65
        sum = 0
        for i in range(0, len(prob)):
            to = ord(self.unvisited[i]) - 65
            # print(country.get_pheromone(fro, to), country.get_distance(fro, to))
            prob[i] = pow(country.get_pheromone(fro, to), alpha) * pow((1 / country.get_distance(fro, to)), beta)
            # print(prob[i])
            sum += prob[i]
        for i in range(0, len(prob)):
            prob[i] /= sum
            # print(prob[i] * sum, prob[i])

        for i in range(0, len(prob)):
            prob_list[i] = (prob[i], self.unvisited[i])

        prob_list.sort(key=operator.itemgetter(0), reverse=True)
        probability = random.random()
        # print("Self= ", self.current)
        # print("Prob= ", probability)
        # print("ProbList= ", prob_list)
        # print()
        dest = -1
        for i in range(0, len(prob_list)):
            if probability < prob_list[i][0]:
                self.current = prob_list[i][1]
                dest = ord(self.current) - 65
                self.trail_length += country.get_distance(fro, dest)
                break
            else:
                probability -= prob_list[i][0]
        self.unvisited.remove(self.current)
        if fro != dest:
            country.update_pheromone_local(fro, dest,
                                           country.get_pheromone(fro, dest) + 1 / country.get_distance(
                                               fro, dest))

    def reset_ant(self):
        self.unvisited.clear()
        self.unvisited += country.cities
        self.unvisited.remove(self.current)
        # print(self.unvisited)
        # print(self.current)


def draw_graph(graph, i):
    G = nx.Graph()
    G.add_edges_from(graph[0])
    pos = nx.spring_layout(G)
    plt.figure(i)
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()})

    nx.draw_networkx_edge_labels(G, pos, edge_labels=graph[1], font_color='red')
    plt.savefig(save_at + 'graph'+str(i)+'.png', dpi=300)
    return G


def init():
    # making nodes
    for i in range(0, node_count):
        nodes.append(chr(i + 65))

    # deciding distances
    for i in range(0, node_count):
        temp = []
        for j in range(0, i):
            temp.append(distances[j][i])
        for j in range(i, node_count):
            if i == j:
                temp.append(0)
            else:
                temp.append(random.randrange(min_distance_limit, max_distance_limit))
        distances.append(temp)


node_count = 5
min_distance_limit = 1
max_distance_limit = 100
iterations = 10
evaporation_factor = 0.5
alpha = 1
beta = 5
save_at = 'C:/Users/Esteev/Desktop/Results/'
nodes = []
copy_nodes = []
edges = []
distances = []
edgeLabels = {}

init()
country = Map(nodes, distances)
ants = []
copy_nodes += nodes
random.shuffle(copy_nodes)
print(distances)
# print(copy_nodes)
# print(nodes)
print()

# Generating Ants
for i in range(0, len(copy_nodes)):
    this_ant = Ant(copy_nodes[i], list(set(copy_nodes) - set(copy_nodes[i])))
    ants.append(this_ant)

# print(country.pheromones)

cur = 0
while cur < iterations:
    for i in range(len(nodes) - 1):
        for ant in ants:
            ant.travel_next()
    best = math.inf
    for ant in ants:
        if best > ant.trail_length:
            best = ant.trail_length
    for ant in ants:
        ant.reset_ant()
    country.update_pheromones_global()
    # print(country.pheromones)
    # print(best)
    cur += 1

# Finding shortest paths based on pheromone values
shortest = []
for i in range(0, node_count):
    max = 0
    for j in range(0, node_count):
        if country.pheromones[i][j] > country.pheromones[i][max]:
            max = j
    shortest.append((chr(i+65), chr(max+65), country.get_distance(i, max)))

print("Best Traversal Distance = ", best)
print("Shortest Paths A to B(A, B) are = ", shortest)


# adding edges and edge labels to distance graph
for i in range(0, node_count):
    for j in range(i+1, node_count):
        if i != j:
            edges.append([nodes[i], nodes[j]])
            edgeLabels[(nodes[i], nodes[j])] = distances[i][j]
distance_graph = [edges, edgeLabels]
dg = draw_graph(distance_graph, 0)

# adding edges and edge labels to pheromone graph
for i in range(0, node_count):
    for j in range(i+1, node_count):
        if i != j:
            edgeLabels[(nodes[i], nodes[j])] = round(country.pheromones[i][j], 2)
pheromone_graph = [edges, edgeLabels]
pg = draw_graph(pheromone_graph, 1)

plt.show()

