from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    ChatMemberHandler
)

# Configuración
TOKEN = "7599405971:AAGwtBTydguBTKssHOaPnCYsb5IKFvfrngo"
ADMIN_ID = 7736662759  # Tu ID

def build_info(update: Update) -> str:
    chat = update.effective_chat
    user = update.effective_user  # Puede ser None en canales
    sender_chat = getattr(update, "effective_message", None)
    sender_title = None
    if sender_chat and getattr(sender_chat, "sender_chat", None):
        sender_title = sender_chat.sender_chat.title

    chat_id = chat.id if chat else "Desconocido"
    chat_type = chat.type if chat else "Desconocido"
    chat_title = chat.title if getattr(chat, "title", None) else "No aplica"

    user_id = user.id if user else "No disponible"
    first_name = user.first_name if user and user.first_name else "No disponible"
    last_name = user.last_name if user and user.last_name else ""
    username = f"@{user.username}" if user and user.username else "Sin username"

    # En canales, a veces el post viene firmado por la entidad del canal
    if chat_type == "channel" and sender_title:
        author = f"Autor del post: {sender_title}"
    else:
        author = f"Usuario: {user_id} ({first_name} {last_name}) • {username}"

    info = (
        "📡 Activación detectada\n"
        f"- Chat ID: {chat_id}\n"
        f"- Tipo de chat: {chat_type}\n"
        f"- Título: {chat_title}\n"
        f"- {author}"
    )
    return info

async def safe_reply(update: Update, text: str):
    # Responde donde se originó el evento, si es posible
    msg = update.effective_message
    if msg:
        try:
            await msg.reply_text(text)
        except Exception:
            pass

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    # Envía al privado del admin, capturando errores (p.ej., sin chat iniciado)
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)
        return True
    except Exception:
        return False

# /start en cualquier contexto
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = build_info(update)
    await safe_reply(update, "✅ Bot activo. Enviando datos al administrador...")
    ok = await notify_admin(context, info)
    if not ok:
        await safe_reply(update, "⚠️ No pude escribir al admin. Confirma que ya hablaste con el bot por privado.")

# Evento: el bot es agregado o cambia su estado en un chat
async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    my_member = update.my_chat_member
    if not my_member:
        return

    new_status = my_member.new_chat_member.status  # e.g., "administrator", "member", "kicked"
    # Cuando el bot es agregado o promovido, enviamos reporte
    if new_status in ("administrator", "member"):
        info = build_info(update)
        sent = await notify_admin(context, f"🆕 Bot agregado o activado en un chat:\n{info}")
        if not sent:
            # Intentamos avisar localmente en el chat donde nos agregaron
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="⚠️ No pude avisar al admin por privado. Pídele que inicie chat con el bot."
                )
            except Exception:
                pass

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatMemberHandler(on_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    app.run_polling(close_loop=False)