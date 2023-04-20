import random
import json

# 定义科室列表
department_names = [f"科室{i}" for i in range(1, 11)]
departments = [{"id": i+1, "name": department_names[i], "rotation_duration": f"{(i+1)*4}周"} for i in range(10)]

# 定义学生列表
students = []
for i in range(1, 21):
    student = {"id": i, "name": f"学生{i}"}
    # 随机选择8个科室
    department_ids = random.sample(range(1, 11), 8)
    student["department_ids"] = department_ids
    students.append(student)

# 生成JSON数据
data = {"departments": departments, "students": students}

# 将JSON数据写入文件
with open('students.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON文件已生成！")
