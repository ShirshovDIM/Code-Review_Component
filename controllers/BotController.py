import io
import os
import shutil

from pathlib import Path
from zipfile import ZipFile
from glob import glob

from application.assemble_pipeline import archive_report_pipeline, file_report_pipeline
from application.pdf_converter import assemble_document


# Функция для обработки архивов
def process_archive(zip_file, dir_id):
    try:
        with ZipFile(io.BytesIO(zip_file), 'r') as archive:
            tmp_path = f"{os.getcwd()}\\data\\{dir_id}"
            archive.extractall(tmp_path)

            if not os.path.isdir(tmp_path):
                Path(tmp_path).mkdir(parents=True, exist_ok=True)

            try:
                shutil.rmtree(f"{tmp_path}\\__MACOSX")
            except Exception as ex:
                print(ex)

            for report in glob(f"{tmp_path}\\*.pdf"):    
                os.remove(report) 

            project_files = glob(f"{tmp_path}\\**", recursive=True)
            project_name = glob(f"{tmp_path}\\*")[0].split("\\")[-1]
            faker_split = str(dir_id)
            report_dict = archive_report_pipeline(project_files, project_name, faker_split)
            shutil.rmtree(f"{tmp_path}\\{project_name}")
        
        file_dir = f"{tmp_path}\\{project_name}_report.pdf"
        assemble_document(file_dir, report_dict)
        return file_dir
    
    except Exception as ex:
        print(ex)

        raise NotImplementedError

# Функция для обработки файлов и создания репортов
def process_file(file_inst, dir_id, file_name) -> str:
    try: 
        assert file_name.endswith(".py"), AssertionError

        tmp_path = f"{os.getcwd()}\\data\\{dir_id}"

        if not os.path.isdir(tmp_path):
            Path(tmp_path).mkdir(parents=True, exist_ok=True)

        with open(f"{tmp_path}\\{file_name}", "wb") as file: 
            file.write(file_inst)
            
        project_files = glob(f"{tmp_path}\\**", recursive=True)
        faker_split = str(dir_id)
        report_dict = file_report_pipeline(project_files, file_name, faker_split)
        project_name = file_name.split(".py")[0]
        file_dir = f"{tmp_path}\\{project_name}_report.pdf"
        assemble_document(file_dir, report_dict)
        os.remove(f"{tmp_path}\\{file_name}") 
        return file_dir
    
    except Exception as ex:
        print(ex)

        raise NotImplementedError
