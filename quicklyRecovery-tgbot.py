import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configura el log
logging.basicConfig(level=logging.INFO)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    chat_type = chat.type
    chat_id = chat.id
    user_id = user.id
    username = user.username or "Sin username"
    first_name = user.first_name or "Sin nombre"
    last_name = user.last_name or ""
    chat_title = chat.title or "No aplica"

    message = (
        f"👋 ¡Hola, {first_name} {last_name}!\n\n"
        f"📌 Aquí están los datos del entorno:\n"
        f"• 🧑‍💻 Usuario ID: `{user_id}`\n"
        f"• 🆔 Chat ID: `{chat_id}`\n"
        f"• 💬 Tipo de chat: `{chat_type}`\n"
        f"• 🔗 Username: @{username}\n"
        f"• 🧾 Título del chat: {chat_title}\n"
    )

    await context.bot.send_message(chat_id=chat.id, text=message, parse_mode="Markdown")

# Token de tu bot
TOKEN = "7599405971:AAGwtBTydguBTKssHOaPnCYsb5IKFvfrngo"

# Inicializa el bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()