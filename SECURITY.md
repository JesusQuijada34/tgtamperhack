# 🔐 Guía de Seguridad para Tokens

Este documento explica cómo proteger los tokens y credenciales en este proyecto usando un sistema de ofuscación y cifrado.

## 🚀 Configuración Inicial

### 1. Instalar dependencias

```bash
pip install cryptography telebot python-telegram-bot requests beautifulsoup4 scapy
```

### 2. Configurar tokens de forma segura

```bash
python setup_tokens.py
```

Este script te guiará para configurar tus tokens de forma segura.

## 🛡️ Sistema de Protección

### Características de Seguridad

- **Cifrado AES-256**: Los tokens se cifran usando Fernet (AES-256)
- **Ofuscación**: Los tokens se ofuscan antes del cifrado
- **Clave maestra**: Se genera una clave única para cada instalación
- **Validación**: Verificación automática de tokens al ejecutar scripts
- **Archivos protegidos**: Los archivos sensibles están en `.gitignore`

### Archivos de Seguridad

- `.env.encrypted`: Configuración cifrada con todos los tokens
- `.master.key`: Clave maestra para descifrar la configuración
- `config.py`: Sistema de cifrado y ofuscación
- `secure_loader.py`: Cargador seguro de tokens

## 📋 Uso

### En tus scripts Python

```python
from secure_loader import get_telegram_token, get_admin_id, validate_environment

# Validar entorno
if not validate_environment():
    print("❌ Error: Tokens no configurados")
    exit(1)

# Obtener tokens
bot_token = get_telegram_token()
admin_id = get_admin_id()
```

### Funciones disponibles

- `get_telegram_token()`: Obtiene el token del bot de Telegram
- `get_admin_id()`: Obtiene el Chat ID del administrador
- `get_api_key()`: Obtiene la API key adicional
- `validate_environment()`: Valida que todos los tokens estén configurados

## 🔧 Gestión de Tokens

### Agregar un nuevo token

```python
from config import set_secure_token

set_secure_token('NUEVO_TOKEN', 'valor_del_token')
```

### Actualizar un token existente

```python
from config import set_secure_token

set_secure_token('TELEGRAM_BOT_TOKEN', 'nuevo_token')
```

## ⚠️ Mejores Prácticas

### ✅ Hacer

- Ejecutar `python setup_tokens.py` para configurar tokens
- Hacer backup de `.master.key` en un lugar seguro
- Usar el sistema de tokens seguro en todos los scripts
- Mantener los archivos de configuración fuera del control de versiones

### ❌ No hacer

- Nunca subir `.master.key` o `.env.encrypted` al repositorio
- No hardcodear tokens directamente en el código
- No compartir archivos de configuración cifrados
- No usar tokens de placeholder en producción

## 🔄 Migración desde tokens hardcodeados

Si ya tienes tokens hardcodeados en tu código:

1. Ejecuta `python setup_tokens.py`
2. Ingresa tus tokens reales cuando se soliciten
3. Los scripts se actualizarán automáticamente para usar el sistema seguro

## 🆘 Solución de Problemas

### Error: "Token requerido no encontrado"

```bash
python setup_tokens.py
```

### Error: "No se pudieron cargar los tokens"

1. Verifica que existan los archivos `.env.encrypted` y `.master.key`
2. Ejecuta `python setup_tokens.py` para recrear la configuración

### Error de permisos en archivos de configuración

```bash
chmod 600 .master.key .env.encrypted
```

## 🔍 Verificación de Seguridad

Para verificar que tu configuración es segura:

1. Los archivos `.master.key` y `.env.encrypted` no deben estar en el repositorio
2. Los tokens no deben aparecer en texto plano en el código
3. Los archivos de configuración deben tener permisos restrictivos (600)

## 📞 Soporte

Si tienes problemas con la configuración de tokens:

1. Revisa este documento
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que los archivos de configuración existan y tengan los permisos correctos
