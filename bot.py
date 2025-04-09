import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters

# Bot tokenini o'zgartiring
TOKEN = 'YOUR_BOT_TOKEN'

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Anime izlash", callback_data='search')],
        [InlineKeyboardButton("Tasodifiy anime", callback_data='random')],
        [InlineKeyboardButton("Anonim chat", callback_data='anonymous_chat')],
        [InlineKeyboardButton("Anime menyu", callback_data='anime_menu')],
        [InlineKeyboardButton("AI qidiruv", callback_data='ai_search')],
        [InlineKeyboardButton("Reklama & Homiylik", callback_data='advertising')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Salom! Iltimos, biror tugmani tanlang:', reply_markup=reply_markup)

def get_random_anime_image() -> str:
    response = requests.get('https://api.waifu.pics/sfw/waifu')
    if response.status_code == 200:
        return response.json().get('url')
    return None

def search_anime(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Iltimos, izlayotgan anime nomini yozing:")
    context.user_data['searching'] = True

def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('searching'):
        anime_name = update.message.text
        # Anime nomini qidirish uchun API qo'ng'irog'i (bu yerda siz o'zingizning API manzilingizni qo'shishingiz kerak)
        # Misol uchun, anime nomini qidirish uchun API qo'ng'irog'i
        # response = requests.get(f'YOUR_ANIME_SEARCH_API/{anime_name}')
        # if response.status_code == 200:
        #     # Qidiruv natijalarini qaytarish
        #     pass
        # else:
        #     update.message.reply_text('Anime topilmadi.')
        
        # Hozircha tasodifiy anime rasm yuborish
        image_url = get_random_anime_image()
        if image_url:
            update.message.reply_photo(photo=image_url)
        else:
            update.message.reply_text('Rasm olishda xatolik yuz berdi.')

        context.user_data['searching'] = False

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'random':
        image_url = get_random_anime_image()
        if image_url:
            query.edit_message_text(text="Mana sizga tasodifiy anime rasm:", reply_markup=None)
            query.message.reply_photo(photo=image_url)
        else:
            query.edit_message_text(text='Rasm olishda xatolik yuz berdi.')
    elif query.data == 'search':
        search_anime(update, context)
    elif query.data == 'anonymous_chat':
        query.edit_message_text(text="Anonim chat funksiyasi hozirda mavjud emas.")
    elif query.data == 'anime_menu':
        query.edit_message_text(text="Anime menyu: \n1. Anime izlash\n2. Tasodifiy anime\n3. Anonim chat")
    elif query.data == 'ai_search':
        query.edit_message_text(text="AI qidiruv funksiyasi hozirda mavjud emas.")
    elif query.data == 'advertising':
        query.edit_message_text(text="Reklama & Homiylik funksiyasi hozirda mavjud emas.")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
