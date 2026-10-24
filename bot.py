import os
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackQueryHandler
)
from datetime import datetime
import random

load_dotenv('.env')

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context):
    button_hi = KeyboardButton('Привет')
    button_how = KeyboardButton('Как дела?')
    button_help = KeyboardButton('Помощь')

    keyboard = [[button_hi, button_how], [button_help]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Привет! Я твой телеграм-бот. Как могу помочь?', reply_markup=reply_markup)

async def help_command(update: Update, context):
    await update.message.reply_text(
        'Команды: \n/start - начать\n/help - помощь\n/about - обо мне\n/menu - меню с интерасктивными кнопочками'
    )

async def about(update: Update, context):
    await update.message.reply_text(
        'Я учебный бот на python-telegram-bot v21.'
    )

async def handle_text(update: Update, context):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()

    if 'привет' in text:
        await update.message.reply_text('Привет! Как твои дела?')
    elif 'как дела' in text:
        await update.message.reply_text('У меня всё отлично, спасибо!')
    elif 'пока' in text:
        await update.message.reply_text('До встречи! Хорошего дня!')
    elif 'помощь' in text:
        await update.message.reply_text('Если нужна помощь напишите /help')
    else:
        await update.message.reply_text('Извините, я вас не понимаю. Попробуйте команду /menu')

async def menu(update: Update, context):
    button_time = InlineKeyboardButton('Дата и время', callback_data='time')
    button_fact = InlineKeyboardButton('Случайный факт', callback_data='fact')
    button_site = InlineKeyboardButton('Открыть сайт', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    
    keyboard = [
        [button_time, button_site],
        [button_fact]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'time':
        now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        await query.edit_message_text(f'Текущее время: {now}')
    elif query.data == 'fact':
        facts = ['Коты спят до 16 часов в сутки.', 'Банан - это ягода, а не фрукт.', 'Скорость улитки около 0.05 км/ч.']
        await query.edit_message_text(f'Случайный факт: {random.choice(facts)}')

async def send_photo(update, context):
    url = 'https://webcalypt.cloud/tools/meme-generator/104651'
    await update.message.reply_photo(url, caption='Шок контент')

async def send_sticker(update, context):
    sticker_id = 'CAACAgIAAxkBAAEX6PRq0zpe7S1ba9xttouPZ9LJSovjfAACC5gAAjn_aUnL2SmeV0TtVj0E'
    await update.message.reply_sticker(sticker_id)

async def send_gif(update, context):
    url = 'https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif'
    await update.message.reply_animation(url, caption='это ты')

if __name__ == '__main__':
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about))
    app.add_handler(CommandHandler('menu', menu))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(CommandHandler('photo', send_photo))
    app.add_handler(CommandHandler('sticker', send_sticker))
    app.add_handler(CommandHandler('gif', send_gif))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
