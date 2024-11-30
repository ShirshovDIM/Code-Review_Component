import re
import json
from string import Template

def check_patterns_logger(project_files, return_json=False): 
    patterns = {
        'print_statements': re.compile(r'^\s*print\(', re.MULTILINE),
        'logging_imports': re.compile(r'^\s*import logging', re.MULTILINE),
        'basic_config_usage': re.compile(r'logging\.basicConfig\(', re.MULTILINE),
        'non_lazy_logging': re.compile(r'\.(debug|info|warning|error|critical)\(\s*f[\'"].*?[\'"]\s*\)', re.MULTILINE),
        'json_logger_usage': re.compile(r'python-json-logger', re.MULTILINE),
        'logger_creation': re.compile(r'logging\.getLogger\((.*?)\)', re.MULTILINE)
    }

    issues = {
        'print_statements': [],
        'logging_imports': [],
        'basic_config_usage': [],
        'non_lazy_logging': [],
        'json_logger_usage': [],
        'global_loggers': [],
        'scoped_loggers': []
    }

    for file_path in project_files:
        if file_path.endswith('.py'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            lines = content.splitlines()
            line_starts = [0] + [m.end() for m in re.finditer(r'\n', content)]
            
            def get_line_number(pos):
                """Calculate line number based on position in content."""
                for i, start in enumerate(line_starts):
                    if start > pos:
                        return i
                return len(line_starts)

            for key, pattern in patterns.items():
                if key == 'logger_creation':
                    continue

                for match in pattern.finditer(content):
                    line_number = get_line_number(match.start())
                    line_content = lines[line_number - 1].strip()
                    issues[key].append({
                        "Расположение файла в дереве проекта":file_path, 
                        "Номер -> Строка": Template("```$line_num -> line_content```")\
                        .substitute(line_num=str(line_number), line_content=line_content)
                        })
            

            for match in patterns['logger_creation'].finditer(content):
                logger_name = match.group(1).strip()
                line_number = get_line_number(match.start())
                line_content = lines[line_number - 1].strip()

                is_global = True
                for line in lines[:line_number - 1][::-1]:
                    if re.match(r'^\s*class\s+|^\s*def\s+', line):
                        is_global = False
                        break

                target_key = 'global_loggers' if is_global else 'scoped_loggers'
                issues[target_key].append((file_path, line_number, logger_name))

    if return_json: 
        with open('logging_issues.json', 'w') as file:
            json.dump(issues, file, indent=4)

    return issues
