# from controllers import LL
from typing import List, Tuple, AnyStr


class DescriptionModel:
    def __init__(self, llm):
        self.llm = llm

    def execute(self, file_contexts):
        promt = self.collect_project_context(self.llm, file_contexts)
        response = self.get_response((promt))

    def collect_project_context(self, file_contexts: List[Tuple[AnyStr, AnyStr]]):
        promt = "Существует проект в котором присутствуют следующие модули:\n\n"

        for file_context in file_contexts:
            for f_name, f_context in file_context:
                promt = promt + f"{f_name}:\n{f_context}\n"

        promt = promt + '\n, классифицируй каждый файл по ему архитектурному предназначению: Адаптер, Бизнес логика, Иное'

        return promt

    def get_response(self, promt: str) -> str:
        """Реквест запрос к LLM модели
        """
        return self.llm(promt)
