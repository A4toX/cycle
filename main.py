import json
from ortools.linear_solver import pywraplp

# 读取数据
with open("students.json", "r", encoding="utf-8") as f:
    students = json.load(f)

with open("dept.json", "r", encoding="utf-8") as f:
    departments = json.load(f)

with open("rules.json", "r", encoding="utf-8") as f:
    rotation_rules = json.load(f)

# 定义线性规划求解器
solver = pywraplp.Solver.CreateSolver("GLOP")

# 定义变量
x = {}
for s in students:
    for d in departments:
        x[(s["id"], d["name"])] = solver.BoolVar(f"x_{s['id']}_{d['name']}")


# 定义约束条件
# 1. 每个学生必须轮转到所有科室
for s in students:
    solver.Add(sum(x[(s["id"], d["name"])] for d in departments) == len(departments))

# 2. 每个科室，每个学生只去一次
for d in departments:
    for s in students:
        solver.Add(sum(x[(s["id"], d["name"])] for d in departments) == 1)

# 3. 计算每个科室每个时间单位的平均人数，并且保证人数尽量控制在平均人数左右
avg_students_per_dept = len(students) * rotation_rules["total_duration"] / sum(d["duration"] for d in departments)
for d in departments:
    solver.Add(sum(x[(s["id"], d["name"])] * d["duration"] for s in students) <= avg_students_per_dept * d["duration"])
    solver.Add(sum(x[(s["id"], d["name"])] * d["duration"] for s in students) >= avg_students_per_dept * d["duration"] - 1)

# 定义目标函数
solver.Minimize(solver.Sum(x[(s["id"], d["name"])] * d["duration"] for s in students for d in departments))

# 求解
status = solver.Solve()

# 输出结果
if status == pywraplp.Solver.OPTIMAL:
    print("Objective value =", solver.Objective().Value())
    for s in students:
        assigned_depts = [d["name"] for d in departments if x[(s["id"], d["name"])].solution_value() == 1]
        print(f"{s['id']} {' '.join(assigned_depts)}")
else:
    print("The problem does not have an optimal solution.")
