from string import Template
from datetime import datetime

from application.models.logging_model.model_logging import check_patterns_logger
from application.models.ddl_model.model_ddl_feedback import give_ddl_feedback
from application.models.pep_model.model_pep8 import check_patterns_pep
from application.models.hierarchy_model.hierarchy_model import check_hierarchy
from application.models.context_model.adapter_qa_model import adapter_qa_checks


def count_leaf_elements(data):
    if isinstance(data, (str, int, float, bool)):
        return 1
    
    if isinstance(data, dict):
        return sum(count_leaf_elements(value) for value in data.values())
    
    if isinstance(data, list):
        return sum(count_leaf_elements(item) for item in data)
    
    return 0


def count_issues(pipeline_dict): 
    total_count = 0
    issue_lst = []
    for issue_name, issues in pipeline_dict.items():
        issue_count = count_leaf_elements(issues)
        total_count += issue_count
        issue_lst.append(f"{issue_name} : {issue_count}")

    issue_string = ";\n".join(issue_lst)
    
    return issue_string, total_count
        

def get_summary_statistics(pipeline_dict, project_name):
    time_stamp = datetime.now()
    summary_string, total_issues = count_issues(pipeline_dict)
    summary_title = Template("Анализ проекта $project_name от $time_stamp UTC+3").substitute(
        project_name=project_name,
        time_stamp=time_stamp)
    summary_value = Template("""Дата последнего изменения проекта : $time_stamp UTC+3
Общее количество ошибок : $total_issues
$summary_string""").substitute(
    time_stamp=time_stamp, 
    total_issues=total_issues, 
    summary_string=summary_string)

    summary_analytics = {summary_title: summary_value}
    summary_analytics.update(pipeline_dict)

    return summary_analytics


def archive_report_pipeline(project_files, project_name, faker_split):

    logger_report = check_patterns_logger(project_files, project_name, faker_split)
    pep_report = check_patterns_pep(project_files, project_name, faker_split)
    arch_report = check_hierarchy(project_files)
    adapter_qa_report = adapter_qa_checks(project_files)
    # try:
    #     ddl_feedback = give_ddl_feedback(project_files)
    
    # except KeyError:
        # ddl_feedback = []

    pipeline_dict = {
        "Ошибки в архитектуре": arch_report,
        "Описание архитектуры на предмет наличия паттерна адаптера": adapter_qa_report,
        "Ошибки логирования": logger_report, 
        "Ошибки стандарта PEP":pep_report
        # "Рекомендации для DDL сущностей в СУБД": ddl_feedback
    }

    return get_summary_statistics(pipeline_dict, project_name)


def file_report_pipeline(project_files, project_name, faker_split):

    logger_report = check_patterns_logger(project_files, project_name, faker_split)
    pep_report = check_patterns_pep(project_files, project_name, faker_split)

    # try:
    #     ddl_feedback = give_ddl_feedback(project_files)
    
    # except KeyError:
        # ddl_feedback = []

    pipeline_dict = {
        "Ошибки логирования": logger_report, 
        "Ошибки стандарта PEP": pep_report
        # "Рекомендации для DDL сущностей в СУБД": ddl_feedback
    }

    return get_summary_statistics(pipeline_dict, project_name)
