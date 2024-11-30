from decouple import config
from telebot import TeleBot
from controllers.BotController import process_archive, process_file

# Загрузка конфигурации из .env файла
TOKEN = config('TELEGRAM_TOKEN')

# Создание бота и обработка сообщений
bot = TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    message.document.file_name

    # try: 
    if message.document.file_name.endswith('.zip'):
        result_report = process_archive(downloaded_file, chat_id)
        r_type = "архив"
    else:    
        result_report = process_file(downloaded_file, chat_id, message.document.file_name)
        r_type = "файл"

    bot.reply_to(message, f"Ваш {r_type} был обработан, результаты прикреплены к сообщению.")


    with open(result_report, "rb") as report_file:
        bot.send_document(chat_id=message.chat.id, document=report_file)
    
    # except NotImplementedError: 
    #     bot.reply_to(message, f"К сожалению, что-то пошло не так при обработке файла/архива. Убедитесь, что на вход подается корректный архив или отдельный .py файл")

    # except AssertionError: 
    #     bot.reply_to(message, f"К сожалению, что-то пошло не так при обработке файла/архива")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для проверки проектов. Отправьте мне файл или архив для обработки.")


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Я не знаю, что делать с этим. Пожалуйста, отправьте мне файл или архив для обработки.")

if __name__ == '__main__':
    print("Bot started")
    bot.infinity_polling()
