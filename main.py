import json
import pandas as pd
import requests
import random


def get_continuous_blocks(lst):
    blocks = []
    current_block = [lst[0]]

    for i in range(1, len(lst)):
        if lst[i] == lst[i - 1]:
            current_block.append(lst[i])
        else:
            blocks.append(current_block)
            current_block = [lst[i]]

    blocks.append(current_block)

    return blocks


def shuffle_blocks(student_expanded_department_ids):
    continuous_blocks = get_continuous_blocks(student_expanded_department_ids)
    random.shuffle(continuous_blocks)

    shuffled_expanded_department_ids = []
    for block in continuous_blocks:
        shuffled_expanded_department_ids.extend(block)

    return shuffled_expanded_department_ids


# Read students.json from URL
students_url = "https://raw.githubusercontent.com/ajietr/cycle/main/students.json"
students_response = requests.get(students_url)
students_data = students_response.json()
students = students_data["students"]

# Read departments.json from URL
departments_url = "https://raw.githubusercontent.com/ajietr/cycle/main/departments.json"
departments_response = requests.get(departments_url)
departments = departments_response.json()

# 根据科室的rotation_duration增加学生department_ids里对应科室的数量
for student in students:
    expanded_department_ids = []
    for dept_id in student["department_ids"]:
        department = next(dept for dept in departments if dept["id"] == dept_id)
        expanded_department_ids.extend([dept_id] * int(department["rotation_duration"]))
    student["expanded_department_ids"] = expanded_department_ids

# 随机重排expanded_department_ids
for student in students:
    student["expanded_department_ids"] = shuffle_blocks(student["expanded_department_ids"])

# 计算总月份数
total_months = len(students[0]["expanded_department_ids"])

# 初始化一个空的字典，用于在每个时间单位内存储每个科室的学生
schedule = {dept["id"]: [""] * total_months for dept in departments}

# 为每个科室的每个时间单位分配学生ID
for student in students:
    for month, dept_id in enumerate(student["expanded_department_ids"]):
        if schedule[dept_id][month]:
            schedule[dept_id][month] += ", "
        schedule[dept_id][month] += str(student["id"])  # Use student ID instead of name

# 将字典转换为DataFrame
dept_names = {dept["id"]: dept["name"] for dept in departments}
df = pd.DataFrame(schedule)
df.rename(columns=dept_names, inplace=True)
df.index.name = "Month"
df.reset_index(inplace=True)
df["Month"] = df["Month"] + 1

# 转置DataFrame
df = df.set_index('Month').transpose().reset_index()
df.index.name = 'Department'
df.reset_index(inplace=True)
df.rename(columns={"index": "Department"}, inplace=True)

# 添加rotation_duration列
df["rotation_duration"] = [dept["rotation_duration"] for dept in departments]

# 保存为Excel文件
df.to_excel("rotation_schedule.xlsx", index=False, engine="openpyxl")