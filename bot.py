import os
from telegram.ext import Updater, CommandHandler #Классы для обработки бота
from telegram import Update #Для обновлений Телеграмма
from telegram.ext import CallbackContext #Для передачи контекста между разработчиками
from dotenv import load_dotenv #Загрузка файла с токеном

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 
# print(TOKEN)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я Telegram-бот!')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Я могу выполнять следующие команды: \n/start - начать общение \n/help - список команд')


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)

if __name__ == '__main__':
    updater.start_polling()
    print('Бот активирован!')
    updater.idle()