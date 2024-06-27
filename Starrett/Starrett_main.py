import os 
from Starrett.Starrett_functions import load_csv, extract_data, find_fails

def main():
    file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\1525034 - Starrett Data"
    file_name = "1525034_InsideGap.csv"
    
    df = load_csv(file_dir, file_name)
    df = extract_data(df)
    df = find_fails(df)

if __name__ == '__main__':
    main()