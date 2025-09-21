#!/usr/bin/env python3
"""
Script de configuración de tokens seguros
Ejecuta este script para configurar tus tokens de forma segura
"""

import os
import sys
from config import secure_config

def main():
    print("🔐 Configurador de Tokens Seguros")
    print("=" * 50)
    print("Este script te ayudará a configurar tus tokens de forma segura.")
    print("Los tokens se cifrarán y ofuscarán para mayor protección.\n")
    
    # Verificar si ya existe configuración
    if os.path.exists(".env.encrypted"):
        print("⚠️  Ya existe una configuración cifrada.")
        overwrite = input("¿Deseas sobrescribirla? (s/N): ").strip().lower()
        if overwrite not in ['s', 'si', 'y', 'yes']:
            print("❌ Configuración cancelada.")
            return
    
    try:
        # Configurar tokens
        config = secure_config.setup_initial_config()
        
        print("\n✅ Configuración completada exitosamente!")
        print("\n📋 Resumen de configuración:")
        for key, value in config.items():
            if 'token' in key.lower() or 'key' in key.lower():
                # Mostrar solo los primeros y últimos caracteres para seguridad
                if len(value) > 8:
                    masked_value = f"{value[:4]}...{value[-4:]}"
                else:
                    masked_value = "***"
                print(f"   {key}: {masked_value}")
            else:
                print(f"   {key}: {value}")
        
        print(f"\n🔒 Archivos de seguridad creados:")
        print(f"   - .env.encrypted (configuración cifrada)")
        print(f"   - .master.key (clave maestra)")
        
        print(f"\n⚠️  IMPORTANTE:")
        print(f"   - Nunca compartas el archivo .master.key")
        print(f"   - Añade .master.key y .env.encrypted a .gitignore")
        print(f"   - Haz backup de estos archivos en un lugar seguro")
        
    except KeyboardInterrupt:
        print("\n❌ Configuración cancelada por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")

if __name__ == "__main__":
    main()
