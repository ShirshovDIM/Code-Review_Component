import ast
import re


class PEP8Checker:
    
    def __init__(self):
        self.violations = []

    
    def check_all_standards(self, file_path, dummy_file_path):

        with open(file_path, 'r', encoding='utf-8') as file:
            self.source_code = file.read()
            self.lines = self.source_code.splitlines()

        self.check_line_length(dummy_file_path)
        self.check_imports(dummy_file_path)
        self.check_whitespace(dummy_file_path)
        self.check_naming_conventions(dummy_file_path)
        self.check_comments(dummy_file_path)
        # self.check_complexity(dummy_file_path)
        
        return self.violations
    
    def check_line_length(self, file_path):
        for i, line in enumerate(self.lines, 1):
            if len(line.rstrip()) > 79:
                self.violations.append({f"{file_path}:\nСтрока {i}: Превышена максимальная длина (>79 символов)": 
                                        f"``` | {i} -> {line}```"})
    
    def check_imports(self, file_path):
        """Анализируем импорты"""
        import_pattern = re.compile(r'^import\s+|^from\s+')
        imports = [line for line in self.lines if import_pattern.match(line.strip())]
        
        if imports:
            # Проверка сортировки и группировки импортов
            if not all(imp.startswith('import') or imp.startswith('from') for ind, imp in enumerate(imports)):
                self.violations.append({f"{file_path}:\nНарушен порядок импортов", 
                                        f"```{'\n'.join(imports)}```"})
    
    def check_whitespace(self, file_path):
        for i, line in enumerate(self.lines, 1):
            # Проверка на лишние пробелы в конце строк
            if line.rstrip() != line:
                self.violations.append({f"{file_path}:\nСтрока {i}: Лишние пробелы в конце строки": 
                                        f"``` | {i} -> {line}```"})
            
            # Проверка на смешивание отступов
            if '\t' in line:
                self.violations.append({f"{file_path}\nСтрока {i}: Использование табуляции вместо пробелов": 
                                        f"``` | {i} -> {line}```"})
    
    def check_naming_conventions(self, file_path):
        """Проверка нейминг конвеншена"""
        def validate_name(name, pattern):
            return re.match(pattern, name) is not None
        
        # Compile regex patterns for different naming conventions
        snake_case = r'^[a-z_][a-z0-9_]*$'
        pascal_case = r'^[A-Z][a-zA-Z0-9]*$'
        screaming_snake_case = r'^[A-Z_][A-Z0-9_]*$'
        
        try:
            tree = ast.parse(self.source_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if not validate_name(node.name, pascal_case):
                        self.violations.append({f"{file_path}:\nКласс {node.name}: Некорректное именование": 
                                                node.name})
                
                elif isinstance(node, ast.FunctionDef):
                    if not validate_name(node.name, snake_case):
                        self.violations.append({f"{file_path}:\nФункция {node.name}: Некорректное именование": 
                                                node.name})
                
                elif isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        if not validate_name(node.id, snake_case):
                            self.violations.append({f"{file_path}:\nПеременная {node.id}: Некорректное именование": 
                                                    node.id})
        except SyntaxError:
            self.violations.append({f"{file_path}:\nСинтаксическая ошибка при анализе именований": 
                                    "```code definition error```"})
    
    def check_comments(self, file_path):
        for i, line in enumerate(self.lines, 1):
            # Проверка количества символов в комментарии
            if '#' in line:
                comment = line.split('#')[1].strip()
                if len(comment) > 72:
                    self.violations.append({f"{file_path}:\nСтрока {i}: Слишком длинный комментарий": 
                                            f"```{comment}```"})
    
    def check_complexity(self, file_path):
        tree = ast.parse(self.source_code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Цикломатическая сложность
                complexity = sum(
                    1 for n in ast.walk(node) 
                    if isinstance(n, (ast.If, ast.While, ast.For, ast.And, ast.Or))
                )
                if complexity > 10:
                    self.violations.append({f"{file_path}:\nФункция {node.name}: Высокая цикломатическая сложность",
                                            f"```{node.name}```"})


def check_patterns_pep(project_files, project_name, faker_split): 

    parser = PEP8Checker()

    for file_path in project_files:
        dummy_file_path = f"./path/to/{project_name}/{file_path.split(faker_split)[-1]
                                                      .replace("\\\\", "/")
                                                      .replace("\\", "/")}"

        if file_path.endswith('.py'):
            parser.check_all_standards(file_path, dummy_file_path)

    return parser.violations

# Пример использования
# if __name__ == '__main__':
#     file_path = 'C:\\Users\\dbezu\\Desktop\\EVRAZ_ProtoSpace_Python\\application\\models\\pep_model\\auto_refactor.py'  # Путь к файлу для проверки

#     print(check_patterns_pep([file_path]))
    