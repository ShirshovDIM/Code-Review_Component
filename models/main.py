import io
from zipfile import ZipFile
from glob import glob
from decouple import config
from telebot import TeleBot
import os
import shutil

from assemble_pipeline import report_pipeline
from pdf_converter import assemble_document

# Загрузка конфигурации из .env файла
TOKEN = config('TELEGRAM_TOKEN')


# Функция для обработки файлов и создания репортов
def process_file(file) -> str:
    # Здесь должна быть логика обработки файла
    print("Processing file:", file)
    report = assemble_document("report.pdf", {"Respond":"Hello world"})
    return report


# Функция для обработки архивов
def process_archive(zip_file, dir):
    with ZipFile(io.BytesIO(zip_file), 'r') as archive:
        tmp_path = f"{os.getcwd()}\\data\\{dir}"
        archive.extractall(tmp_path)
        project_files = glob(f"{tmp_path}\\**", recursive=True)
        project_name = glob(f"{tmp_path}\\*")[0].split("\\")[-1]
        print(project_name)
        report_dict = report_pipeline(project_files, project_name)
        shutil.rmtree(f"{tmp_path}\\{project_name}")
    
    file_dir = f"{tmp_path}\\{project_name}_report.pdf"
    assemble_document(file_dir, report_dict)
    return file_dir


# Создание бота и обработка сообщений
bot = TeleBot(TOKEN)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    if message.document.file_name.endswith('.zip'):
        result_report = process_archive(downloaded_file, chat_id)
        print(result_report)
        r_type = "архив"
    else:
        result_report = process_file(downloaded_file)
        r_type = "файл"

    bot.reply_to(message, f"Ваш {r_type} был обработан, результаты прикреплены к сообщению.")
    with open(result_report, "rb") as report_file:
        bot.send_document(chat_id=message.chat.id, document=report_file)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для проверки проектов. Отправьте мне файл или архив для обработки.")


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не знаю, что делать с этим. Пожалуйста, отправьте мне файл или архив для обработки.")


if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()
