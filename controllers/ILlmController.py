from abc import ABC, abstractmethod


class ILlmController(ABC):
    @abstractmethod
    def get_result(self, request_promt: str):
        """По промту возвращает тестовый ответ
        """
        ...


class