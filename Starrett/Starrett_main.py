import os 
from Starrett_functions import *

def main():
    os.system('clear')
    
    file_dir = r"/Users/patrickruiz/Desktop/general_python/Starrett/Data"
    file_name = "1525034_InsideGap.csv"
    
    df_load = load_csv(file_dir, file_name)
    df_data = extract_data(df_load)
    save_csv(df_data, file_dir, file_name, '_all')
    df_fails = find_fails(df_data)
    save_csv(df_fails, file_dir, file_name, '_fails')

    # perform_correlation_analysis(df_data)

if __name__ == '__main__':
    main()
    
