import os
from telegram import (
    Update,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler) #Классы для обработки бота
from dotenv import load_dotenv #Загрузка файла с токеном

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 

app = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    button_info = KeyboardButton('❗ Информация')
    button_contacts = KeyboardButton('☎ Контакты')
    button_help = KeyboardButton('Помощь')
    keyboard = [[button_info], [button_contacts, button_help]]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text('Добро пожаловать!', reply_markup=reply_markup)


async def help_command(update: Update, context):
    await update.message.reply_text('Команды для использования:\n /help - Помощь\n/start - Начать работу')


async def handler_message(update: Update, context):
    text = update.message.text

    if text == '❗ Информация':
        await update.message.reply_text('от')
    elif text == '☎ Контакты':
        await update.message.reply_text('контакты сюда')
    elif text == 'Помощь':
        await help_command(update, context)
    else:
        await update.message.reply_text('Такой команды нет!')

async def contacts(update: Update, context):
    button_link = InlineKeyboardButton('Сайт', url='https://sh47-ulan-ude-r81.gosweb.gosuslugi.ru/')
    button_phone = InlineKeyboardButton('Телефоны', callback_data='phones')
    button_email = InlineKeyboardButton('Электронная почта', callback_data='emails')
    button_adress = InlineKeyboardButton('Адрес', callback_data='adress')

    keyboard = [[button_link], [button_phone, button_email], [button_adress]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('**Контакты**', reply_markup=reply_markup) #TODO parse mode

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'phones':
        await query.edit_message_text('8 (3012) 45-02-32, 8 (3012) 55-63-23')
    elif query.data == 'emails':
        await query.edit_message_text('school_47@govrb.ru')
    elif query.data == 'adress':
        await update.message.reply_text('670042, Республика Бурятия, г.Улан-Удэ, ул.Калашникова,12')
    else:
        await query.edit_message_text('Неизвестная команда')
    
app.add_handler(CommandHandler('contacts', contacts))



app.add_handler(CommandHandler('start',start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_message))


if __name__ == '__main__':
    print('Бот запущен и готов к работе!')
    app.run_polling()
