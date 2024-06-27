import os 
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

if __name__ == '__main__':
    main()
    
