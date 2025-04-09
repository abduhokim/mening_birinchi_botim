import logging
import requests
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# .env faylini yuklash
load_dotenv()

# Bot tokenini olish
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Anime izlash", callback_data='search')],
        [InlineKeyboardButton("Tasodifiy anime", callback_data='random')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Salom! Iltimos, biror tugmani tanlang:', reply_markup=reply_markup)

async def get_random_anime() -> dict:
    response = requests.get('https://api.example.com/random-anime')  # O'zingizning anime API manzilingizni qo'shing
    if response.status_code == 200:
        return response.json()
    return None

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'random':
        anime_data = await get_random_anime()
        if anime_data:
            image_url = anime_data.get('image_url')
            anime_title = anime_data.get('title')
            anime_description = anime_data.get('description')
            await query.edit_message_text(text=f"Mana sizga tasodifiy anime rasm: {anime_title}\n\n{anime_description}", reply_markup=None)
            await query.message.reply_photo(photo=image_url)
        else:
            await query.edit_message_text(text='Rasm olishda xatolik yuz berdi.')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
