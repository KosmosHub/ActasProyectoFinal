from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from PyQt5.QtCore import Qt

class FileLoadedView(QWidget):
    def __init__(self, file_info, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.file_info = file_info
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<b>Vista Previa OC: {file_info.get('orden_compra')}</b>"))

        self.table = QTableWidget()
        datos = file_info.get("preview", [])
        self.table.setColumnCount(3)
        self.table.setRowCount(len(datos))
        self.table.setHorizontalHeaderLabels(["Establecimiento / RBD", "Items", "Total ($)"])

        for i, fila in enumerate(datos):
            # Usamos get con valores por defecto por seguridad
            nombre = str(fila.get("nombre", "N/A"))
            items = str(fila.get("productos", 0))
            # Formateamos el total con separadores de miles
            total_num = fila.get("total", 0)
            total_formato = f"$ {total_num:,.0f}"

            self.table.setItem(i, 0, QTableWidgetItem(nombre))
            self.table.setItem(i, 1, QTableWidgetItem(items))
            self.table.setItem(i, 2, QTableWidgetItem(total_formato))

        layout.addWidget(self.table)
        self.btn_confirm = QPushButton("✅ Generar todas las Actas y Guardar")
        self.btn_confirm.setFixedHeight(40)
        self.btn_confirm.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.btn_confirm.clicked.connect(self.finalizar)
        layout.addWidget(self.btn_confirm)
        self.setLayout(layout)

    def finalizar(self):
        import main
        try:
            # Llamamos al proceso definitivo
            if main.procesar_final(self.file_info['nombre_excel'], self.file_info):
                self.btn_confirm.setText("¡PROCESO COMPLETADO EXITOSAMENTE!")
                self.btn_confirm.setEnabled(False)
                self.btn_confirm.setStyleSheet("background-color: #95a5a6; color: white;")
            else:
                self.btn_confirm.setText("❌ ERROR EN EL PROCESO (Ver Terminal)")
        except Exception as e:
            self.btn_confirm.setText(f"❌ Error crítico: {str(e)[:30]}...")