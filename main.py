import random
from deap import base
from deap import creator
from deap import tools
import pandas as pd

DEPARTMENTS = ['A', 'B', 'C', 'D', 'E']
SCHEDULE = [1, 2, 3, 4, 5]
STUDENTS = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10']
STUDENTS_WEIGHTS = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("department", random.choice, DEPARTMENTS)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.department, n=len(SCHEDULE))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

DISTANCE_MATRIX = [
    [0, 1, 2, 3, 4],
    [1, 0, 1, 2, 3],
    [2, 1, 0, 1, 2],
    [3, 2, 1, 0, 1],
    [4, 3, 2, 1, 0],
]

def evalScheduling(individual, distance_matrix=DISTANCE_MATRIX):
    total_distance = 0
    student_schedule = individual

    for i, department in enumerate(student_schedule[1:]):
        previous_department = student_schedule[i]
        distance = distance_matrix[previous_department][department]
        total_distance += distance * STUDENTS_WEIGHTS[STUDENTS.index(individual)]

    return total_distance,

toolbox.register("evaluate", evalScheduling)
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def decode_individual(individual):
    return [DEPARTMENTS[department_code] for department_code in individual]

def main():
    random.seed(42)
    pop = toolbox.population(n=50)

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

    def export_to_excel(schedule):
        department_schedule = {department: ['' for _ in range(len(SCHEDULE))] for department in DEPARTMENTS}

        for student, schedule in zip(STUDENTS, schedule):
            for i, department in enumerate(schedule):
                if department_schedule[department][i]:
                    department_schedule[department][i] += ', ' + student
                else:
                    department_schedule[department][i] = student

        df = pd.DataFrame(department_schedule)
        df.index.name = 'Time Slot'
        df.index += 1
        df.to_excel('schedule_output.xlsx', engine='openpyxl')

    best_individual = tools.selBest(pop, 1)[0]
    best_schedule = decode_individual(best_individual)
    export_to_excel(best_schedule)

if __name__ == "__main__":
    main()
