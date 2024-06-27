import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_csv(file_dir, file_name):
    """
    Load a CSV file into a DataFrame from the specified directory and file name.

    Parameters:
    - file_dir (str): The directory where the CSV file is located.
    - file_name (str): The name of the CSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing the loaded CSV data.
    """
    file_path = os.path.join(file_dir, file_name)
    return pd.read_csv(file_path)

def extract_data(df):
    """
    Extracts and organizes data from a DataFrame based on the 'Feature' column into specific categories.

    Parameters:
    - df (pd.DataFrame): DataFrame containing 'Feature' and 'Actual' columns where each 'Feature' corresponds to a part of an item.

    Returns:
    - pd.DataFrame: A new DataFrame organized by feature categories with device numbers as the index.
    """
    data = {'Rear': [], 'Base': [], 'Mid': [], 'Tip': []}
    for index, row in df.iterrows():
        # Append actual measurements to corresponding feature category
        if row['Feature'] == 'REAR':
            data['Rear'].append(row['Actual'])
        elif row['Feature'] == 'BASE':
            data['Base'].append(row['Actual'])
        elif row['Feature'] == 'MID':
            data['Mid'].append(row['Actual'])
        elif row['Feature'] == 'TIP':
            data['Tip'].append(row['Actual'])
    # Create device numbers as index based on the number of entries in 'Rear'
    device_num = range(1, len(data['Rear']) + 1)
    return pd.DataFrame(data, columns=data.keys(), index=device_num)

def find_fails(df):
    """
    Identifies rows where any measurement fails to meet specified criteria across specified columns.

    Parameters:
    - df (pd.DataFrame): DataFrame containing measurements in specific columns.

    Returns:
    - pd.DataFrame: Filtered DataFrame containing only rows where at least one measurement failed the criteria.
    """
    lower_bound, upper_bound = 0.003, 0.006  # Define bounds for failure criteria
    locations = ['Rear', 'Base', 'Mid', 'Tip']
    # Create a boolean mask for failures
    fail_mask = (df[locations] < lower_bound) | (df[locations] > upper_bound)
    return df[fail_mask.any(axis=1)]

def perform_correlation_analysis(data_frame):
    """
    Calculates and visualizes the correlation matrix for the DataFrame.

    Parameters:
    - data_frame (pd.DataFrame): DataFrame where each column is a variable and each row is an observation.

    Returns:
    - pd.DataFrame: The computed correlation matrix.
    """
    correlation_matrix = data_frame.corr()  # Calculate correlation matrix
    print("Correlation Matrix:")
    print(correlation_matrix)
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='cool', fmt=".2f", linewidths=.5)
    plt.title('Jaw Gap Correlation Graph')
    plt.show()
    return correlation_matrix

def save_csv(df, file_dir, file_name, suffix):
    """
    Saves the DataFrame to a CSV file with a specified suffix in the file name.

    Parameters:
    - df (pd.DataFrame): The DataFrame to be saved.
    - file_dir (str): The directory to save the CSV file in.
    - file_name (str): The base file name without the suffix.
    - suffix (str): The suffix to append to the file name before saving.

    Returns:
    - None: The function saves the file and does not return any value.
    """
    save_name = f"{file_name}{suffix}.csv"
    save_path = os.path.join(file_dir, save_name)
    df.to_csv(save_path)