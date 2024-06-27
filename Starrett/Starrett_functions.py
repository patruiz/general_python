import os
import pandas as pd

def load_csv(file_dir, file_name):
    """
    Loads a Starrett Jaw Gap data CSV file into a DataFrame from the specified directory and file name.

    Parameters:
    file_dir (str): The directory where the CSV file is located.
    file_name (str): The name of the CSV file.

    Returns:
    DataFrame: A DataFrame containing the loaded CSV data.
    """
    file_path = os.path.join(file_dir, file_name)
    return pd.read_csv(file_path)

def extract_data(df):
    """
    Processes measurements from a DataFrame, categorizes them by feature type, and returns a new DataFrame
    organized by these categories.

    Parameters:
    df (DataFrame): A DataFrame containing the raw measurement data.

    Returns:
    DataFrame: A new DataFrame organized by feature categories.
    """
    # Dictionary to collect data based on feature type
    data = {'Rear': [], 'Base': [], 'Mid': [], 'Tip':[]}

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        # Append the 'Actual' measurement to the appropriate list based on 'Feature' value
        if row['Feature'] == 'REAR':
            data['Rear'].append(row['Actual'])
        elif row['Feature'] == 'BASE':
            data['Base'].append(row['Actual'])
        elif row['Feature'] == 'MID':
            data['Mid'].append(row['Actual'])
        elif row['Feature'] == 'TIP':
            data['Tip'].append(row['Actual'])

    # Generate a sequence of device numbers based on the length of the 'Rear' feature data
    device_num = range(1, len(data['Rear']) + 1)

    # Create a new DataFrame from the processed data
    return pd.DataFrame(data, columns=data.keys(), index=device_num)

def find_fails(df):
    """
    Analyzes data from a DataFrame for failure rates based on measurement values and jaw locations, and
    prints the count of failures per location.

    Parameters:
    df (DataFrame): A DataFrame containing the measurement data to analyze.

    Returns:
    None: This function prints the counts of failures per specified location.
    """
    # Dictionary to store failure counts by location
    fails = {}
    locations = ['Rear', 'Base', 'Mid', 'Tip']

    # Iterate over each row in the DataFrame to identify failures
    for index, row in df.iterrows():
        new_fail = {str(index): []}
        for i in range(1, len(row)):
            # Check if the value falls outside the acceptable range
            if (row.iloc[i] <= 0.003) or (row.iloc[i] >= 0.006):
                new_fail[str(index)].append(locations[i - 1])

        # If any failures are found, add them to the fails dictionary
        if len(new_fail[str(index)]) != 0:
            fails.update(new_fail)

    # Count the number of failures for each location
    rear_count, base_count, mid_count, tip_count = 0, 0, 0, 0
    for key in fails.keys():
        for location in fails[str(key)]:
            if location == 'Rear':
                rear_count += 1
            elif location == 'Base':
                base_count += 1
            elif location == 'Mid':
                mid_count += 1
            elif location == 'Tip':
                tip_count += 1

    # Print the failure counts for each location
    print(f"Rear: {rear_count}, Base: {base_count}, Mid: {mid_count}, Tip: {tip_count}")
