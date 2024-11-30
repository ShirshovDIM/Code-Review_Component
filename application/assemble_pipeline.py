from application.models.model_logging import check_patterns_logger


def get_summary_statistics():
    pass


def report_pipeline(project_files):

    logger_report = check_patterns_logger(project_files)

    pipeline_dict = {
        "Отчет по логированию": logger_report
    }
    print(logger_report)

    return pipeline_dict
