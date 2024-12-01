from typing import List, AnyStr
from application.models.hierarchy_model.utils.utils import find_application_files, extract_imports


class HierarchyModel():
    def execute(self, project_structure: List[AnyStr]):
        issues = {}
        app_files = find_application_files(project_structure)

        for file in app_files:
            imports = extract_imports(file)
            for one_import in imports:
                if 'adapter/' in one_import:
                    issues['Вызов адаптера из слоя приложения'] = issues.get(['Вызов адаптера из слоя приложения'], [])
                    issues['Вызов адаптера из слоя приложения'].append(one_import)

        return issues
    

def check_hierarchy(project_files):

    model = HierarchyModel()

    return model.execute(project_files)
