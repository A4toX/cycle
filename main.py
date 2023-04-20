import random
import numpy as np

def generate_initial_population(num_students, departments):
    population = []
    for _ in range(num_students):
        individual = random.sample(departments, len(departments))
        population.append(individual)
    return population

def fitness(schedule, num_students, departments_duration, max_students_per_department):
    fitness_value = 0
    for month in range(1, 15):
        dept_count = {dept: 0 for dept in departments_duration}
        for student in range(num_students):
            for dept, duration in [(dept, departments_duration[dept]) for dept in schedule[student]]:
                if month >= duration:
                    month -= duration
                    dept_count[dept] += 1
                    break
        if all([count <= max_students_per_department for count in dept_count.values()]):
            fitness_value += 1
    return fitness_value


def crossover(parent1, parent2, num_students):
    crossover_point = random.randint(1, num_students - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, departments):
    i, j = random.sample(range(len(individual)), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual

def genetic_algorithm(num_students, departments_duration, max_students_per_department, population_size=100, generations=1000, mutation_rate=0.1):
    departments = list(departments_duration.keys())
    population = [generate_initial_population(num_students, departments) for _ in range(population_size)]

    for gen in range(generations):
        population_fitness = [fitness(ind, num_students, departments_duration, max_students_per_department) for ind in population]
        if max(population_fitness) == 14:  # 最大适应度值为14，因为总共有14个月
            break

        new_population = []
        for _ in range(population_size // 2):
            parents = random.choices(population, weights=population_fitness, k=2)
            children = crossover(parents[0], parents[1], num_students)

            if random.random() < mutation_rate:
                children = (mutate(children[0], departments), mutate(children[1], departments))

            new_population.extend(children)

        population = new_population

    best_individual = population[np.argmax(population_fitness)]

    # 将科室和轮转时长重新组合
    best_schedule = []
    for student in best_individual:
        student_schedule = []
        for dept in student:
            student_schedule.append((dept, departments_duration[dept]))
        best_schedule.append(student_schedule)

    return best_schedule

if __name__ == "__main__":
    num_students = 20
    departments_duration = {'A': 1, 'B': 2, 'C': 3, 'D': 2, 'E': 2, 'F': 2, 'G': 2}
    max_students_per_department = 3

    best_solution = genetic_algorithm(num_students, departments_duration, max_students_per_department)
    for idx, student_schedule in enumerate(best_solution):
        print(f"Student {idx + 1}: {student_schedule}")