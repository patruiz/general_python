import os 
import pandas as pd 

file_name = "1525034_InsideGap.csv"
file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\1525034 - Starrett Data"
file_path = os.path.join(file_dir, file_name)

df = pd.read_csv(file_path)

fails = {}
locations = ['Rear', 'Base', 'Mid', 'Tip']

for index, val in df.iterrows():
    new_fail = {str(index): []}
    for i in range(1, len(val)):
        if (val.iloc[i] <= .003) or (val.iloc[i] >= .006):
            new_fail[str(index)].append(locations[i - 1])
    
    if len(new_fail[str(index)]) != 0:
        fails.update(new_fail)

rear_count, base_count, mid_count, tip_count = 0, 0, 0, 0
for i in fails.keys():
    for j in range(len(fails[str(i)])):
        if fails[str(i)][j] == 'Rear':
            rear_count = rear_count + 1
        elif fails[str(i)][j] == 'Base':
            base_count = base_count + 1
        elif fails[str(i)][j] == 'Mid':
            mid_count = mid_count + 1
        elif fails[str(i)][j] == 'Tip':
            tip_count = tip_count + 1

print(rear_count, base_count, mid_count, tip_count)