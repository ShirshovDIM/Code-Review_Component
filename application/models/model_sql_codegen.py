import os
import re
import sys


project_path = 'c:\\Users\\dbezu\\Desktop\\tst\\FlaskApiEcommerce-master'
class SQLAlchemyModelParser:
    """Парсер SQLAlchemy моделей с использованием регулярных выражений"""
    
    def __init__(self, project_path: str):
        """
        Инициализация парсера моделей
        
        Args:
            project_path (str): Корневой путь проекта
        """
        self.project_path = project_path
        self.models_data = []
        
        # Регулярные выражения для извлечения информации о моделях
        self.patterns = {
            'model_class': r'class\s*(\w+)\s*\(\s*(?:.*?db\.Model\s*\))?:',
            'table_name': r'__tablename__\s*=\s*[\'"](\w+)[\'"]',
            'column_pattern': r'(\w+)\s*=\s*db\.Column\(\s*(.*?)\s*\)',
            'column_type': r'[A-Za-z]+\.(Integer|String|DateTime|Boolean|Float|Text)'
        }

    def find_python_files(self) -> list:
        """
        Поиск Python-файлов в проекте
        
        Returns:
            list: Пути к найденным файлам
        """
        py_files = []
        for root, _, files in os.walk(self.project_path):
            py_files.extend([
                os.path.join(root, file) 
                for file in files 
                if file.endswith('.py')
            ])
        return py_files

    def extract_model_info(self, file_path: str):
        """
        Извлечение информации о моделях из файла
        
        Args:
            file_path (str): Путь к файлу
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Поиск классов моделей
        for model_match in re.finditer(self.patterns['model_class'], content, re.MULTILINE | re.DOTALL):
            model_name = model_match.group(1)
            
            # Поиск имени таблицы
            table_match = re.search(self.patterns['table_name'], content)
            table_name = table_match.group(1) if table_match else model_name.lower() + 's'
            
            # Поиск колонок
            columns = []
            for col_match in re.finditer(self.patterns['column_pattern'], content):
                col_name = col_match.group(1)
                col_definition = col_match.group(2)
                
                # Извлечение типа колонки
                type_match = re.search(self.patterns['column_type'], col_definition)
                col_type = type_match.group(1) if type_match else 'String'
                
                columns.append({
                    'name': col_name,
                    'type': col_type,
                    'primary_key': 'primary_key=True' in col_definition,
                    'nullable': 'nullable=False' not in col_definition
                })
            
            # Сохранение информации о модели
            self.models_data.append({
                'model_name': model_name,
                'table_name': table_name,
                'columns': columns
            })

    def generate_ddl(self, output_path: str = 'ddl_queries.sql'):
        """
        Генерация DDL-запросов для найденных моделей
        
        Args:
            output_path (str): Путь для сохранения SQL-файла
        
        Returns:
            str: Сгенерированные DDL-запросы
        """
        ddl_queries = []
        
        # Преобразование типов SQLAlchemy в SQL-типы
        type_mapping = {
            'Integer': 'INTEGER',
            'String': 'VARCHAR(255)',
            'DateTime': 'TIMESTAMP',
            'Boolean': 'BOOLEAN',
            'Float': 'FLOAT',
            'Text': 'TEXT'
        }
        
        for model in self.models_data:
            columns = []
            for col in model['columns']:
                col_def = f"{col['name']} {type_mapping.get(col['type'], 'VARCHAR(255)')}"
                
                if col['primary_key']:
                    col_def += " PRIMARY KEY"
                
                if not col['nullable']:
                    col_def += " NOT NULL"
                
                columns.append(col_def)
            
            create_table_query = f"CREATE TABLE {model['table_name']} (\n    " + \
                                 ",\n    ".join(columns) + "\n);"
            ddl_queries.append(create_table_query)
        
        # Запись в файл
        ddl_content = "\n\n".join(ddl_queries)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ddl_content)
        
        return ddl_content

def main(project_path: str):
    """
    Основная функция для парсинга и генерации DDL
    
    Args:
        project_path (str): Корневой путь проекта
    """
    parser = SQLAlchemyModelParser(project_path)
    
    # Поиск и парсинг файлов
    for file_path in parser.find_python_files():
        parser.extract_model_info(file_path)
    
    # Генерация DDL
    ddl_queries = parser.generate_ddl()
    print(f"Найдено моделей: {len(parser.models_data)}")
    print("DDL-запросы сгенерированы в ddl_queries.sql")
        
        # Запись в файл
    # ddl_content = "\n\n".join(ddl_queries)
    # with open(project_path, 'w', encoding='utf-8') as f:
    #     f.write(ddl_content)
        
    return ddl_queries


if __name__ == "__main__":
    print(main(project_path))