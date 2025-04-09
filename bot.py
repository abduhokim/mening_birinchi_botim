import logging
import requests
import os
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Load environment variables
load_dotenv()

# Get bot token and Google API credentials
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Random anime image URLs (for fallback)
anime_images = [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg",
]

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
        random_image = random.choice(anime_images)
        await query.edit_message_text(text="Mana sizga tasodifiy anime rasm:" + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
        await query.message.reply_photo(photo=random_image)
    elif query.data == 'search':
        await query.edit_message_text(text="Iltimos, qidirayotgan anime nomini kiriting:")
    elif query.data == 'ai_search':
        await query.edit_message_text(text="AI qidiruv funksiyasi hozirda ishlab chiqilmoqda." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    elif query.data == 'advertising':
        await query.edit_message_text(text="Reklama va homiylik haqida ma'lumot: ...\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    elif query.data == 'back':
        await start(update, context)  # Call start function to return to main menu
    else:
        await query.edit_message_text(text="Hozirda ishlab chiqilmoqda." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Orqaga", callback_data='back')]])

async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    anime_name = update.message.text
    # Use Google Custom Search API to find images
    url = f"https://www.googleapis.com/customsearch/v1?q={anime_name}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}&searchType=image"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        search_results = response.json()
        if 'items' in search_results and len(search_results['items']) > 0:
            # Get the first image URL from the search results
            image_url = search_results['items'][0]['link']
            await update.message.reply_photo(photo=image_url, caption=f"Qidirilgan anime: {anime_name}\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
        else:
            await update.message.reply_text("Qidirilgan anime topilmadi." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())
    else:
        await update.message.reply_text("Qidiruvda xatolik yuz berdi." + "\n\nOrqaga qaytish uchun tugmani bosing:", reply_markup=back_button())

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_anime))

    application.run_polling()

if __name__ == '__main__':
    main()
