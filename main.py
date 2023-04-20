import random
from deap import base
from deap import creator
from deap import tools
import pandas as pd

DEPARTMENTS = {'A': 1, 'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 2, 'G': 2}
STUDENTS = list(range(1, 21))

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("department", random.choice, list(DEPARTMENTS.keys()))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.department, n=len(DEPARTMENTS))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

DISTANCE_MATRIX = [
    [0, 1, 2, 3, 4, 5, 6],
    [1, 0, 1, 2, 3, 4, 5],
    [2, 1, 0, 1, 2, 3, 4],
    [3, 2, 1, 0, 1, 2, 3],
    [4, 3, 2, 1, 0, 1, 2],
    [5, 4, 3, 2, 1, 0, 1],
    [6, 5, 4, 3, 2, 1, 0],
]

def evalScheduling(individual, distance_matrix=DISTANCE_MATRIX):
    total_distance = 0
    student_schedule = individual

    for i, department in enumerate(student_schedule[1:]):
        previous_department = student_schedule[i]
        distance = distance_matrix[list(DEPARTMENTS.keys()).index(previous_department)][list(DEPARTMENTS.keys()).index(department)]
        total_distance += distance

    return total_distance,

def cxPartialyMatchedStrings(ind1, ind2):
    size = min(len(ind1), len(ind2))
    p1, p2 = [-1] * size, [-1] * size

    for i in range(size):
        if i < size // 2:
            p1[i] = ind1[i]
            p2[i] = ind2[i]
        else:
            p1[ind1[i]] = i
            p2[ind2[i]] = i

    for i in range(size):
        if p1[i] == -1:
            p1[i] = ind1[p2[i]]
        if p2[i] == -1:
            p2[i] = ind2[p1[i]]

    ind1[:], ind2[:] = p1[:], p2[:]
    return ind1, ind2

toolbox.register("evaluate", evalScheduling)
toolbox.register("mate", cxPartialyMatchedStrings)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)
    pop = toolbox.population(n=50 * len(STUDENTS))

    CXPB, MUTPB, NGEN = 0.7, 0.2, 50

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(offspring)

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

    best_individuals = tools.selBest(pop,1)
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is: %s\nwith fitness: %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()
