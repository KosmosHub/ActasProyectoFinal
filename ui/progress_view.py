# ui/progress_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QTextEdit

class ProgressView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label_title = QLabel("Generando actas de despacho…")
        self.label_note = QLabel("No cierre la aplicación.")

        # Barra de progreso
        self.progress = QProgressBar()
        self.progress.setValue(58)  # Simulación: 58% completado

        # Log del proceso
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setText(
            "✓ Escuela Diego de Almagro — Folio #0041\n"
            "✓ Colegio San Martín — Folio #0042\n"
            "✓ Liceo Técnico A-34 — Folio #0043\n"
            "➜ Procesando: Escuela República de Italia…\n"
            "Pendiente: 5 establecimientos"
        )

        layout.addWidget(self.label_title)
        layout.addWidget(self.label_note)
        layout.addWidget(self.progress)
        layout.addWidget(self.log)

        self.setLayout(layout)


# 🔹 Bloque de prueba independiente
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ProgressView()
    window.show()
    sys.exit(app.exec_())
