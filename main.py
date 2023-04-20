import random
import numpy as np
import pandas as pd
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from statistics import mean

DEPARTMENTS = {"A": 1, "B": 2, "C": 2, "D": 2, "E": 2, "F": 2, "G": 2}
STUDENTS = list(range(1, 21))


def evalScheduling(individual):
    total_distance = 0
    student_schedule = individual

    for i, department in enumerate(student_schedule[1:]):
        previous_department = student_schedule[i]
        distance = DISTANCES[previous_department][department]
        total_distance += distance * STUDENTS_WEIGHTS[STUDENTS.index(individual)]

    return total_distance,



def createValidIndividual():
    departments_list = list(DEPARTMENTS.keys())
    student_departments = random.sample(departments_list, len(departments_list))
    return [random.choice(STUDENTS)] + student_departments


def main():
    random.seed(64)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, createValidIndividual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.5)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evalScheduling)

    IND_SIZE = len(DEPARTMENTS) + 1
    POP_SIZE = 100
    NGEN = 1000
    MUTPB = 0.2
    CXPB = 0.8

    population = []
    for student in STUDENTS:
        temp_population = toolbox.population(n=1)
        for ind in temp_population:
            ind.student = student
        population.extend(temp_population)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", mean)
    stats.register("min", min)
    stats.register("max", max)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN,
                                              stats=stats, verbose=True)

    best_schedule = tools.selBest(population, 1)[0]
    print("Best schedule is %s, %s" % (best_schedule, best_schedule.fitness.values))

    return best_schedule



def create_excel(schedule_matrix):
    df = pd.DataFrame(columns=["Department"] + ["Month {}".format(i + 1) for i in range(len(DEPARTMENTS))])

    for department in DEPARTMENTS.keys():
        row = [department]
        for month in range(len(DEPARTMENTS)):
            students_in_month = [str(x[0]) for x in schedule_matrix if x[month + 1] == department]
            row.append(", ".join(students_in_month))
        df.loc[len(df)] = row

    df.to_excel("scheduling_output.xlsx", index=False)


if __name__ == "__main__":
    best_schedule = main()
    schedule_matrix = np.array(best_schedule).reshape(len(STUDENTS), -1).tolist()
    create_excel(schedule_matrix)
