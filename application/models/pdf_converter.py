import json
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import darkblue, navy
import re


class JSONtoPDFConverter:
    """
    Утилита для конвертации вложенного JSON в PDF-документ с поддержкой форматирования кода.
    
    Ключевые возможности:
    - Генерация PDF из вложенной JSON-структуры
    - Автоматическое создание заголовков из ключей JSON
    - Поддержка форматирования кода внутри значений
    """
    
    def __init__(self, output_path='output.pdf'):
        """
        Инициализация конвертера PDF.
        
        Args:
            output_path (str): Путь для сохранения PDF-файла
        """
        pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))

        self.output_path = output_path
        self.styles = getSampleStyleSheet()

        style_names = ['Normal', 'Title', 'Heading1', 'Heading2', 'Heading3']
        for name in style_names:
            if name in self.styles:
                self.styles[name].fontName = 'DejaVuSerif'
        
        # Создание пользовательского стиля для кода
        self.code_style = ParagraphStyle(
            'CodeStyle', 
            parent=self.styles['Normal'], 
            fontName='DejaVuSerif', 
            fontSize=9, 
            textColor=navy,
            backColor='lightgrey',
            borderColor=darkblue,
            borderWidth=0.5,
            borderPadding=6
        )

    def _parse_json_recursive(self, data, level=0):
        """
        Рекурсивный парсинг JSON-структуры для генерации элементов PDF.
        
        Args:
            data (dict/list/str): Входные данные для парсинга
            level (int): Уровень вложенности для форматирования
        
        Returns:
            list: Список элементов для PDF
        """
        content = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                # Добавление заголовка с отступом
                title_style = self.styles['Heading%d' % min(max(level+1, 1), 6)]
                content.append(Paragraph(str(key), title_style))
                
                # Рекурсивный парсинг значений
                if isinstance(value, (dict, list)):
                    content.extend(self._parse_json_recursive(value, level+1))
                else:
                    # Проверка на наличие кода
                    if '```' in str(value):
                        code_sections = str(value).split('```')
                        for idx, section in enumerate(code_sections):
                            if idx % 2 == 1:  # Нечетные секции - код
                                content.append(Paragraph(section, self.styles['CodeStyle']))
                            else:  # Четные секции - текст
                                content.append(Paragraph(section, self.styles['Normal']))
                    else:
                        content.append(Paragraph(str(value), self.styles['Normal']))
                
                content.append(Spacer(1, 12))
        
        elif isinstance(data, list):
            for item in data:
                content.extend(self._parse_json_recursive(item, level))
        
        return content

    def convert(self, json_data):
        """
        Конвертация JSON в PDF-документ.
        
        Args:
            json_data (str/dict): JSON-данные для конвертации
        """
        # Преобразование JSON, если передана строка
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        # Создание PDF-документа
        doc = SimpleDocTemplate(self.output_path, pagesize=A4)
        
        # Генерация контента
        content = self._parse_json_recursive(json_data)
        
        # Сборка и сохранение PDF
        doc.build(content)
        print(f"PDF создан: {self.output_path}")

# Пример использования
def example_usage():
    """Демонстрация использования конвертера JSON в PDF"""
    sample_json = {
        "Проект": "Конвертер JSON в PDF",
        "Описание": "Утилита для генерации PDF из JSON",
        "Код": {
            "Пример": "```python\ndef hello_world():\n    print('Привет, мир!')\n```"
        }
    }
    
    converter = JSONtoPDFConverter('json_to_pdf_example.pdf')
    converter.convert(sample_json)


def assemble_document(file_name, json_struct): 
    converter = JSONtoPDFConverter(file_name)
    converter.convert(json_struct)


# Пример использования
def main():
    """Демонстрация конвертации JSON в PDF."""
    sample_json = {
        "Проект": "Конвертер JSON в PDF",
        "Описание": "Поддержка кириллических символов",
        "Язык": "Русский",
        "Детали": {
            "Версия": "1.0",
            "Совместимость": "```Python 3.7+```"
        }
    }
    
    converter = JSONtoPDFConverter('cyrillic_pdf_example.pdf')
    converter.convert(sample_json)

example_usage()