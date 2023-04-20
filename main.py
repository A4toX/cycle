import random
from deap import base, creator, tools, algorithms
from collections import namedtuple
from statistics import mean

# 科室和学员信息
departments = {'A': 1, 'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 2, 'G': 2}
students = list(range(1, 21))

# 计算每个科室每个月的最佳人数
total_months = sum(departments.values())
optimal_students_per_dept = {dept: (len(students) * duration) / total_months for dept, duration in departments.items()}

# 定义遗传算法相关参数
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("department", random.choice, list(departments.keys()))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.department, len(departments))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def eval_schedule(individual):
    student_dept_counts = {dept: 0 for dept in departments}

    for dept in individual:
        student_dept_counts[dept] += 1

    deviation = sum((optimal_students_per_dept[dept] - count) ** 2 for dept, count in student_dept_counts.items())
    return deviation,


toolbox.register("evaluate", eval_schedule)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(departments) - 1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)


# 遗传算法主程序
def main():
    random.seed(42)

    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", mean)
    stats.register("min", tools.selBest, k=1)

    population, logbook = algorithms.eaSimple(
        pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100,
        stats=stats, halloffame=hof, verbose=True)

    return hof[0]


# 执行遗传算法
best_schedule = main()

# 输出结果
StudentSchedule = namedtuple("StudentSchedule", ["id", "departments"])
schedules = []

for student_id, department in zip(students, best_schedule):
    schedules.append(StudentSchedule(student_id, department))

for schedule in schedules:
    print(f"{schedule.id} {' '.join(schedule.departments)}")
