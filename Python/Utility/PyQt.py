import sys
import random
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsDropShadowEffect

class AnimatedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.setWindowTitle("Ventana Animada e Interactiva")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Fondo dinámico
        self.color1 = QColor(50, 50, 200)
        self.color2 = QColor(200, 50, 50)
        self.gradient_timer = QTimer()
        self.gradient_timer.timeout.connect(self.update_gradient)
        self.gradient_timer.start(50)

        # Sombras y bordes redondeados
        self.setStyleSheet("border-radius: 20px; background-color: transparent;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 200))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        # Botones interactivos
        self.init_ui()

        # Animación para mover la ventana
        self.anim = QPropertyAnimation(self, b"geometry")

    def init_ui(self):
        # Botón para cambiar el color de fondo
        self.color_button = QPushButton("Cambiar Color", self)
        self.color_button.setGeometry(50, 300, 150, 40)
        self.color_button.setStyleSheet(self.button_style())
        self.color_button.clicked.connect(self.change_colors)

        # Botón para mover la ventana
        self.move_button = QPushButton("Mover Ventana", self)
        self.move_button.setGeometry(220, 300, 150, 40)
        self.move_button.setStyleSheet(self.button_style())
        self.move_button.clicked.connect(self.animate_window)

        # Botón para cerrar la ventana
        self.close_button = QPushButton("Cerrar", self)
        self.close_button.setGeometry(390, 300, 150, 40)
        self.close_button.setStyleSheet(self.button_style())
        self.close_button.clicked.connect(self.close)

    def button_style(self):
        return (
            "QPushButton {"
            "    background-color: rgba(255, 255, 255, 200);"
            "    color: black;"
            "    border-radius: 10px;"
            "    font-size: 16px;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgba(255, 255, 255, 255);"
            "}"
        )

    def change_colors(self):
        # Cambia los colores del gradiente de fondo
        self.color1 = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color2 = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def animate_window(self):
        # Mueve la ventana a una posición aleatoria en la pantalla
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        new_x = random.randint(0, screen_geometry.width() - self.width())
        new_y = random.randint(0, screen_geometry.height() - self.height())
        self.anim.setDuration(1000)
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(QRect(new_x, new_y, self.width(), self.height()))
        self.anim.start()

    def update_gradient(self):
        # Actualiza el fondo con un gradiente dinámico
        self.color1 = self.color1.lighter(102)
        self.color2 = self.color2.darker(102)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 0))
        self.setPalette(palette)
        gradient_style = (
            f"background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {self.color1.name()}, stop:1 {self.color2.name()});"
        )
        self.setStyleSheet(f"border-radius: 20px; {gradient_style}")

    def mousePressEvent(self, event):
        # Permitir arrastrar la ventana con el mouse
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedWindow()
    window.show()
    sys.exit(app.exec())
