from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit, QCompleter
from PyQt5.QtCore import Qt
from ui.file_loaded_view import FileLoadedView
from core.database import obtener_proveedores_dict
import main

class UploadView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Sistema de Actas — Ovalle 2026</b>"))
        self.status = QLabel("Seleccione el archivo Excel")

        self.input_oc = QLineEdit()
        self.input_oc.setPlaceholderText("Número de Orden de Compra")
        layout.addWidget(self.input_oc)

        self.input_prov = QLineEdit()
        self.input_prov.setPlaceholderText("Nombre del Proveedor")
        layout.addWidget(self.input_prov)

        self.input_rut = QLineEdit()
        self.input_rut.setPlaceholderText("RUT del Proveedor")
        layout.addWidget(self.input_rut)

        self.memoria = obtener_proveedores_dict()
        completer = QCompleter(self.memoria.keys())
        self.input_prov.setCompleter(completer)
        completer.activated.connect(lambda n: self.input_rut.setText(self.memoria.get(n, "")))

        self.combo_finan = QComboBox()
        self.combo_finan.addItems(["SEP", "FONDOS PROPIOS", "PIE", "MANTENCIÓN"])
        layout.addWidget(QLabel("Financiamiento:"))
        layout.addWidget(self.combo_finan)

        self.btn_select = QPushButton("📁 Cargar Excel")
        self.btn_process = QPushButton("Siguiente ➡")
        self.btn_select.clicked.connect(self.select_file)
        self.btn_process.clicked.connect(self.process_file)

        layout.addWidget(self.btn_select)
        layout.addWidget(self.status)
        layout.addWidget(self.btn_process)
        self.setLayout(layout)
        self.file_path = None

    def select_file(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Excel", "", "Excel (*.xlsx *.xls)")
        if ruta:
            self.file_path = ruta
            self.status.setText(f"Cargado: {ruta.split('/')[-1]}")

    def process_file(self):
        if not self.file_path or not self.input_oc.text():
            self.status.setText("❌ Falta cargar archivo o ingresar OC.")
            return
        
        try:
            prev_data = main.analizar_excel_previa(self.file_path)
            if not prev_data:
                self.status.setText("❌ No se detectaron colegios válidos.")
                return

            file_info = {
                "nombre_excel": self.file_path, "orden_compra": self.input_oc.text(),
                "proveedor_nombre": self.input_prov.text(), "proveedor_rut": self.input_rut.text(),
                "financiamiento": self.combo_finan.currentText(), "preview": prev_data
            }
            main_win = self.parent_window or self.window()
            main_win.setCentralWidget(FileLoadedView(file_info, main_win))
        except Exception as e:
            self.status.setText(f"Error: {e}")