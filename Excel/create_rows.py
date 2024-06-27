import pandas as pd
import numpy as np

def create_row_pattern(numbers, repeats):
    """
    Creates a DataFrame with a single column where each number in the provided
    array 'numbers' is repeated 'repeats' times.
    
    Parameters:
    numbers (list[int]): The array of numbers to be repeated.
    repeats (int): The number of times each number should be repeated.
    
    Returns:
    pd.DataFrame: A DataFrame with one column filled with repeated numbers from the input array.
    
    Example:
    >>> create_row_pattern([1, 3, 5], 4)
       Sequence
    0         1
    1         1
    2         1
    3         1
    4         3
    5         3
    6         3
    7         3
    8         5
    9         5
    10        5
    11        5
    """
    # Create an array where each number from the input array 'numbers' is repeated 'repeats' times
    data = np.repeat(numbers, repeats)
    
    # Convert the array into a DataFrame
    df = pd.DataFrame(data, columns=['Sequence'])

    # Print the DataFrame
    print(df)

    # Save the DataFrame to a CSV file without the index
    df.to_csv('create_row_pattern.csv', index=False)

# Example usage:
create_row_pattern([range(1, 281)], 4)
