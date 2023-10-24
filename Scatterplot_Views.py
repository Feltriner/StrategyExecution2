import pandas as pd
import matplotlib.pyplot as plt

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

# Pre-processing step to rename columns to a standardized 'Downloads' column 2021
for df in dataframes_21:
    if 'Aufrufe und Downloads' in df.columns:
        df.rename(columns={'Aufrufe und Downloads': 'Downloads'}, inplace=True)
    else:
        df.rename(columns={'Views and Downloads': 'Downloads'}, inplace=True)

# Pre-processing step to rename columns to a standardized 'Downloads' column 2023
for df in dataframes_23:
    if 'Aufrufe und Downloads' in df.columns:
        df.rename(columns={'Aufrufe und Downloads': 'Downloads'}, inplace=True)
    else:
        df.rename(columns={'Views and Downloads': 'Downloads'}, inplace=True)

# Continue with merging using custom suffixes 2021
for index, df in enumerate(dataframes_21):
    try:
        merge_suffix = f"_df{index+1}"
        df_21 = pd.merge(df_21, df[['Name', 'Downloads']], on='Name', how='left', suffixes=('', merge_suffix))
    except KeyError:
        print(f"Error when merging with DataFrame {index+1}")
        break
    except pd.errors.MergeError as e:
        print(f"Merge error with DataFrame {index+1}: {e}")
        break


# Continue with merging using custom suffixes 2023
for index, df in enumerate(dataframes_23):
    try:
        merge_suffix = f"_df{index+1}"
        df_23 = pd.merge(df_23, df[['Name', 'Downloads']], on='Name', how='left', suffixes=('', merge_suffix))
    except KeyError:
        print(f"Error when merging with DataFrame {index+1}")
        break
    except pd.errors.MergeError as e:
        print(f"Merge error with DataFrame {index+1}: {e}")
        break

# Sum up all 'Downloads' columns for the scatter plot
df_21['Views per Student'] = df_21[[col for col in df_21.columns if 'Downloads' in col]].sum(axis=1)

# Sum up all 'Downloads' columns for the scatter plot
df_23['Views per Student'] = df_23[[col for col in df_23.columns if 'Downloads' in col]].sum(axis=1)



# Assuming you've already loaded your DataFrames: df_21 and df_23

# Extracting x and y values for 2021
x_values_21 = df_21['Course total (Real)']
y_values_21 = df_21['Views per Student']

# Convert x_values_23 to numeric while handling non-convertible values
x_values_23 = df_23['Course total (Real)'].replace(',', '.', regex=True).astype(float)
y_values_23 = df_23['Views per Student']

# Individual Scatter Plot for 2021
plt.figure()
plt.scatter(x_values_21, y_values_21, alpha=0.6, color='blue')
plt.xlabel('Grade Points')
plt.ylabel('Views per Student')
plt.title('Scatter Plot of Grade Points vs Views per Student in 2021')
plt.ticklabel_format(style='plain', axis='y')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add a grid for better readability
plt.show()

# Individual Scatter Plot for 2023
plt.figure()
plt.scatter(x_values_23, y_values_23, alpha=0.6, color='red')
plt.xlabel('Grade Points')
plt.ylabel('Views per Student')
plt.title('Scatter Plot of Grade Points vs Views per Student in 2023')
plt.ticklabel_format(style='plain', axis='y')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Add a grid for better readability
plt.show()

# Determine the consistent x-axis and y-axis range for both plots
combined_x_min = min(x_values_21.min(), x_values_23.min())
combined_x_max = max(x_values_21.max(), x_values_23.max())
combined_y_min = min(y_values_21.min(), y_values_23.min())
combined_y_max = max(y_values_21.max(), y_values_23.max())

plt.figure(figsize=(12, 14))

# First subplot for 2021 data
plt.subplot(2, 1, 1)
plt.scatter(x_values_21, y_values_21, alpha=0.6, color='blue')
plt.xlabel('Grade Points', fontsize=12)
plt.ylabel('Views per Student', fontsize=12)
plt.title('Scatter Plot of Grade Points vs Views per Student in 2021', fontsize=14)
plt.xlim(combined_x_min, combined_x_max)
plt.ylim(combined_y_min, combined_y_max)
plt.ticklabel_format(style='plain', axis='both')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Scatter Plot for 2023 in the second subplot
plt.subplot(2, 1, 2)
plt.scatter(x_values_23, y_values_23, alpha=0.6, color='red')
plt.xlabel('Grade Points', fontsize=12)
plt.ylabel('Views per Student', fontsize=12)
plt.title('Scatter Plot of Grade Points vs Views per Student in 2023', fontsize=14)
plt.xlim(combined_x_min, combined_x_max)
plt.ylim(combined_y_min, combined_y_max)
plt.xticks(range(int(combined_x_min), int(combined_x_max)+1, (int(combined_x_max) - int(combined_x_min))//5))
plt.ticklabel_format(style='plain', axis='both')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.tight_layout(pad=3.0)
plt.show()
