import asyncio
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7670469438:AAH17F1_Ztumqea7TSQ8qsSmtLtLzjjNwO8"

# Anonim chat uchun
waiting_users = []
active_chats = {}

# Tasodifiy anime
animes = [
    {"name": "Jujutsu Kaisen", "episodes": 48, "movie": 1},
    {"name": "Attack on Titan", "episodes": 87, "movie": 0},
    {"name": "Demon Slayer", "episodes": 55, "movie": 1},
    {"name": "One Piece", "episodes": 1000, "movie": 15},
]

def menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🌸 Tasodifiy Anime 🌸")],
        [KeyboardButton("🎌 Anime menyu"), KeyboardButton("🔍 Kod orqali qidirish")],
        [KeyboardButton("🤖 AI yordamchi"), KeyboardButton("👥 Anonim Chat")],
        [KeyboardButton("❌ Suhbatni to‘xtatish")],
    ], resize_keyboard=True)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalomu alaykum! Xush kelibsiz!", reply_markup=menu_keyboard())

# Tasodifiy anime
async def random_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    anime = random.choice(animes)
    text = f"""✨ <b>Anime nomi:</b> <i>{anime['name']}</i>
🎬 <b>Qismlar soni:</b> <i>{anime['episodes']}</i>
🎥 <b>Filmlar:</b> <i>{anime['movie']}</i>"""
    await update.message.reply_sticker("CAACAgUAAxkBAAEBV1ZlYr9FWEFg1x3c0DkZAAGHt1EnXM8AAkcFAAIBjcpVxz6TXRxdcGsqBA")
    await update.message.reply_html(text)

# Kod orqali qidirish
async def search_by_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Kod kiriting:")

# AI yordamchi (mock)
async def ai_helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Menga savol bering, yordam beraman!")

# Anonim chatga ulanish
async def anonymous_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_chats:
        await update.message.reply_text("❗Siz allaqachon chatdasiz.")
        return

    if waiting_users and waiting_users[0] != user_id:
        partner_id = waiting_users.pop(0)
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id
        await context.bot.send_message(partner_id, "👥 Sizga suhbatdosh topildi!")
        await context.bot.send_message(user_id, "👥 Sizga suhbatdosh topildi!")
    else:
        waiting_users.append(user_id)
        await update.message.reply_text("⏳ Kuting, sizga suhbatdosh izlayapmiz...")

# Anonim xabar yuborish
async def relay_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.id
    if sender in active_chats:
        receiver = active_chats[sender]
        try:
            if update.message.text:
                await context.bot.send_message(receiver, update.message.text)
            elif update.message.sticker:
                await context.bot.send_sticker(receiver, update.message.sticker.file_id)
        except:
            await update.message.reply_text("❌ Suhbatdoshga xabar yuborib bo‘lmadi.")
    else:
        return  # Agar anonim chatda bo'lmasa, xabar yuborilmaydi

# Chatni to‘xtatish
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_chats:
        partner = active_chats[user_id]
        await context.bot.send_message(partner, "❌ Suhbat tugatildi.")
        await update.message.reply_text("❌ Suhbat tugatildi.")
        del active_chats[user_id]
        del active_chats[partner]
    else:
        await update.message.reply_text("❗Sizda faol suhbat yo‘q.")

# Tugmalarni boshqarish
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Tasodifiy" in text:
        await random_anime(update, context)
    elif "Kod orqali" in text:
        await search_by_code(update, context)
    elif "AI" in text:
        await ai_helper(update, context)
    elif "Anonim" in text:
        await anonymous_chat(update, context)
    elif "to‘xtatish" in text:
        await stop_chat(update, context)
    elif "menyu" in text:
        await update.message.reply_text("📜 Bu yerda menyu chiqadi (keyin qo‘shamiz)")
    else:
        await update.message.reply_text("❓ Noma'lum buyruq.")

# Main
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop_chat))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_buttons))
    app.add_handler(MessageHandler(filters.Sticker.ALL | filters.TEXT, relay_message))

    print("✅ Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
