from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Tu ID personal
ADMIN_ID = 7736662759

# Token del bot
TOKEN = "7599405971:AAGwtBTydguBTKssHOaPnCYsb5IKFvfrngo"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    # Datos del entorno
    info = (
        f"📡 Activación detectada:\n"
        f"• Chat ID: `{chat.id}`\n"
        f"• Tipo de chat: `{chat.type}`\n"
        f"• Título: {chat.title or 'No aplica'}\n"
        f"• Usuario: `{user.id}` ({user.first_name} {user.last_name or ''})\n"
        f"• Username: @{user.username or 'Sin username'}"
    )

    # Respuesta local
    await update.message.reply_text("✅ Bot activo. Enviando datos al administrador...")

    # Envío al privado del admin
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=info, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error al enviar al privado: {e}")

# Inicializa el bot
if __name__ == "__mainBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()