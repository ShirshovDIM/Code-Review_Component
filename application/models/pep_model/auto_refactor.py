import os
import json
from yapf.yapflib.yapf_api import FormatCode
import nbformat
import autopep8

## TODO: автоматическая конвертация кода
def format_python_script(file_path: str, verbose: bool = True):
    """Форматирует Python файл с помощью YAPF."""
    with open(file_path, 'r', encoding='utf-8') as f:
        original_code = f.read()
    formatted_code, _ = FormatCode(original_code, )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_code)
    if verbose:
        print(f"Файл {file_path} успешно отформатирован.")


def format_notebook(file_path: str, verbose: bool = True):
    """Форматирует кодовые ячейки в Jupyter Notebook с помощью YAPF."""
    with open(file_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    for cell in notebook.cells:
        if cell.cell_type == 'code':  # Форматируем только кодовые ячейки
            original_code = cell.source
            if original_code.strip():  # Если ячейка не пустая
                formatted_code, _ = FormatCode(original_code)
                cell.source = formatted_code

    with open(file_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)
    if verbose:
        print(f"Файл {file_path} успешно отформатирован.")


def format_repository(directory, exclude_dirs=None):
    """
    Форматирует все Python-файлы в указанной директории и её поддиректориях,
    исключая файлы в заданных директориях.

    Args:
        directory (str): Путь к директории с файлами.
        exclude_dirs (list[str]): Список путей, которые нужно исключить.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    ignored_files = []

    for root, dirs, files in os.walk(directory):
        # Исключение директорий
        dirs[:] = [
            d for d in dirs if os.path.join(root, d) not in exclude_dirs
        ]

        for file in files:
            if file.endswith(".py") or file.endswith(".ipynb"):
                file_path = os.path.join(root, file)

                # Исключение файлов, содержащих .git или .ipynb_checkpoints в пути
                if ".git" in file_path or ".ipynb_checkpoints" in file_path:
                    ignored_files.append(file_path)
                    continue

                if file.endswith('.py'):
                    try:
                        format_python_script(file_path, verbose=False)
                        print(f"Файл {file_path} успешно отформатирован.")

                    except SyntaxError:
                        print(f"Ошибка синтаксиса в файле: {file_path}")
                        try:
                            with open(file_path, 'r') as f:
                                file_content = f.read()

                            # Исправляем синтаксические ошибки с помощью autopep8
                            fixed_content = autopep8.fix_code(file_content)

                            # Перезаписываем файл с исправленным кодом
                            with open(file_path, 'w') as f:
                                f.write(fixed_content)

                            # Пытаемся снова отформатировать файл с помощью yapf
                            format_python_script(file_path, verbose=False)
                            print(
                                f"Синтаксическая ошибка исправлена, файл {file_path} отформатирован."
                            )
                        except Exception as e:
                            print(
                                f"Не удалось исправить синтаксическую ошибку в файле {file_path}: {e}"
                            )

                    except Exception as e:
                        print(f"Ошибка при форматировании {file_path}: {e}")

                elif file.endswith('.ipynb'):
                    try:
                        format_notebook(file_path, verbose=False)
                        print(f"Файл {file_path} успешно отформатирован.")

                    except SyntaxError:
                        print(f"Ошибка синтаксиса в файле: {file_path}")
                        try:
                            with open(file_path, 'r') as f:
                                notebook = json.load(f)
                            # Пройдем по всем ячейкам, ищем кодовые ячейки
                            for cell in notebook['cells']:
                                if cell['cell_type'] == 'code':
                                    # Получаем исходный код из ячейки
                                    code = ''.join(cell['source'])

                                    # Используем autopep8 для исправления кода
                                    formatted_code = autopep8.fix_code(code)

                                    # Записываем отформатированный код обратно в ячейку
                                    cell['source'] = formatted_code.splitlines(
                                        keepends=True)

                            with open(file_path, 'w') as f:
                                json.dump(notebook, f, indent=2)

                            # Пытаемся снова отформатировать файл с помощью yapf
                            format_notebook(file_path, verbose=False)
                            print(
                                f"Синтаксическая ошибка исправлена, файл {file_path} отформатирован."
                            )

                        except Exception as e:
                            print(
                                f"Не удалось исправить синтаксическую ошибку в файле {file_path}: {e}"
                            )

                    except Exception as e:
                        print(f"Ошибка при форматировании {file_path}: {e}")
    print('___Пропущенные файлы___')
    print(*ignored_files, sep='\n')


if __name__ == "__main__":
    repo_path = '/Users/arsen/Documents/huck/'  #input("Enter the path to the repository: ")#.strip()
    if os.path.isdir(repo_path):
        format_repository(repo_path)
        print("Formatting complete!")
    else:
        print(repo_path)
        print("Invalid repository path!")
