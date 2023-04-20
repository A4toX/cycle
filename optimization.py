import pandas as pd
import numpy as np
import random


def count_students(data, department, month):
    return len(data.loc[(data['Department'] == department) & (data['Month'] == month)])


def optimize_schedule(schedule_file, max_difference=1):
    data = pd.read_excel(schedule_file)
    departments = data['Department'].unique()
    months = data['Month'].unique()

    while True:
        department_month_counts = []
        for department in departments:
            for month in months:
                department_month_counts.append((department, month, count_students(data, department, month)))

        department_month_counts = sorted(department_month_counts, key=lambda x: x[2], reverse=True)
        max_count = department_month_counts[0][2]
        min_count = department_month_counts[-1][2]

        if max_count - min_count <= max_difference:
            break

        max_dept, max_month, _ = department_month_counts[0]
        min_dept, min_month, _ = department_month_counts[-1]

        max_students = data.loc[(data['Department'] == max_dept) & (data['Month'] == max_month)]
        random_student_id = max_students.sample(n=1).iloc[0]["ID"]

        min_students = data.loc[(data['Department'] == min_dept) & (data['Month'] == min_month)]

        for _, min_student in min_students.iterrows():
            if not data.loc[(data['ID'] == min_student["ID"]) & (data['Department'] == max_dept)].empty:
                continue

            data.loc[(data['ID'] == random_student_id) & (data['Department'] == max_dept), 'Month'] = min_month
            data.loc[(data['ID'] == min_student["ID"]) & (data['Department'] == min_dept), 'Month'] = max_month
            break

    data.to_excel('optimized_schedule.xlsx', index=False)


if __name__ == '__main__':
    schedule_file = 'rotation_schedule.xlsx'
    optimize_schedule(schedule_file)
