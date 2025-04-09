import logging
import os
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# .env faylini yuklash
load_dotenv()

# Tokenlar
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Log sozlamalari
logging.basicConfig(level=logging.INFO)

# Fallback tasodifiy so'zlar
random_keywords = [
    "anime aesthetic site:pinterest.com",
    "anime girl site:pinterest.com",
    "anime boy site:pinterest.com",
    "cool anime wallpaper site:pinterest.com",
    "anime background site:pinterest.com"
]

# Orqaga tugmasi
def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back")]])

# Boshlash
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎭 Anonim chat", callback_data="anonymous_chat")],
        [InlineKeyboardButton("🎲 Tasodifiy anime", callback_data="random_anime")],
        [InlineKeyboardButton("🔍 Anime izlash", callback_data="search")],
        [InlineKeyboardButton("🤖 AI qidiruv", callback_data="ai_search")],
        [InlineKeyboardButton("📢 Reklama & Homiylik", callback_data="advertising")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Salom! Quyidagilardan birini tanlang:", reply_markup=reply_markup)

# Crunchyroll saytidan anime qidirish
def search_crunchyroll(anime_name: str):
    search_url = f"https://www.crunchyroll.com/search?q={anime_name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='title')
        
        if results:
            first_result = results[0].find('a')
            title = first_result.text.strip()
            link = f"https://www.crunchyroll.com{first_result['href']}"
            image_url = soup.find('img', class_='lazyload')['data-src']
            return title, link, image_url
        else:
            return None, None, None
    return None, None, None

# Tugmalarni bosganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "anonymous_chat":
        await query.edit_message_text("Anonim chat hali tayyor emas.", reply_markup=back_button())

    elif query.data == "random_anime":
        await query.edit_message_text("Tasodifiy anime rasm.", reply_markup=back_button())
        random_image = random.choice(random_keywords)
        await query.message.reply_text(f"Mana tasodifiy anime: {random_image}", reply_markup=back_button())
        
    elif query.data == "search":
        await query.edit_message_text("Iltimos, anime nomini kiriting:")

    elif query.data == "ai_search":
        await query.edit_message_text("AI qidiruv hozircha yoqilmagan.", reply_markup=back_button())

    elif query.data == "advertising":
        await query.edit_message_text("📢 Reklama va hamkorlik uchun @username ga yozing.", reply_markup=back_button())

    elif query.data == "back":
        await query.edit_message_text(text="Asosiy menyuga qaytdingiz!", reply_markup=None)
        await start(update, context)

    else:
        await query.edit_message_text("Hozircha mavjud emas.", reply_markup=back_button())

# Anime haqida ma'lumot izlash
async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    anime_name = update.message.text
    title, link, image_url = search_crunchyroll(anime_name)
    
    if title:
        await update.message.reply_text(f"Anime nomi: {title}\nLink: {link}", reply_markup=back_button())
        await update.message.reply_photo(photo=image_url, caption=f"Mana, {title} ning rasmi:", reply_markup=back_button())
    else:
        await update.message.reply_text("Aniq ma'lumot topilmadi.", reply_markup=back_button())

# Ishga tushirish
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_anime))
    app.run_polling()

if __name__ == "__main__":
    main()
