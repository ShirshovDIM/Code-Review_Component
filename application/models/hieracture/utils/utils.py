def find_application_files(file_paths):
    """Возвращает файл, если он лежит в папке applications
    """
    return [path for path in file_paths if ('application/' in path) and (path[-3:] == '.py')]


def extract_imports(file_path):
    """Извлекает все конструкции `import` из файлa.

    Args:
        file_paths (list): Путь к файлу.

    Returns:
        list: Список строк, содержащих конструкции `import`.
    """

    imports = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip().startswith('import'):
                imports.append(line.strip())
    return imports
