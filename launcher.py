import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def iniciar():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    iniciar()