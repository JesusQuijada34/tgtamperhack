#!/usr/bin/env python3
"""
Demo del sistema de tokens seguros
Muestra cómo funciona la protección de tokens
"""

from secure_loader import validate_environment, get_telegram_token, get_admin_id, get_api_key

def main():
    print("🔐 Demo del Sistema de Tokens Seguros")
    print("=" * 50)
    
    # Validar entorno
    print("1. Validando entorno...")
    if validate_environment():
        print("   ✅ Entorno configurado correctamente")
    else:
        print("   ❌ Entorno no configurado")
        print("   💡 Ejecuta: python setup_tokens.py")
        return
    
    # Mostrar tokens (parcialmente enmascarados por seguridad)
    print("\n2. Tokens cargados:")
    
    bot_token = get_telegram_token()
    if bot_token and bot_token != "TU_TOKEN":
        masked_token = f"{bot_token[:8]}...{bot_token[-8:]}" if len(bot_token) > 16 else "***"
        print(f"   🤖 Bot Token: {masked_token}")
    else:
        print("   🤖 Bot Token: No configurado")
    
    admin_id = get_admin_id()
    if admin_id and admin_id != "TU_CHAT_ID":
        print(f"   👤 Admin ID: {admin_id}")
    else:
        print("   👤 Admin ID: No configurado")
    
    api_key = get_api_key()
    if api_key:
        masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
        print(f"   🔑 API Key: {masked_key}")
    else:
        print("   🔑 API Key: No configurado")
    
    print("\n3. Características de seguridad:")
    print("   🔒 Tokens cifrados con AES-256")
    print("   🎭 Tokens ofuscados antes del cifrado")
    print("   🔑 Clave maestra única por instalación")
    print("   🛡️ Archivos protegidos en .gitignore")
    
    print("\n4. Archivos de seguridad:")
    import os
    if os.path.exists(".env.encrypted"):
        print("   ✅ .env.encrypted (configuración cifrada)")
    else:
        print("   ❌ .env.encrypted (no encontrado)")
    
    if os.path.exists(".master.key"):
        print("   ✅ .master.key (clave maestra)")
    else:
        print("   ❌ .master.key (no encontrado)")
    
    print("\n🎉 Sistema de tokens seguros funcionando correctamente!")

if __name__ == "__main__":
    main()
