from typing import List, AnyStr
from utils.utils import find_application_files, extract_imports


class HieractureModel():
    def execute(self, project_structure: List[AnyStr]):
        issues = {''}
        app_files = find_application_files(project_structure)

        for file in app_files:
            imports = extract_imports(file)
            for one_improt in imports:
                if 'adapter/' in one_improt:
                    issues['Вызов адаптера из слоя приложения'] = issues.get(['Вызов адаптера из слоя приложения'], [])
                    issues['Вызов адаптера из слоя приложения'].append(one_improt)

        return issues
