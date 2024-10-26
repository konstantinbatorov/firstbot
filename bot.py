import os
from telegram import (
    Update,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto)

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

async def info(update: Update, context):
    media = [
        InputMediaPhoto(open('./Files/history.jpg', 'rb')),
        InputMediaPhoto(open('./Files/director.jpg', 'rb'))
    ]
    caption_info = '23 января 1988 года в газете "Правда Бурятии" появилась статья с объявлением о конкурсном наборе комсомльско- молодежного педагогического коллектива в школу- новостройку. Молодые учителя прошли несколько профессиональных испытаний. с и 1 сентября 1988 года школа №47 распахнула свои двери для своих первых учеников. \nЗа четверть века в школе сменилось несколько руководителей, десятки учителей, тысячи детей. В разные годы коллектив возгвляли директора С.С. Перелыгин, Ж.Б. Сультимова, О.А. Бильдушкин, Т.И. Матхеева. С 2008 года коллективом школы №47 руководит Тамара Мункуевна Трофимова.'
    await context.bot.send_media_group(chat_id = update.effective_chat.id, media=media, caption =caption_info)
    #await update.message.reply_photo(photo=photo_url, caption = caption_info)



async def handler_message(update: Update, context):
    text = update.message.text
    print(text)

    if text == '❗ Информация':
        await info(update, context)
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

    await update.message.reply_text('<b>Контакты</b>', reply_markup=reply_markup, parse_mode='HTML') #do

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'phones':
        await query.edit_message_text('8 (3012) 45-02-32, 8 (3012) 55-63-23')
    elif query.data == 'emails':
        await query.edit_message_text('school_47@govrb.ru')
    elif query.data == 'adress':
        await query.edit_message_text('670042, Республика Бурятия, г.Улан-Удэ, ул.Калашникова,12')
    else:
        await query.edit_message_text('Неизвестная команда')
    
app.add_handler(CommandHandler('contacts', contacts))

app.add_handler(CommandHandler('info', info))

app.add_handler(CommandHandler('start',start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_message))
app.add_handler(CallbackQueryHandler(button_callback))


if __name__ == '__main__':
    print('Бот запущен и готов к работе!')
    app.run_polling()
