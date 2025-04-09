import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Bot tokenini o'zgartiring
TOKEN = ()

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Anime izlash", callback_data='search')],
        [InlineKeyboardButton("Tasodifiy anime", callback_data='random')],
        [InlineKeyboardButton("Anonim chat", callback_data='anonymous_chat')],
        [InlineKeyboardButton("Anime menyu", callback_data='anime_menu')],
        [InlineKeyboardButton("AI qidiruv", callback_data='ai_search')],
        [InlineKeyboardButton("Reklama & Homiylik", callback_data='advertising')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Salom! Iltimos, biror tugmani tanlang:', reply_markup=reply_markup)

async def get_random_anime_image() -> str:
    response = requests.get('https://api.waifu.pics/sfw/waifu')
    if response.status_code == 200:
        return response.json().get('url')
    return None

async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Iltimos, izlayotgan anime nomini yozing:")
    context.user_data['searching'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('searching'):
        anime_name = update.message.text
        # Anime nomini qidirish uchun API qo'ng'irog'i (bu yerda siz o'zingizning API manzilingizni qo'shishingiz kerak)
        # Misol uchun, anime nomini qidirish uchun API qo'ng'irog'i
        # response = requests.get(f'YOUR_ANIME_SEARCH_API/{anime_name}')
        # if response.status_code == 200:
        #     # Qidiruv natijalarini qaytarish
        #     pass
        # else:
        #     await update.message.reply_text('Anime topilmadi.')
        
        # Hozircha tasodifiy anime rasm yuborish
        image_url = await get_random_anime_image()
        if image_url:
            await update.message.reply_photo(photo=image_url)
        else:
            await update.message.reply_text('Rasm olishda xatolik yuz berdi.')

        context.user_data['searching'] = False

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'random':
        image_url = await get_random_anime_image()
        if image_url:
            await query.edit_message_text(text="Mana sizga tasodifiy anime rasm:", reply_markup=None)
            await query.message.reply_photo(photo=image_url)
        else:
            await query.edit_message_text(text='Rasm olishda xatolik yuz berdi.')
    elif query.data == 'search':
        await search_anime(update, context)
    elif query.data == 'anonymous_chat':
        await query.edit_message_text(text="Anonim chat funksiyasi hozirda mavjud emas.")
    elif query.data == 'anime_menu':
        await query.edit_message_text(text="Anime menyu: \n1. Anime izlash\n2. Tasodifiy anime\n3. Anonim chat")
    elif query.data == 'ai_search':
        await query.edit_message_text(text="AI qidiruv funksiyasi hozirda mavjud emas.")
    elif query.data == 'advertising':
        await query.edit_message_text(text="Reklama & Homiylik funksiyasi hozirda mavjud emas.")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
