from model_logging import check_patterns_logger
from string import Template
from datetime import datetime


def count_issues(pipeline_dict): 
    total_count = 0
    issue_lst = []
    for issue_name, issues in pipeline_dict.items():
        issue_count = len(issues)
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

def report_pipeline(project_files, project_name):

    logger_report = check_patterns_logger(project_files)

    pipeline_dict = {
        # "Ошибки в архитектуре": 
        "Ошибки логирования": logger_report
    }

    return get_summary_statistics(pipeline_dict, project_name)
