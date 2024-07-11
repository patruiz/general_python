import os 
import pandas as pd 
from pathlib import Path
from Starrett_functions import *

def main():
    os.system('cls')

    file_dir = Path(input("File DIR: "))
    file_name = f"{input('File Name: ')}.csv"
    
    # file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\Starrett Data\1525034\Data\Processed"
    # file_name = "Maryland-Inside - MIS - Copy.CSV"
    
    df_load = load_csv(file_dir, file_name)
    df_data = extract_data(df_load)
    save_csv(df_data, file_dir, file_name, '_PR')
    
    # df_fails = find_fails(df_data)
    # save_csv(df_fails, file_dir, file_name, '_fails')
    # perform_correlation_analysis(df_data)

def correlation():
    cols_to_read = ['Rear', 'Base', 'Mid', 'Tip']
    inside_df = pd.read_csv(r"C:\Users\pr19556\OneDrive - Appl1525034_JawGap_Inside.csvied Medical\Documents\Investigations\02 - MD Jaw Gap\Starrett Data\1524590\Inside\1524590_Inside_PR.csv", usecols=cols_to_read)
    outside_df = pd.read_csv(r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\Starrett Data\1524590\Outside\1524590_Outside_PR.csv", usecols=cols_to_read)
    perform_correlation_analysis(inside_df, outside_df)
    
# def test():
#     inside_path = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\Starrett Data\1525034\Inside\1525034_Inside_PR.csv"
#     outside_path = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\Starrett Data\1525034\Outside\1525034_Outside_PR.csv"
#     filter_outside(inside_path, outside_path)
    
    
if __name__ == '__main__':
    main()
    # correlation()
    # test()
    
