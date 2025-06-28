from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Choose service", callback_data="services")],
        [InlineKeyboardButton("📞 Call Now", url="tel:+18882498589")],
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="request")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Чем можем помочь?", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "services":
        await query.edit_message_text("Вот наши услуги:\n🔧 Washer Repair\n🧺 Стиральных машин\n🔥 Плит и др.")
    elif query.data == "request":
        await query.edit_message_text("Пожалуйста, отправьте своё имя и номер телефона. Мы скоро свяжемся с вами.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()