import zipfile
import os


archive_path = 'c:\\Users\\dbezu\\Desktop\\tst\\http-api-3.1.zip'
extract_dir = 'c:\\Users\\dbezu\\Desktop\\tst\\http-api-3.1'


os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

project_files = []
for root, dirs, files in os.walk(extract_dir):
    for file in files:
        project_files.append(os.path.join(root, file))

print(project_files[:10]) 
