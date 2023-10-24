import pandas as pd
import matplotlib.pyplot as plt

# Read main grade dataframes
df_21 = pd.read_csv('data/OMBA - Strategy Execution - 2021 Grades.csv', delimiter=';')
df_23 = pd.read_csv('data/OMBA - Strategy Execution - 2023 Grades.csv', delimiter=';')

# Read 2021 data
df_01_1_2021 = pd.read_csv('data/Panopto_2021/01_1_2021.csv', delimiter=',')
df_01_2_2021 = pd.read_csv('data/Panopto_2021/01_2_2021.csv', delimiter=',')
df_01_3_2021 = pd.read_csv('data/Panopto_2021/01_3_2021.csv', delimiter=',')
df_02_1_2021 = pd.read_csv('data/Panopto_2021/02_1_2021.csv', delimiter=',')
df_03_1_2021 = pd.read_csv('data/Panopto_2021/03_1_2021.csv', delimiter=',')
df_03_2_2021 = pd.read_csv('data/Panopto_2021/03_2_2021.csv', delimiter=',')
df_04_1_2021 = pd.read_csv('data/Panopto_2021/04_1_2021.csv', delimiter=',')
df_04_2_2021 = pd.read_csv('data/Panopto_2021/04_2_2021.csv', delimiter=',')

# Read 2023 data
df_01_1_2023 = pd.read_csv('data/Panopto_2023/01_1_2023.csv', delimiter=',')
df_01_2_2023 = pd.read_csv('data/Panopto_2023/01_2_2023.csv', delimiter=',')
df_01_3_2023 = pd.read_csv('data/Panopto_2023/01_3_2023.csv', delimiter=',')
df_02_1_2023 = pd.read_csv('data/Panopto_2023/02_1_2023.csv', delimiter=',')
df_03_1_2023 = pd.read_csv('data/Panopto_2023/03_1_2023.csv', delimiter=',')
df_03_2_2023 = pd.read_csv('data/Panopto_2023/03_2_2023.csv', delimiter=',')
df_04_1_2023 = pd.read_csv('data/Panopto_2023/04_1_2023.csv', delimiter=',')
df_04_2_2023 = pd.read_csv('data/Panopto_2023/04_2_2023.csv', delimiter=',')

# List of 2021 dataframes
dataframes_21 = [
    df_01_1_2021, df_01_2_2021, df_01_3_2021, df_02_1_2021, df_03_1_2021,
    df_03_2_2021, df_04_1_2021, df_04_2_2021
]

# List of 2023 dataframes
dataframes_23 = [
    df_01_1_2023, df_01_2_2023, df_01_3_2023, df_02_1_2023, df_03_1_2023,
    df_03_2_2023, df_04_1_2023, df_04_2_2023
]

# Create a combined Name column for df_21
df_21['Name'] = df_21['First name'] + " " + df_21['Surname']

# Create a combined Name column for df_23
df_23['Name'] = df_23['First name'] + " " + df_23['Surname']

# Sum 'Minutes Delivered' across all 2021 dataframes
total_minutes_21 = pd.concat(dataframes_21).groupby('Name')['Minutes Delivered'].sum().reset_index()

# Sum 'Minutes Delivered' across all 2023 dataframes
total_minutes_23 = pd.concat(dataframes_23).groupby('Name')['Minutes Delivered'].sum().reset_index()

# Merge summed minutes with main grade dataframe for 2021 based on 'Name'
df_21 = pd.merge(df_21, total_minutes_21, on='Name', how='left')

# Merge summed minutes with main grade dataframe for 2023 based on 'Name'
df_23 = pd.merge(df_23, total_minutes_23, on='Name', how='left')

# Scatter Plot for 2021
plt.figure()  # Create a new figure window
x_values_21 = df_21['Course total (Real)']
y_values_21 = df_21['Minutes Delivered']
plt.scatter(x_values_21, y_values_21, alpha=0.6, color='blue')
plt.xlabel('Grade Points')
plt.ylabel('Minutes Delivered')
plt.title('Scatter Plot of Grade Points vs Minutes Delivered per Student in 2021')
plt.ticklabel_format(style='plain', axis='y')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Adding grid for 2021 plot
plt.show()  # Display the first plot


# Convert strings with commas to float values
x_values_23 = df_23['Course total (Real)'].replace(',', '.', regex=True).astype(float)
y_values_23 = df_23['Minutes Delivered']

# Scatter Plot for 2023
plt.figure()  # Create another new figure window
plt.scatter(x_values_23, y_values_23, alpha=0.6, color='red')
plt.xlabel('Grade Points')
plt.ylabel('Minutes Delivered')
plt.title('Scatter Plot of Grade Points vs Minutes Delivered per Student in 2023')
x_max = x_values_23.max()
x_min = x_values_23.min()
plt.xticks(range(int(x_min), int(x_max)+1, (int(x_max) - int(x_min))//5))  # Adjust this for your preferred number of ticks
plt.ticklabel_format(style='plain', axis='y')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Adding grid for 2023 plot
plt.show()  # Display the second plot



plt.figure(figsize=(12, 14))  # Increase the figure size for better spacing

# Determine the consistent x-axis range for both plots
combined_x_min = min(x_values_21.min(), x_values_23.min())
combined_x_max = max(x_values_21.max(), x_values_23.max())

# Determine the consistent y-axis range for both plots
combined_y_min = min(y_values_21.min(), y_values_23.min())
combined_y_max = max(y_values_21.max(), y_values_23.max())

# First subplot for 2021 data
plt.subplot(2, 1, 1)  # 2 rows, 1 column, first plot
plt.scatter(x_values_21, y_values_21, alpha=0.6, color='blue')
plt.xlabel('Grade Points', fontsize=12)
plt.ylabel('Minutes Delivered', fontsize=12)
plt.title('Scatter Plot of Grade Points vs Minutes Delivered per Student in 2021', fontsize=14)
plt.xlim(combined_x_min, combined_x_max)  # Set x-axis range for 2021 plot
plt.ylim(combined_y_min, combined_y_max)  # Set y-axis range for 2021 plot
plt.ticklabel_format(style='plain', axis='both')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add a grid for better readability

# Scatter Plot for 2023 in the second subplot
plt.subplot(2, 1, 2)  # 2 rows, 1 column, second plot
plt.scatter(x_values_23, y_values_23, alpha=0.6, color='red')
plt.xlabel('Grade Points', fontsize=12)
plt.ylabel('Minutes Delivered', fontsize=12)
plt.title('Scatter Plot of Grade Points vs Minutes Delivered per Student in 2023', fontsize=14)
plt.xlim(combined_x_min, combined_x_max)  # Set x-axis range for 2023 plot
plt.ylim(combined_y_min, combined_y_max)  # Set y-axis range for 2023 plot
plt.xticks(range(int(combined_x_min), int(combined_x_max)+1, (int(combined_x_max) - int(combined_x_min))//5))
plt.ticklabel_format(style='plain', axis='both')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add a grid for better readability

plt.tight_layout(pad=3.0)  # Adjusts spacing between subplots and adds padding
plt.show()
