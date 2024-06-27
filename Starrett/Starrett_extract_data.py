import os
import pandas as pd 

file_name = "1525034_InsideGap.csv"
file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Investigations\02 - MD Jaw Gap\1525034 - Starrett Data"
file_path = os.path.join(file_dir, file_name)

df = pd.read_csv(file_path)
data = {'Rear': [], 'Base': [], 'Mid': [], 'Tip':[]}

for index, val in df.iterrows():
    if val.loc['Feature'] == 'REAR':
        data['Rear'].append(val.loc['Actual'])
    elif val.loc['Feature'] == 'BASE':
        data['Base'].append(val.loc['Actual'])
    elif val.loc['Feature'] == 'MID':
        data['Mid'].append(val.loc['Actual'])
    elif val.loc['Feature'] == 'TIP':
        data['Tip'].append(val.loc['Actual'])

device_num = range(len(data['Rear']))
new_df = pd.DataFrame(data, columns = data.keys(), index = device_num)
new_df.to_csv(file_name)