import logging
import os
import random
import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Load .env
load_dotenv()

# Tokenlar
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Log
logging.basicConfig(level=logging.INFO)

# Fallback tasodifiy so‘zlar (pinterest uchun)
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

# Tugma bosilganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "anonymous_chat":
        await query.edit_message_text("Anonim chat hali tayyor emas.", reply_markup=back_button())

    elif query.data == "random_anime":
        keyword = random.choice(random_keywords)
        url = f"https://www.googleapis.com/customsearch/v1?q={keyword}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}&searchType=image"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                image_url = data["items"][0]["link"]
                await query.edit_message_text("Mana sizga tasodifiy anime rasm 👇", reply_markup=back_button())
                await query.message.reply_photo(photo=image_url)
            else:
                await query.edit_message_text("Rasm topilmadi.", reply_markup=back_button())
        else:
            await query.edit_message_text("Xatolik yuz berdi.", reply_markup=back_button())

    elif query.data == "search":
        await query.edit_message_text("Iltimos, anime nomini kiriting (faqat matn):")

    elif query.data == "ai_search":
        await query.edit_message_text("AI qidiruv hozircha yoqilmagan.", reply_markup=back_button())

    elif query.data == "advertising":
        await query.edit_message_text("📢 Reklama va hamkorlik uchun @username ga yozing.", reply_markup=back_button())

    elif query.data == "back":
        await start(query, context)

    else:
        await query.edit_message_text("Hozircha mavjud emas.", reply_markup=back_button())

# Matn kiritsagina rasm qidirish
async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    anime_name = update.message.text
    query = f"{anime_name} site:pinterest.com"

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}&searchType=image"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            image_url = data["items"][0]["link"]
            await update.message.reply_photo(photo=image_url, caption=f"🔍 Qidiruv natijasi: {anime_name}", reply_markup=back_button())
        else:
            await update.message.reply_text("Rasm topilmadi.", reply_markup=back_button())
    else:
        await update.message.reply_text("Google API xatolik berdi.", reply_markup=back_button())

# Ishga tushirish
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_anime))
    app.run_polling()

if __name__ == "__main__":
    main()
