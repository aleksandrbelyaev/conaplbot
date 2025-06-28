from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
import os

TOKEN = os.getenv("BOT_TOKEN")

# Для хранения состояния пользователя
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Select a service", callback_data="select_service")],
        [InlineKeyboardButton("📝 Leave a request", callback_data="request")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Hi! How can we help you today?\n\n📞 Call us: +1 (888) 249-8589",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "select_service":
        service_keyboard = [
            [InlineKeyboardButton("🧊 Refrigerator repair", callback_data="service_fridge")],
            [InlineKeyboardButton("🧺 Washer repair", callback_data="service_washer")],
            [InlineKeyboardButton("🔥 Oven/stove repair", callback_data="service_oven")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")]
        ]
        await query.edit_message_text("Please select a service:", reply_markup=InlineKeyboardMarkup(service_keyboard))

    elif query.data.startswith("service_"):
        service_map = {
            "service_fridge": "refrigerator repair",
            "service_washer": "washer repair",
            "service_oven": "oven or stove repair"
        }
        selected = service_map.get(query.data, "an unknown service")
        await query.edit_message_text(f"You selected: {selected}.\nClick 'Leave a request' or send your name and phone number.")
    
    elif query.data == "request":
        user_states[user_id] = {'step': 'zip'}
        await query.edit_message_text("Please enter your ZIP code:")

    elif query.data == "back_to_main":
        await start(update, context)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_input = update.message.text

    if user_id not in user_states:
        return  # Пользователь не в процессе заполнения

    state = user_states[user_id]

    # Этап 1: ZIP-код
    if state.get('step') == 'zip':
        user_states[user_id]['zip'] = user_input.strip()
        user_states[user_id]['step'] = 'contact'
        await update.message.reply_text("Thanks! Now please send your name and phone number:")

    # Этап 2: Имя + телефон
    elif state.get('step') == 'contact':
        user_states[user_id]['contact'] = user_input.strip()
        zip_code = user_states[user_id].get('zip')
        contact_info = user_states[user_id].get('contact')

        await update.message.reply_text(
            f"Thank you! ✅\n\nWe received your request:\n📍 ZIP: {zip_code}\n👤 Contact: {contact_info}\n\nWe'll get back to you shortly!"
        )

        # Очистим состояние
        del user_states[user_id]

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
