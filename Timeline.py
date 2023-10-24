import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('data/modified_logs_OMBA-Strategy Execution-2023_20230815-1405.csv')
df = df.sort_values('Time', ascending=True).reset_index(drop=True)
# Retain only the necessary columns
df = df[['Time', 'User full name']]
# Convert the 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%d/%m/%y, %H:%M')

# Group by date and count accesses per user per day
daily_counts = df.groupby('Time').size()

# Ensure daily_counts uses a datetime index
daily_counts.index = pd.to_datetime(daily_counts.index)

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

# Create a separate plot for each course segment
for segment, (start_date, end_date) in course_schedule.items():
    segment_data = daily_counts[pd.to_datetime(start_date):pd.to_datetime(end_date)]
    plt.figure(figsize=(12, 6))
    segment_data.plot(label=f"Number of Students accessed Moodle during {segment}")
    plt.legend()
    plt.title(segment)
    plt.tight_layout()
    plt.show()
