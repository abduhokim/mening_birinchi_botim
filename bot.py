from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Tasodifiy anime"],
        ["Anime menyu", "Kod orqali qidirish", "AI qidiruv"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Xush kelibsiz! Quyidagi tugmalardan birini tanlang:", reply_markup=reply_markup)

# Tasodifiy anime tugmasi
import random
async def handle_random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    animelar = [
        "Naruto 🍥", "One Piece ☠️", "Attack on Titan 🛡️",
        "Jujutsu Kaisen 🔥", "Demon Slayer 🗡️", "Death Note 📓"
    ]
    tanlangan = random.choice(animelar)
    await update.message.reply_text(f"Tasodifiy anime: {tanlangan} #animeni_yuklab_olish_uchun_ssilka")

# Anime menyu tugmasi
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Anime menyu: (Hali ishlab chiqilmoqda)")

# Kod orqali qidirish tugmasi
async def handle_kod_qidir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Kod orqali qidiruv: Kod yuboring...")

# AI qidiruv tugmasi
async def handle_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 AI orqali qidiruv: Nima qidirmoqchisiz?")

# Asosiy ishga tushirish
def main():
    app = ApplicationBuilder().token("BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Tasodifiy anime$"), handle_random))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Anime menyu$"), handle_menu))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Kod orqali qidirish$"), handle_kod_qidir))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^AI qidiruv$"), handle_ai))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
