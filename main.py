
import random

class Student:
    def __init__(self, id):
        self.id = id

class Department:
    def __init__(self, id, duration, capacity):
        self.id = id
        self.duration = duration
        self.capacity = capacity

class RotationSolution:
    def __init__(self, students, departments, months):
        self.schedule = {student.id: [(None, 0)] * months for student in students}
        self.departments = departments

    def initialize(self):
        for student_id in self.schedule.keys():
            department_order = random.sample(self.departments, len(self.departments))
            month = 0
            for dept in department_order:
                self.schedule[student_id][month:(month + dept.duration)] = [(dept.id, dept.capacity)] * dept.duration
                month += dept.duration

class GeneticAlgorithm:
    def __init__(self, students, departments, population_size, generations, months):
        self.students = students
        self.departments = departments
        self.population_size = population_size
        self.generations = generations
        self.months = months

    def crossover(self, parent1, parent2):
        child1, child2 = RotationSolution(self.students, self.departments, self.months), RotationSolution(self.students, self.departments, self.months)
        for student_id in parent1.schedule.keys():
            crossover_point = random.randint(1, len(parent1.schedule[student_id]) - 1)
            child1.schedule[student_id] = parent1.schedule[student_id][:crossover_point] + parent2.schedule[student_id][crossover_point:]
            child2.schedule[student_id] = parent2.schedule[student_id][:crossover_point] + parent1.schedule[student_id][crossover_point:]
        return child1, child2

    def mutation(self, individual):
        student_id = random.choice(self.students).id
        swap_index1, swap_index2 = random.sample(range(len(self.departments)), 2)
        individual.schedule[student_id][swap_index1], individual.schedule[student_id][swap_index2] = individual.schedule[student_id][swap_index2], individual.schedule[student_id][swap_index1]
        return individual

    def run(self):
        population = [RotationSolution(self.students, self.departments, self.months) for _ in range(self.population_size)]
        for ind in population:
            ind.initialize()

        for generation in range(self.generations):
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(population, 2)
                child1, child2 = self.crossover(parent1, parent2)

                if random.random() < 0.1:  # mutation probability
                    child1 = self.mutation(child1)
                    child2 = self.mutation(child2)

                new_population.extend([child1, child2])

            population = new_population

        best_solution = min(population, key=lambda x: self.calculate_fitness(x))
        return best_solution

    def calculate_fitness(self, individual):
        fitness = 0
        for student_id in individual.schedule.keys():
            # Requirement 2: Each department only once per student
            unique_departments = set([dept_id for dept_id, _ in individual.schedule[student_id] if dept_id is not None])
            if len(unique_departments) != len(self.departments):
                fitness += 1

            # Requirement 3: Limit students per department based on capacity
            student_counts = {dept.id: 0 for dept in self.departments}
            for _, (dept_id, capacity) in enumerate(individual.schedule[student_id]):
                if dept_id is not None:
                    student_counts[dept_id] += 1
                    if student_counts[dept_id] > capacity:
                        fitness += 1

        return fitness

def main():
    students = [Student(id=i) for i in range(1, 21)]
    departments = [Department(id=chr(65 + i), duration=1, capacity=2) for i in range(7)]

    ga = GeneticAlgorithm(students, departments, population_size=100, generations=200, months=len(departments))
    solution = ga.run()

    for student_id, rotation_order in solution.schedule.items():
        departments_string = ' '.join([dept_id for dept_id, _ in rotation_order if dept_id is not None])
        print(f"{student_id}: {departments_string}")

if __name__ == '__main__':
    main()
