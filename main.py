import random
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from statistics import mean

def evalOneMax(individual):
    return sum(individual),

def main():
    random.seed(64)

    IND_SIZE = 50
    POP_SIZE = 100
    NGEN = 1000
    MUTPB = 0.2
    CXPB = 0.8

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evalOneMax)

    population = toolbox.population(n=POP_SIZE)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", mean)
    stats.register("min", min)
    stats.register("max", max)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN,
                                              stats=stats, verbose=True)

    best_ind = tools.selBest(population, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    return best_ind

if __name__ == "__main__":
    best_schedule = main()
