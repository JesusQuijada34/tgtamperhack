"""
Cargador seguro para tokens y credenciales
Proporciona una interfaz unificada para cargar tokens de forma segura
"""

import os
import sys
from config import secure_config, get_secure_token, set_secure_token

class SecureTokenLoader:
    """Cargador seguro de tokens con múltiples fuentes de configuración"""
    
    def __init__(self):
        self.tokens = {}
        self._load_all_tokens()
    
    def _load_all_tokens(self):
        """Carga todos los tokens desde diferentes fuentes"""
        # Cargar desde configuración cifrada
        encrypted_config = secure_config.decrypt_config()
        self.tokens.update(encrypted_config)
        
        # Cargar desde variables de entorno (para desarrollo)
        env_tokens = {
            'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
            'ADMIN_CHAT_ID': os.getenv('ADMIN_CHAT_ID'),
            'API_KEY': os.getenv('API_KEY'),
        }
        
        # Actualizar con variables de entorno si existen
        for key, value in env_tokens.items():
            if value:
                self.tokens[key] = value
    
    def get_token(self, token_name, required=True, default=None):
        """
        Obtiene un token de forma segura
        
        Args:
            token_name: Nombre del token a obtener
            required: Si el token es requerido (lanzará excepción si no existe)
            default: Valor por defecto si el token no existe
        
        Returns:
            El valor del token o None si no existe y no es requerido
        """
        token_value = self.tokens.get(token_name, default)
        
        if required and not token_value:
            raise ValueError(f"Token requerido '{token_name}' no encontrado. "
                           f"Configúralo usando: python setup_tokens.py")
        
        return token_value
    
    def get_telegram_bot_token(self):
        """Obtiene el token del bot de Telegram"""
        return self.get_token('TELEGRAM_BOT_TOKEN')
    
    def get_admin_chat_id(self):
        """Obtiene el Chat ID del administrador"""
        chat_id = self.get_token('ADMIN_CHAT_ID')
        if chat_id and chat_id != "TU_CHAT_ID":
            try:
                return int(chat_id)
            except ValueError:
                pass
        return chat_id
    
    def get_api_key(self):
        """Obtiene la API Key adicional"""
        return self.get_token('API_KEY', required=False)
    
    def validate_tokens(self):
        """Valida que todos los tokens requeridos estén presentes"""
        required_tokens = ['TELEGRAM_BOT_TOKEN', 'ADMIN_CHAT_ID']
        missing_tokens = []
        
        for token in required_tokens:
            if not self.get_token(token, required=False):
                missing_tokens.append(token)
        
        if missing_tokens:
            print("❌ Tokens faltantes:")
            for token in missing_tokens:
                print(f"   - {token}")
            print("\n💡 Ejecuta: python setup_tokens.py")
            return False
        
        return True
    
    def setup_missing_tokens(self):
        """Configura los tokens faltantes de forma interactiva"""
        if not self.validate_tokens():
            print("\n🔧 Configurando tokens faltantes...")
            secure_config.setup_initial_config()
            self._load_all_tokens()
            return self.validate_tokens()
        return True

# Instancia global
token_loader = SecureTokenLoader()

def get_telegram_token():
    """Función de conveniencia para obtener el token de Telegram"""
    return token_loader.get_telegram_bot_token()

def get_admin_id():
    """Función de conveniencia para obtener el ID del administrador"""
    return token_loader.get_admin_chat_id()

def get_api_key():
    """Función de conveniencia para obtener la API key"""
    return token_loader.get_api_key()

def validate_environment():
    """Valida que el entorno esté configurado correctamente"""
    return token_loader.setup_missing_tokens()
