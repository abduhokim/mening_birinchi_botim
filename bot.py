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
        [InlineKeyboardButton("Anonim chat", callback_data='anonymous_chat')],
        [InlineKeyboardButton("Tasodifiy anime", callback_data='random_anime')],
        [InlineKeyboardButton("Anime izlash", callback_data='search')],
        [InlineKeyboardButton("AI qidiruv", callback_data='ai_search')],
        [InlineKeyboardButton("Reklama & Homiylik", callback_data='advertising')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Salom! Iltimos, biror tugmani tanlang:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'anonymous_chat':
        await query.edit_message_text(text="Anonim chat funksiyasi hozirda ishlab chiqilmoqda." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    elif query.data == 'random_anime':
        anime_data = await get_random_anime()
        if anime_data:
            image_url = anime_data.get('image_url')
            anime_title = anime_data.get('title')
            anime_description = anime_data.get('description')
            await query.edit_message_text(text=f"Mana sizga tasodifiy anime: {anime_title}\n\n{anime_description}" + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
            await query.message.reply_photo(photo=image_url)
        else:
            await query.edit_message_text(text='Rasm olishda xatolik yuz berdi.' + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    elif query.data == 'search':
        await query.edit_message_text(text="Iltimos, qidirayotgan anime nomini kiriting:")
    elif query.data == 'ai_search':
        await query.edit_message_text(text="AI qidiruv funksiyasi hozirda ishlab chiqilmoqda." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    elif query.data == 'advertising':
        await query.edit_message_text(text="Reklama va homiylik haqida ma'lumot: ...\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    elif query.data == 'back':
        await start(update, context)
    else:
        await query.edit_message_text(text="Hozirda ishlab chiqilmoqda." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Orqaga", callback_data='back')]])

async def get_random_anime() -> dict:
    # Tasodifiy anime olish uchun API manzilini qo'shing
    response = requests.get('https://api.example.com/random-anime')  # O'zingizning anime API manzilingizni qo'shing
    if response.status_code == 200:
        return response.json()
    return None

async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    anime_name = update.message.text
    # Anime qidirish uchun API so'rovini yuboring
    response = requests.get(f'https://api.example.com/search-anime?name={anime_name}')  # O'zingizning qidiruv API manzilingizni qo'shing
    if response.status_code == 200:
        anime_data = response.json()
        if anime_data:
            # Anime ma'lumotlarini ko'rsatish
            await update.message.reply_text(f"Qidirilgan anime: {anime_data['title']}\nQismlar soni: {anime_data['episodes']}\nIshlab chiqaruvchi: {anime_data['studio']}\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
        else:
            await update.message.reply_text("Qidirilgan anime topilmadi." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    else:
        await update.message.reply_text("Qidiruvda xatolik yuz berdi." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_anime))  # Foydalanuvchi matn kiritganda qidiruv funksiyasini chaqirish

    application.run_polling()

if __name__ == '__main__':
    main()
