# COMP 569 - Artificial Intelligence
# Spring 2025
# Group Programming Assignment 2 - 8 Queens
# Group 4: Nicholas Rodriguez Weda, Sarah Vaseem, Tanner Good, Moeeza Nazir, Tamim Sweedan, Luis Olmos

import random
import math

# 8 Queens - can be modified to solve smaller or larger boards
N = 8

############################################################
# -----Helper Functions-----
############################################################

# Generate a random starting board configuration
# index - row, value - where the queen is contained in that row (column)
def generate_random_state():
    return [random.randrange(N) for _ in range(N)]


# Count pairs of queens attacking each other (conflicts)
def conflicts(state):

    count = 0

    # Compare pairs of rows
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j): # checking same column or diagonal
                count += 1

    return count

# Checking the solution found by the Algorithms
def print_board(state):
    if state is None:
        print("No solution found.")
        return
    for r in range(N):
        print(''.join('Q ' if state[r] == c else '. ' for c in range(N)))
    print()

############################################################
# -----Algorithms-----
############################################################

# Hillclimbing Algorithm - Optimization
def hill_climb(max_restarts=1000):
    for _ in range(max_restarts): # loop for a maximum ammount of times or until solution found
        
        state = generate_random_state()
        current_conflicts = conflicts(state)

        while True:
            if current_conflicts == 0:
                return state # True Solution
            
            neighbors = []
            best_conflicts = current_conflicts

            # Explore single move neighbors
            for row in range(N):
                for col in range(N):
                    if col == state[row]:
                        continue

                    # Move the Queen
                    new_state = list(state)
                    new_state[row] = col
                    c = conflicts(new_state)

                    if c < best_conflicts:
                        best_conflicts = c
                        neighbors = [new_state]
                    elif c == best_conflicts:
                        neighbors.append(new_state)
            
            # Keep climbing if there is possible improvement
            if best_conflicts < current_conflicts and neighbors:
                state = random.choice(neighbors)
                current_conflicts = best_conflicts
            else:
                break # local optimum found
    return None # no solution

# Simmulated Annealing Algorithm - Physics/Nature Inspired
def simulated_annealing(max_steps=100000, initial_temp=100.0, alpha=0.99):
    state = generate_random_state()
    current_conflicts = conflicts(state)
    
    # Temperature
    T = initial_temp

    for _ in range(max_steps):

        if current_conflicts == 0:
            return state # True solution!
        
        # Move the Queen
        row = random.randrange(N)
        col = random.randrange(N)
        new_state = list(state)
        new_state[row] = col
        new_conflicts = conflicts(new_state)

        # Change in cost between new solution and current solution
        delta = new_conflicts - current_conflicts

        # Accept better state always, worse state with probability exp(-delta/T)
        if delta < 0 or random.random() < math.exp(-delta / T):
            state = new_state
            current_conflicts = new_conflicts
        
        # Cool Down
        T *= alpha
        if T < 1e-3:
            T = initial_temp # Temp dropped too low, reset to initial

    return None # no solution within max steps

# Genetic Algorithm - Stochastic
def genetic_algorithm(pop_size=100, generations=1000, crossover_rate=0.8, mutation_rate=0.1):

    # Fitness - Number of non-attacking pairs
    def fitness(state):
        # N*(N-1)/2 (Max number of non attacking paris)
        return (N * (N - 1) // 2) - conflicts(state) # subtract conflict count to get fitness score

    # Roulette Wheel
    def selection(population):
        # Find each individual's fitness
        weights = [fitness(ind) for ind in population]
        total = sum(weights)

        if total == 0: # all are unfit, pick at random
            return random.choice(population)
        
        # Pick a random fitness threshold
        pick = random.uniform(0, total)
        current = 0

        # Spin the Wheel!
        for ind, w in zip(population, weights):
            current += w
            if current >= pick:
                return ind

    # Take two parents and make a child!
    def crossover(parent1, parent2):
        # Decide if we should mix at all
        if random.random() > crossover_rate:
            return parent1[:] # skip crossover, clone parent 1
        point = random.randrange(1, N - 1) # pick a random crossover point
        return parent1[:point] + parent2[point:] # child takes a slice of each parent

    # Increase diversity by giving individuals random tweaks
    def mutate(state):
        # Small probability, randomly move a queen
        if random.random() < mutation_rate:
            row = random.randrange(N)
            state[row] = random.randrange(N)
        return state

    # Intial random board
    population = [generate_random_state() for _ in range(pop_size)]

    for _ in range(generations): # loop for set ammount of generations
        population.sort(key=lambda s: conflicts(s)) # sort population by conflicts
        best = population[0]

        if conflicts(best) == 0:
            return best # True solution
        
        new_pop = [best]  # Elitism - carry over the best individual untouched

        # Fill the rest of the population with offspring
        while len(new_pop) < pop_size:
            # Parents
            p1 = selection(population)
            p2 = selection(population)
            # Newly created Children
            child = crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)
        population = new_pop # start the next generation
    return None # no solution

############################################################
# -----Test Cases-----
############################################################
def test_cases():

    # Hill Climb: trivial and boundary cases
    # trivial: max_restarts=1 (likely fail)
    # boundary: max_restarts=1000
    print("Running Hill Climb Test Cases")

    for restarts in [1, 1000]:
        sol = hill_climb(max_restarts=restarts)
        tag = 'trivial' if restarts == 1 else 'boundary' # which case
        print(f"  restarts={restarts} ({tag}) -> conflicts={conflicts(sol) if sol else 'None'}") # status of test

    # Simulated Annealing: edge and typical cases
    # edge: max_steps=0 (no iterations)
    # typical: max_steps=100000
    print("Running Simulated Annealing Test Cases")

    for steps, temp, alpha in [(0, 100.0, 0.99), (100000, 100.0, 0.99)]:
        sol = simulated_annealing(max_steps=steps, initial_temp=temp, alpha=alpha)
        tag = 'edge' if steps == 0 else 'typical' # which case
        print(f"  steps={steps} ({tag}), temp={temp}, alpha={alpha} -> conflicts={conflicts(sol) if sol else 'None'}") # status of case

    # Genetic Algorithm: trivial and larger population cases
    #  trivial: pop_size=1 (minimal diversity)
    #  larger: pop_size=200
    print("Runnning Genetic Algorithm Test Cases")

    for pop, gens in [(1, 100), (200, 500)]:
        sol = genetic_algorithm(pop_size=pop, generations=gens)
        tag = 'trivial' if pop == 1 else 'larger' # which case
        print(f"  pop_size={pop} ({tag}), generations={gens} -> conflicts={conflicts(sol) if sol else 'None'}") # status of case

############################################################
# -----Main-----
############################################################

if __name__ == "__main__":

    # Run Test Cases
    test_cases()
    
    # Run with default parameters
    print("Hill Climbing Solution:")
    hc = hill_climb()
    print_board(hc) # print the board state found

    print("Simulated Annealing Solution:")
    sa = simulated_annealing()
    print_board(sa)

    print("Genetic Algorithm Solution:")
    ga = genetic_algorithm()
    print_board(ga)
