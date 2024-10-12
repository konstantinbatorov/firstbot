import os
from telegram import Update #Для обновлений Телеграмма
from telegram.ext import Application, CommandHandler #Классы для обработки бота
from dotenv import load_dotenv #Загрузка файла с токеном

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 

app = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text('Добро пожаловать!')

async def help_command(update: Update, context):
    await update.message.reply_text('Команды для использования:\n /help - Помощь\n/start - Начать работу')


app.add_handler(CommandHandler('start',start))
app.add_handler(CommandHandler('help', help_command))


if __name__ == '__main__':
    print('Бот запущен и готов к работе!')
    app.run_polling()
