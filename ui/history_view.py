# ui/history_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class HistoryView(QWidget):
    def __init__(self, history_data, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label_title = QLabel("Historial de actas generadas")

        # Tabla con historial
        self.table = QTableWidget(len(history_data), 4)
        self.table.setHorizontalHeaderLabels(["Fecha", "Archivo", "Actas", "Estado"])

        for row, item in enumerate(history_data):
            self.table.setItem(row, 0, QTableWidgetItem(item["fecha"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["archivo"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["actas"])))
            self.table.setItem(row, 3, QTableWidgetItem(item["estado"]))

        layout.addWidget(self.label_title)
        layout.addWidget(self.table)

        self.setLayout(layout)


# 🔹 Bloque de prueba independiente
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Datos simulados
    history_data = [
        {"fecha": "2026-04-20", "archivo": "OrdenCompra_2026_04.xlsx", "actas": 12, "estado": "Completado"},
        {"fecha": "2026-04-18", "archivo": "OrdenCompra_2026_03.xlsx", "actas": 10, "estado": "Completado"},
        {"fecha": "2026-04-15", "archivo": "OrdenCompra_2026_02.xlsx", "actas": 8, "estado": "Error en 1 acta"},
    ]

    window = HistoryView(history_data)
    window.show()
    sys.exit(app.exec_())
