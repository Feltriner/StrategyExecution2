import pandas as pd
import os
import sys

def get_current_directory():
    """Get the current directory of the script or .exe file."""
    if getattr(sys, 'frozen', False):  # Running as compiled .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))  # Running as .py script

script_directory = get_current_directory()

# Path to the directory with the files to merge
directory_path = os.path.join(script_directory, 'data', 'Files_To_Merge')

# Get a list of all CSV files in the directory
file_list = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

# Initialize DataFrames
breakout_df_list = []
views_and_downloads_df_list = []
heat_map_df_list = []

# Loop through the files and separate them based on their type
for file_name in file_list:
    df = pd.read_csv(os.path.join(directory_path, file_name), delimiter=',')
    df['File Name'] = file_name  # Add a new column with the file name
    if 'Breakout' in file_name:
        breakout_df_list.append(df)
    elif 'ViewsAndDownloads' in file_name:
        views_and_downloads_df_list.append(df)
    elif 'HeatMap' in file_name:
        heat_map_df_list.append(df)

# Concatenate the DataFrames
breakout_df = pd.concat(breakout_df_list, ignore_index=True)
views_and_downloads_df = pd.concat(views_and_downloads_df_list, ignore_index=True)
heat_map_df = pd.concat(heat_map_df_list, ignore_index=True)

# Print sizes of the DataFrames before merging
print('Size of Breakout DataFrame before merge:', breakout_df.shape)
print('Size of ViewsAndDownloads DataFrame before merge:', views_and_downloads_df.shape)
print('Size of HeatMap DataFrame before merge:', heat_map_df.shape)

# Merge Breakout and ViewsAndDownloads based on User ID
if 'User ID' in views_and_downloads_df.columns and 'Name' in breakout_df.columns:
    unique_user_mapping = views_and_downloads_df[['User ID', 'Name']].drop_duplicates()
    breakout_df = pd.merge(breakout_df, unique_user_mapping, on='Name', how='left')

# Merge the DataFrames
merged_df = pd.concat([breakout_df, views_and_downloads_df, heat_map_df], axis=0, ignore_index=True)

# Reorder columns to put 'File Name' at the end
cols = list(merged_df.columns)
cols.append(cols.pop(cols.index('File Name')))
merged_df = merged_df[cols]

# Print size of the merged DataFrame
print('Size of merged DataFrame:', merged_df.shape)

# Display the result and additional information
print(merged_df.head())
print('Column Names:',  merged_df.columns)
print('Shape:', merged_df.shape)

# Ensure the 'Merged_Files' directory exists, if not create it
output_directory = os.path.join(script_directory, 'data', 'Merged_Files')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Save the result to a CSV file in the 'Merged_Files' directory
merged_df.to_csv(os.path.join(output_directory, 'merged_data.csv'), index=False)
