from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Выбрать услугу", callback_data="services")],
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="request")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Чем можем помочь?\n\n📞 Позвонить: +1 (888) 249-8589",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        await query.edit_message_text(
            "Наши услуги:\n🔧 Ремонт холодильников\n🧺 Стиральных машин\n🔥 Плит и духовок\n🧊 Льдогенераторов и др."
        )
    elif query.data == "request":
        await query.edit_message_text(
            "Пожалуйста, отправьте своё имя, номер телефона и кратко опишите проблему. Мы свяжемся с вами как можно скорее."
        )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
