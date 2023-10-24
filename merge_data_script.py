import pandas as pd
import os

# Get the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the directory with the files to merge
directory_path = os.path.join(script_directory, 'data/Files_To_Merge/')

# Get a list of all CSV files in the directory
file_list = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

# Function to determine the suffix based on the file name
def get_suffix_from_filename(file_name):
    if 'HeatMap' in file_name:
        return 'HeatMap'
    elif 'Breakout' in file_name:
        return 'Breakout'
    elif 'ViewsAndDownloads' in file_name:
        return 'ViewsAndDownloads'
    else:
        return ''

# Initialize merged_df with the first file
merged_df = pd.read_csv(os.path.join(directory_path, file_list[0]), delimiter=',')
suffix = get_suffix_from_filename(file_list[0])
if 'Minutes Delivered' in merged_df.columns:
    merged_df.rename(columns={'Minutes Delivered': f'Minutes Delivered {suffix}'}, inplace=True)
merged_df['File Name'] = file_list[0]

# Loop through the rest of the files and merge with the merged_df
for file_name in file_list[1:]:
    df = pd.read_csv(os.path.join(directory_path, file_name), delimiter=',')
    suffix = get_suffix_from_filename(file_name)
    if 'Minutes Delivered' in df.columns:
        df.rename(columns={'Minutes Delivered': f'Minutes Delivered {suffix}'}, inplace=True)
    df['File Name'] = file_name

    # Merge based on all common columns, including 'Name', 'UserName', and 'Email'
    common_cols = list(set(merged_df.columns) & set(df.columns))
    merged_df = pd.merge(merged_df, df, on=common_cols, how='outer')

# Ensure 'File Name' column is the last column
cols = [col for col in merged_df if col != 'File Name'] + ['File Name']
merged_df = merged_df[cols]

# Display the result and additional information
print(merged_df.head())
print('Column Names:',  merged_df.columns)
print('Shape:', merged_df.shape)

# Ensure the 'Merged_Files' directory exists, if not create it
output_directory = os.path.join(script_directory, 'data/Merged_Files/')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Save the result to a CSV file in the 'Merged_Files' directory
merged_df.to_csv(os.path.join(output_directory, 'merged_data.csv'), index=False)
