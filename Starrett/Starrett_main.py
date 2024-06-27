import os 
import pandas as pd 
from Starrett_functions import *

def main():
    os.system('clear')
    
    file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\Starrett Data\1525034\Inside"
    file_name = "1525034_Inside.csv"
    
    df_load = load_csv(file_dir, file_name)
    df_data = extract_data(df_load)
    save_csv(df_data, file_dir, file_name, '_PR')
    
    # df_fails = find_fails(df_data)
    # save_csv(df_fails, file_dir, file_name, '_fails')
    # perform_correlation_analysis(df_data)

def test():
    cols_to_read = ['Rear', 'Base', 'Mid', 'Tip']
    df1 = pd.read_csv(r"/Users/patrickruiz/Desktop/general_python/Starrett/Data/1524590_Inside_PR.csv", usecols=cols_to_read)
    df2 = pd.read_csv(r"/Users/patrickruiz/Desktop/general_python/Starrett/Data/1524590_Outside_PR.csv", usecols=cols_to_read)
    perform_correlation_analysis(df1, df2)
if __name__ == '__main__':
    # main()
    test()
    
