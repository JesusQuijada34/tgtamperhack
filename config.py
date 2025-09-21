"""
Sistema de configuración seguro para tokens y credenciales
Protege los tokens mediante ofuscación y cifrado
"""

import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import getpass

class SecureConfig:
    def __init__(self, config_file=".env.encrypted", master_key_file=".master.key"):
        self.config_file = config_file
        self.master_key_file = master_key_file
        self.fernet = None
        self._load_or_create_key()
    
    def _load_or_create_key(self):
        """Carga o crea la clave maestra para cifrado"""
        if os.path.exists(self.master_key_file):
            with open(self.master_key_file, 'rb') as f:
                key = f.read()
        else:
            # Generar nueva clave maestra
            key = Fernet.generate_key()
            with open(self.master_key_file, 'wb') as f:
                f.write(key)
            os.chmod(self.master_key_file, 0o600)  # Solo lectura para el propietario
        
        self.fernet = Fernet(key)
    
    def _obfuscate_token(self, token):
        """Ofusca un token usando técnicas de codificación"""
        if not token or token == 'TU_TOKEN':
            return None
        
        # Codificación múltiple para ofuscación
        encoded = base64.b64encode(token.encode()).decode()
        # Añadir ruido aleatorio
        noise = base64.b64encode(os.urandom(16)).decode()[:8]
        obfuscated = f"{noise}{encoded}{noise[::-1]}"
        return obfuscated
    
    def _deobfuscate_token(self, obfuscated_token):
        """Desofusca un token"""
        if not obfuscated_token:
            return None
        
        try:
            # Remover ruido
            clean_token = obfuscated_token[8:-8]
            # Decodificar
            token = base64.b64decode(clean_token).decode()
            return token
        except:
            return None
    
    def encrypt_config(self, config_dict):
        """Cifra la configuración completa"""
        # Ofuscar tokens antes de cifrar
        obfuscated_config = {}
        for key, value in config_dict.items():
            if 'token' in key.lower() or 'key' in key.lower():
                obfuscated_config[key] = self._obfuscate_token(value)
            else:
                obfuscated_config[key] = value
        
        # Cifrar la configuración
        config_json = json.dumps(obfuscated_config, indent=2)
        encrypted_config = self.fernet.encrypt(config_json.encode())
        
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_config)
        os.chmod(self.config_file, 0o600)
    
    def decrypt_config(self):
        """Descifra y carga la configuración"""
        if not os.path.exists(self.config_file):
            return {}
        
        with open(self.config_file, 'rb') as f:
            encrypted_data = f.read()
        
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            config_dict = json.loads(decrypted_data.decode())
            
            # Desofuscar tokens
            deobfuscated_config = {}
            for key, value in config_dict.items():
                if 'token' in key.lower() or 'key' in key.lower():
                    deobfuscated_config[key] = self._deobfuscate_token(value)
                else:
                    deobfuscated_config[key] = value
            
            return deobfuscated_config
        except Exception as e:
            print(f"Error al descifrar configuración: {e}")
            return {}
    
    def set_token(self, key, value):
        """Establece un token de forma segura"""
        config = self.decrypt_config()
        config[key] = value
        self.encrypt_config(config)
    
    def get_token(self, key, default=None):
        """Obtiene un token de forma segura"""
        config = self.decrypt_config()
        return config.get(key, default)
    
    def setup_initial_config(self):
        """Configuración inicial interactiva"""
        print("🔐 Configuración segura de tokens")
        print("=" * 40)
        
        config = {}
        
        # Token del bot principal
        bot_token = input("Ingresa el token del bot de Telegram (o presiona Enter para usar placeholder): ").strip()
        if not bot_token:
            bot_token = "TU_TOKEN"
        config['TELEGRAM_BOT_TOKEN'] = bot_token
        
        # Chat ID del administrador
        admin_id = input("Ingresa el Chat ID del administrador (o presiona Enter para usar placeholder): ").strip()
        if not admin_id:
            admin_id = "TU_CHAT_ID"
        else:
            try:
                admin_id = int(admin_id)
            except ValueError:
                print("⚠️ Chat ID inválido, usando placeholder")
                admin_id = "TU_CHAT_ID"
        config['ADMIN_CHAT_ID'] = admin_id
        
        # Otros tokens si es necesario
        api_key = input("Ingresa API Key adicional (opcional): ").strip()
        if api_key:
            config['API_KEY'] = api_key
        
        # Cifrar y guardar
        self.encrypt_config(config)
        print("✅ Configuración guardada de forma segura")
        
        return config

# Instancia global para uso en toda la aplicación
secure_config = SecureConfig()

def get_secure_token(key, default=None):
    """Función de conveniencia para obtener tokens de forma segura"""
    return secure_config.get_token(key, default)

def set_secure_token(key, value):
    """Función de conveniencia para establecer tokens de forma segura"""
    secure_config.set_token(key, value)
