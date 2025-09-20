import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configura el log
logging.basicConfig(level=logging.INFO)

# Tu ID personal (puedes obtenerlo con @userinfobot si no lo tienes)
ADMIN_ID = 5824140104  # ← reemplaza con tu ID si cambia

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

    # Mensaje para el usuario que ejecuta /start
    local_message = (
        f"👋 ¡Hola, {first_name} {last_name}!\n"
        f"Este bot está activo y ha detectado el entorno correctamente."
    )
    await context.bot.send_message(chat_id=chat.id, text=local_message)

    # Mensaje privado al administrador
    admin_message = (
        f"📡 Activación detectada:\n\n"
        f"• 🆔 Chat ID: `{chat_id}`\n"
        f"• 💬 Tipo de chat: `{chat_type}`\n"
        f"• 🧾 Título del chat: {chat_title}\n"
        f"• 👤 Usuario que lo activó: `{user_id}` ({first_name} {last_name})\n"
        f"• 🔗 Username: @{username}\n"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")

# Token del bot
TOKEN = "7599405971:AAGwtBTydguBTKssHOaPnCYsb5IKFvfrngo"

# Inicializa el bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()