# Ant colony optimization
 Python implementation of Ant Colony Optimization with networkx

### Variables:
1. node_count: represents the number of cities
2. min_distance_limit: Least distance possible between two cities
3. max_distance_limit: Maximum distance possible between two cities
4. iterations: Number of complete node traversals for each ant
5. evaporation_factor: Rate of evaporation of pheromone
6. alpha: Weight of pheromone importance
7. beta: Weight of heuristic importance

### Assumptions:
1. Number of ants used = Number of cities
2. Heuristic (A, B) -> 1 / (Distance from City A to City B)
3. Each ant deposits the same amount of pheromone in a city path divided by the distance between the two cities. i.e. local_new_pheromone (i, j) = local_old_pheromone(i, j) + 1 / distance(i, j) when an ant travels from city i to j.
4. Pheromones are updated locally until all the ants have travelled completely. Then the pheromones are updated globally with evaporation. i.e. For all i and j global_pheromone(i, j) = (1 – evaporation_factor) * global_pheromone(i, j) + local_pheromone(i, j), when all the ants have travelled.
5. All path pheromone values are updated to 1 initially.
6. Directory save_at exists to store graphs

### Libraries Used:
1. network - for constructing graphs
2. matplotlib – for plotting graphs

### Approach:
1. Randomly generating distances between all node_count cities and initializing the nodes as states, and ants
2. Each ant traverses from a random start point towards the next city with probabilities based on existing pheromone deposit on the trail weighted by alpha, heuristic of distance weighted by beta and the probabilities of rest of the cities that may be visited. This step is repeated till there are no new cities to visit. A city once visited is not visited again, so there is guarantee of finishing all the nodes.
3. Pheromones are updated based on distance on a local basis. Once all the ants complete traversing all the cities then the pheromones are updated globally.
4. Process is repeated till number of iterations are finished and best distance sum is printed.
Observations
5. alpha and beta play an important role in the rate of success. Finding the balance to these is the key to finding the shortest path in Travelling salesman problem. As alpha denotes the weightage given to the pheromone trail and beta denotes the weightage of heuristic (1 / distance) the probability of going to the next city changes by a lot.
Optimal solutions were more generally observed at the values: alpha = 1 and beta = 5
6. If there is small difference between distances from a city to two or more cities in the way to the destination, then the city with more distance may be picked by the ants if their ancestors also picked the same, i.e. pheromone stacks up.
7. As the number of cities increase, the probability of finding the shortest path decreases.
8. Number of iterations are helpful till a certain degree, after that the same trails are used because of accumulation of too much pheromone on them.
9. Ants will pick new cities to explore (Exploration), but also favour the city paths with more pheromone deposited on them (Exploitation.)
10. Value of evaporation_factor at 0.5 is a balanced key for retaining information as well as aiding further learning.

### Results and Inferences
1. Works better when number of nodes are less.
2. Value of beta should be higher than alpha, else the ants will be more bound to repeat the routes the previous ants took. But beta should be kept in check else the pheromones will have little effect.
3. Evaporation Factor guides the importance of the newest iteration vs learning performed in the previous iterations. Striking a balance with this factor is essential to avoid getting stuck with non-optimal data or not retaining information at all.
4. After some iterations, increasing the number of iterations further does not improve the result as new ants follow the paths more traversed by previous ants and probability of exploration becomes very low.

The pheromone values of trails that aren’t traversed have been reduced to 0 by evaporation and shorter paths have loads of pheromones deposited on them.
