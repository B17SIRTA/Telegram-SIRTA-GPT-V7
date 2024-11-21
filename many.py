from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os

# تحميل المتغيرات من ملف .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 1253804825

user_ids = []

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
    update.message.reply_text('مرحباً! لقد تم تسجيلك في البوت.')

def send_broadcast(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("إرسال رسالة جماعية", callback_data='broadcast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=ADMIN_ID, text='اختر الإجراء:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'broadcast':
        for user_id in user_ids:
            context.bot.send_message(chat_id=user_id, text='هذه رسالة جماعية من البوت.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
    update.message.reply_text('تم استلام رسالتك.')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("broadcast", send_broadcast))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
