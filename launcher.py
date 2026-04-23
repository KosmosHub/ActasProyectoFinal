# launcher.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def cargar_estilos(app):
    try:
        with open("ui/styles.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception:
        print("No se pudo cargar estilos QSS")

def run_app():
    app = QApplication(sys.argv)
    cargar_estilos(app)
    ventana = MainWindow()   # Aquí se carga tu ventana principal
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
