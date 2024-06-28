import os 
import chardet
import pandas as pd 

file_name = "M8548 (Rev. Pat).csv"
file_dir = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\Golden Jaw Force Fixture\AFG Evaluation\PLC Program\M8548 (Rev. Pat)"
file_path = os.path.join(file_dir, file_name)

# with open(file_path, 'rb') as bytefile:
#     byte_file = bytefile.read()
#     bytedata = chardet.detect(byte_file)
#     encoding = result['encoding']

# csvfile = byte_file.decode('utf-8')
# for i in csvfile.readlines():
#     print(i)
#     # for i in csvfile.readlines():
#     #     # for j in range(len(i.split(';'))):
#     #     for j in range(len(i.decode(encoding = 'utf-8').split(';'))):
#     #         print(j)



# Detect the file's encoding
with open(file_path, 'rb') as bytefile:
    raw_data = bytefile.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

# Read the file with the detected encodings
with open(file_path, 'r', encoding=encoding) as csvfile:
    for line in csvfile.readlines():
        print(line)

# Alternatively, read the CSV file into a DataFrame
df = pd.read_csv(file_path, encoding=encoding)
print(df)
df.to_csv('test.csv')