import os 
import pandas as pd 

file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Golden Jaw Force Fixture\Testing\2024\MD AFG\EQ_Prod\Data\Raw"
save_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Golden Jaw Force Fixture\Testing\2024\MD AFG\EQ_Prod"
file_names = ["D02_EQ1_EQ2", "Low_High"]

jf_data = {"High": [], "Low": [], "D_02": [], "EQ_01": [], "EQ_02": []}

df_01 = pd.read_csv(os.path.join(file_dir, file_names[0] + '.csv'), index_col = False)
df_02 = pd.read_csv(os.path.join(file_dir, file_names[1] + '.csv'), index_col = False)

count = 0
for index, val in df_01.iterrows():
    if count == 0:
        jf_data["D_02"].append(float(val["OCR Output"]))
    elif count == 1:
        jf_data["EQ_01"].append(float(val["OCR Output"]))
    elif count == 2:
        jf_data["EQ_02"].append(float(val["OCR Output"]))
    count = count + 1

    if count == 3:
        count = 0

count = 0
for index, val in df_02.iterrows():
    if count == 0:
        jf_data["Low"].append(float(val["OCR Output"]))
    if count == 1:
        jf_data["High"].append(float(val["OCR Output"]))
    count = count + 1

    if count == 2:
        count = 0

os.system('cls')
data = pd.DataFrame.from_dict(jf_data)
data.to_csv(os.path.join(save_dir, 'EQ_Data.csv'), index = False)
print()
print(data.to_string(index = False))