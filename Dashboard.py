import pandas as pd
from tabulate import tabulate

# Load the data
df = pd.read_csv('data/modified_logs_OMBA-Strategy Execution-2023_20230815-1405.csv')
df = df.sort_values('Time', ascending=True).reset_index(drop=True)

# Retain only the necessary columns
df = df[['Time', 'User full name']]

# Convert 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%d/%m/%y, %H:%M')

# Define course schedule
course_schedule = {
    "Pre-course": ["2022-12-12", "2023-01-02"],
    "Week 1": ["2023-01-02", "2023-01-08"],
    "Week 2": ["2023-01-09", "2023-01-14"],
    "Week 3": ["2023-01-15", "2023-01-21"],
    "Week 4": ["2023-01-22", "2023-01-28"],
    "Pre-exam": ["2023-01-28", "2023-02-12"],
    "Post-course": ["2023-02-12", "2023-03-12"]
}

# Total number of students
total_students = 58

# Count the number of unique students
unique_students_count = df['User full name'].nunique()

# Print the result
print(f"Total number of unique students: {unique_students_count}")

# Get all unique student names
unique_student_names = df['User full name'].unique()

unique_student_names = sorted(unique_student_names)

# Print each unique name
for name in unique_student_names:
    print(name)

# Create a table for the desired metrics
table_data = {
    "Time Schedule": [],
    "Total Accesses": [],
    "Avg Access per Student": [],
    "Number of Students Accessed": [],
    "Number of Students Did Not Access": []
}

for segment, (start_date, end_date) in course_schedule.items():
    segment_df = df[(df['Time'] >= start_date) & (df['Time'] <= end_date)]

    # Total accesses
    total_accesses = segment_df.shape[0]

    # Number of unique students who accessed
    students_accessed = segment_df['User full name'].nunique()

    # Average access per student (rounded to 1 decimal place)
    avg_access = round(total_accesses / students_accessed, 1) if students_accessed != 0 else 0

    # Number of students who did not access
    students_did_not_access = total_students - students_accessed

    # Append data to table_data dictionary
    table_data["Time Schedule"].append(segment)
    table_data["Total Accesses"].append(total_accesses)
    table_data["Avg Access per Student"].append(avg_access)
    table_data["Number of Students Accessed"].append(students_accessed)
    table_data["Number of Students Did Not Access"].append(students_did_not_access)

# Convert dictionary to DataFrame
table_df = pd.DataFrame(table_data)

# Display the table using tabulate
print(tabulate(table_df, headers='keys', tablefmt='grid', showindex=False))
