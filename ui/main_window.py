from PyQt5.QtWidgets import QMainWindow
from ui.upload_view import UploadView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Actas — DEM Ovalle")
        self.resize(800, 600)
        self.setCentralWidget(UploadView(self))