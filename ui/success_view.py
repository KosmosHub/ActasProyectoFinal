import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt

class SuccessView(QWidget):
    def __init__(self, summary_info, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        self.label_title = QLabel("✅ ¡Proceso Completado!")
        self.label_title.setObjectName("titleLabel")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("color: #27ae60; font-size: 26px;")

        resumen_frame = QFrame()
        resumen_frame.setObjectName("resumenFrame")
        resumen_layout = QVBoxLayout(resumen_frame)
        resumen_layout.setSpacing(10)

        actas_gen = summary_info.get('actas', 0)
        tiempo_gen = summary_info.get('tiempo', 0)
        errores_gen = summary_info.get('errores', 0)

        self.label_actas = QLabel(f"<b>📄 Actas generadas con éxito:</b> {actas_gen}")
        self.label_time = QLabel(f"<b>⏱ Tiempo de procesamiento:</b> {tiempo_gen} segundos")
        self.label_errors = QLabel(f"<b>⚠️ Actas con errores:</b> {errores_gen}")
        
        if errores_gen > 0:
            self.label_errors.setStyleSheet("color: #e74c3c; font-size: 15px;")
        else:
            self.label_errors.setStyleSheet("color: #27ae60; font-size: 15px;")

        resumen_layout.addWidget(self.label_actas)
        resumen_layout.addWidget(self.label_time)
        resumen_layout.addWidget(self.label_errors)

        self.btn_open_folder = QPushButton("📂 Abrir carpeta de Actas Generadas")
        self.btn_open_folder.setObjectName("btnPrimary")
        self.btn_open_folder.setFixedHeight(50)
        self.btn_open_folder.setCursor(Qt.PointingHandCursor)
        self.btn_open_folder.clicked.connect(self.abrir_carpeta)

        self.btn_back = QPushButton("⬅️ Iniciar un nuevo proceso")
        self.btn_back.setObjectName("btnSecondary")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.volver_inicio)

        layout.addStretch()
        layout.addWidget(self.label_title)
        layout.addWidget(resumen_frame)
        layout.addSpacing(20)
        layout.addWidget(self.btn_open_folder)
        layout.addWidget(self.btn_back)
        layout.addStretch()

    def abrir_carpeta(self):
        ruta_output = os.path.join(os.getcwd(), "output")
        if os.path.exists(ruta_output):
            os.startfile(ruta_output)
        else:
            os.startfile(os.getcwd())

    def volver_inicio(self):
        if self.parent_window:
            self.parent_window.ir_a_carga()