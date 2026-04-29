from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from PyQt5.QtCore import Qt

class FileLoadedView(QWidget):
    def __init__(self, file_info, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.file_info = file_info
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<b>Vista Previa Carga OC: {file_info.get('orden_compra')}</b>"))

        self.table = QTableWidget()
        datos = file_info.get("preview", [])
        self.table.setColumnCount(3)
        self.table.setRowCount(len(datos))
        self.table.setHorizontalHeaderLabels(["Establecimiento / RBD", "Items", "Total ($)"])

        for i, fila in enumerate(datos):
            self.table.setItem(i, 0, QTableWidgetItem(fila.get("nombre", "N/A")))
            self.table.setItem(i, 1, QTableWidgetItem(str(fila.get("productos", 0))))
            self.table.setItem(i, 2, QTableWidgetItem(f"$ {fila.get('total', 0):,.0f}"))

        layout.addWidget(self.table)
        self.btn_confirm = QPushButton("✅ Generar Actas y Guardar")
        self.btn_confirm.setFixedHeight(40)
        self.btn_confirm.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.btn_confirm.clicked.connect(self.finalizar)
        layout.addWidget(self.btn_confirm)
        self.setLayout(layout)

    def finalizar(self):
        import main
        if main.procesar_final(self.file_info['nombre_excel'], self.file_info):
            self.btn_confirm.setText("¡PROCESO COMPLETADO!")
            self.btn_confirm.setEnabled(False)