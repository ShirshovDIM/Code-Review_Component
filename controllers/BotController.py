import io
import os
import shutil

from zipfile import ZipFile
from glob import glob

from application.assemble_pipeline import report_pipeline
from application.pdf_converter import assemble_document


# Функция для обработки архивов
def process_archive(zip_file, dir):
    with ZipFile(io.BytesIO(zip_file), 'r') as archive:
        tmp_path = f"{os.getcwd()}\\data\\{dir}"
        archive.extractall(tmp_path)
        project_files = glob(f"{tmp_path}\\**", recursive=True)
        project_name = glob(f"{tmp_path}\\*")[0].split("\\")[-1]
        print(project_name)
        report_dict = report_pipeline(project_files, project_name)
        shutil.rmtree(f"{tmp_path}\\{project_name}")
    
    file_dir = f"{tmp_path}\\{project_name}_report.pdf"
    assemble_document(file_dir, report_dict)
    return file_dir
# Функция для обработки файлов и создания репортов
def process_file(file) -> str:
    # Здесь должна быть логика обработки файла
    print("Processing file:", file)
    report = assemble_document("report.pdf", {"Respond":"Hello world"})
    return report
