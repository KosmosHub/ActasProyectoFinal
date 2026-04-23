# ui/success_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class SuccessView(QWidget):
    def __init__(self, summary_info, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label_title = QLabel("Proceso completado")
        self.label_actas = QLabel(f"Actas generadas: {summary_info['actas']}")
        self.label_time = QLabel(f"Tiempo total: {summary_info['tiempo']} segundos")
        self.label_errors = QLabel(f"Errores: {summary_info['errores']}")

        # Botones
        self.btn_open_folder = QPushButton("Abrir carpeta de actas")
        self.btn_back = QPushButton("Volver al inicio")

        layout.addWidget(self.label_title)
        layout.addWidget(self.label_actas)
        layout.addWidget(self.label_time)
        layout.addWidget(self.label_errors)
        layout.addWidget(self.btn_open_folder)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)


# 🔹 Bloque de prueba independiente
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Datos simulados
    summary_info = {
        "actas": 12,
        "tiempo": 4,
        "errores": 0
    }

    window = SuccessView(summary_info)
    window.show()
    sys.exit(app.exec_())
