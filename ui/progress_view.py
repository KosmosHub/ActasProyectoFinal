from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QTextEdit
from PyQt5.QtCore import Qt

class ProgressView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        self.label_title = QLabel("Generando actas de despacho…")
        self.label_title.setObjectName("titleLabel")
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_note = QLabel("Por favor, no cierre la aplicación. Esto puede tomar unos segundos.")
        self.label_note.setAlignment(Qt.AlignCenter)
        self.label_note.setStyleSheet("color: #888888; font-style: italic;")

        # Barra de progreso
        self.progress = QProgressBar()
        self.progress.setFixedHeight(25)
        self.progress.setValue(0) # Inicial en 0

        # Log del proceso (estilo terminal)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setObjectName("logText") # Para darle estilo oscuro en QSS
        
        layout.addStretch()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_note)
        layout.addWidget(self.progress)
        layout.addWidget(self.log)
        layout.addStretch()

        self.setLayout(layout)

    def append_log(self, text):
        self.log.append(text)