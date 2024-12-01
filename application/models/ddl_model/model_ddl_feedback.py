import os
import re

from string import Template

from application.models.ddl_model.model_embedded import get_evrazgpt_response


class SQLAlchemyModelParser:
    
    def __init__(self):
        self.models_data = []
        
        # Регулярные выражения для извлечения информации о моделях
        self.patterns = {
            'model_class': r'class\s*(\w+)\s*\(\s*(?:.*?db\.Model\s*\))?:',
            'table_name': r'__tablename__\s*=\s*[\'"](\w+)[\'"]',
            'column_pattern': r'(\w+)\s*=\s*db\.Column\(\s*(.*?)\s*\)',
            'column_type': r'[A-Za-z]+\.(Integer|String|DateTime|Boolean|Float|Text)'
        }

    def extract_model_info(self, file_path):
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

    def generate_ddl(self):
        ddl_queries = []
        
        # Преобразование типв SQLAlchemy в SQL-типы
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
        


        # if output_path: 
        #     ddl_content = "\n\n".join(ddl_queries)
        #     with open(output_path, 'w', encoding='utf-8') as f:
        #         f.write(ddl_content)
        
        return ddl_queries
    

def create_ddl(project_paths):
    parser = SQLAlchemyModelParser()
    
    for file_path in project_paths:
        if file_path.endswith(".py"): 
            parser.extract_model_info(file_path)
    
    ddl_queries = parser.generate_ddl()
        
    return ddl_queries


def give_ddl_feedback(project_path): 
    ddl_queries = create_ddl(project_path)

    ddl_feedback = []
    query_prompt = Template("""
    convert the SQL DDL (data definition language) below in the set of sqlalchemy objects in Python:                            
    $ddl_query
    """)
    
    context = """
    assume that you are proficient Python coder. 
    You have string expertise in SQLAlchemy python library. 
    You can only code. Do not explain anything

    Yor task is also optimize these ddl queries as much as possible.
    To do so consider using more efficient data types, creating indicies on tables, 
    make partitioning for those tables, whos name can be related to heavliy loaded in terms of transactions.

    In your answeres use ` symbols to separate your comments from code 
    """

    for ddl_query in ddl_queries: 
        prompt = query_prompt.substitute(ddl_query=ddl_query)
        ddl_feedback.append(get_evrazgpt_response(prompt, context))

    return ddl_feedback
