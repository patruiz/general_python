import os 

os.system('cls')
filepath = input("File Path: ")

def file_name(file):
    return int(file[:-4])

files = os.listdir(filepath)
files.sort(key = file_name)

for num in range(len(files)):
    new_file_name = f"{num}.jpg"
    new_file_path = os.path.join(filepath, new_file_name)
    old_file_path = os.path.join(filepath, files[num])
    os.rename(old_file_path, new_file_path)


