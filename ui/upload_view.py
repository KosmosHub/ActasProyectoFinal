# ui/upload_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox
from ui.file_loaded_view import FileLoadedView
import main

class UploadView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        layout = QVBoxLayout()

        self.label = QLabel("Arrastra o selecciona el archivo Excel oficial del DEM")
        self.status = QLabel("Sin archivo seleccionado")

        # 🔹 ComboBox para financiamiento
        self.combo_financiamiento = QComboBox()
        self.combo_financiamiento.addItems([
            "Subvención Escolar Preferencial (SEP)",
            "Fondos Propios",
            "Programa de Mejoramiento",
            "Convenio Marco",
            "Otros"
        ])

        self.btn_select = QPushButton("Seleccionar archivo")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_process = QPushButton("Procesar actas")

        self.btn_select.clicked.connect(self.select_file)
        self.btn_process.clicked.connect(self.process_file)

        layout.addWidget(self.label)
        layout.addWidget(self.status)
        layout.addWidget(QLabel("Seleccione financiamiento:"))
        layout.addWidget(self.combo_financiamiento)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_process)

        self.setLayout(layout)
        self.file_path = None

    def select_file(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Excel oficial del DEM",
            "",
            "Archivos Excel (*.xlsx *.xls)"
        )
        if ruta:
            self.file_path = ruta
            self.status.setText(f"Archivo seleccionado: {ruta}")

    def process_file(self):
        if not self.file_path:
            self.status.setText("Primero selecciona un archivo.")
            return
        try:
            resultados = main.procesar_excel(self.file_path)

            # 🔹 Capturar financiamiento seleccionado
            financiamiento = self.combo_financiamiento.currentText()

            # Simulación de datos que devuelve procesar_excel
            file_info = {
                "nombre": self.file_path,
                "establecimientos": 12,
                "productos": 48,
                "actas": 12,
                "financiamiento": financiamiento,
                "preview": [
                    {"nombre": "Colegio San Martín", "productos": 6, "total": 124500},
                    {"nombre": "Escuela Diego de Almagro", "productos": 4, "total": 88200},
                ]
            }

            # Cambiar vista en MainWindow → Pantalla 2
            self.parent_window.setCentralWidget(FileLoadedView(file_info, self.parent_window))

        except Exception as e:
            self.status.setText(f"Error: {str(e)}")
