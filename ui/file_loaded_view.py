# ui/file_loaded_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem

class FileLoadedView(QWidget):
    def __init__(self, file_info, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label_file = QLabel(f"Archivo cargado: {file_info['nombre']} (válido)")
        self.label_financiamiento = QLabel(f"Financiamiento: {file_info['financiamiento']}")
        self.label_summary = QLabel(
            f"Establecimientos: {file_info['establecimientos']} | "
            f"Productos: {file_info['productos']} | "
            f"Actas a generar: {file_info['actas']}"
        )

        self.table = QTableWidget(len(file_info['preview']), 3)
        self.table.setHorizontalHeaderLabels(["Establecimiento", "Productos", "Total"])
        for row, item in enumerate(file_info['preview']):
            self.table.setItem(row, 0, QTableWidgetItem(item['nombre']))
            self.table.setItem(row, 1, QTableWidgetItem(str(item['productos'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['total'])))

        self.btn_change = QPushButton("Cambiar archivo")
        self.btn_process = QPushButton("Procesar actas")

        layout.addWidget(self.label_file)
        layout.addWidget(self.label_summary)
        layout.addWidget(self.label_financiamiento)  # ahora sí funciona
        layout.addWidget(self.table)
        layout.addWidget(self.btn_change)
        layout.addWidget(self.btn_process)

        self.setLayout(layout)


# 🔹 Bloque de prueba independiente
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Datos de prueba completos (incluye financiamiento)
    file_info = {
        "nombre": "OrdenCompra_2024_05.xlsx",
        "establecimientos": 12,
        "productos": 48,
        "actas": 12,
        "financiamiento": "Subvención Escolar Preferencial (SEP)",  # agregado
        "preview": [
            {"nombre": "Colegio San Martín", "productos": 6, "total": 124500},
            {"nombre": "Escuela Diego de Almagro", "productos": 4, "total": 88200},
        ]
    }

    window = FileLoadedView(file_info)
    window.show()

    sys.exit(app.exec_())
