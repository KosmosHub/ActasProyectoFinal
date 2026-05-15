from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class HistoryView(QWidget):
    def __init__(self, history_data, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # --- ENCABEZADO Y BUSCADOR ---
        header_layout = QHBoxLayout()
        
        self.label_title = QLabel("Historial de Actas Generadas")
        self.label_title.setObjectName("titleLabel")
        header_layout.addWidget(self.label_title)

        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("🔍 Buscar por OC, Folio o Establecimiento...")
        self.input_search.setFixedWidth(300)
        self.input_search.textChanged.connect(self.filtrar_historial)
        header_layout.addWidget(self.input_search, alignment=Qt.AlignRight)

        layout.addLayout(header_layout)

        # --- TABLA ---
        self.table = QTableWidget(len(history_data), 5)
        self.table.setHorizontalHeaderLabels(["Fecha", "Orden de Compra", "Folio", "Establecimiento", "Estado"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch) # Establecimiento toma el espacio
        self.table.setAlternatingRowColors(True)

        # Llenar datos (ahora con los campos OC, Folio y Establecimiento)
        for row, item in enumerate(history_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.get("fecha", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(item.get("oc", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(item.get("folio", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.get("establecimiento", ""))))
            
            # Estado con color
            estado = str(item.get("estado", ""))
            item_estado = QTableWidgetItem(estado)
            if "Error" in estado:
                item_estado.setForeground(Qt.red)
            else:
                item_estado.setForeground(Qt.green)
            self.table.setItem(row, 4, item_estado)

        layout.addWidget(self.table)

        # --- BOTÓN VOLVER ---
        self.btn_back = QPushButton("⬅️ Volver al Inicio")
        self.btn_back.setObjectName("btnSecondary")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.volver_inicio)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.btn_back, alignment=Qt.AlignLeft)
        layout.addLayout(bottom_layout)

    # --- FUNCIÓN DE FILTRADO INTELIGENTE ---
    def filtrar_historial(self, texto):
        texto = texto.lower()
        for row in range(self.table.rowCount()):
            # Obtenemos las celdas de OC (Col 1), Folio (Col 2) y Establecimiento (Col 3)
            item_oc = self.table.item(row, 1)
            item_folio = self.table.item(row, 2)
            item_estab = self.table.item(row, 3)
            
            # Si el texto escrito existe en alguna de las 3 celdas, mostramos la fila
            match = False
            if item_oc and texto in item_oc.text().lower(): match = True
            if item_folio and texto in item_folio.text().lower(): match = True
            if item_estab and texto in item_estab.text().lower(): match = True
            
            # Ocultamos la fila si no hubo coincidencia
            self.table.setRowHidden(row, not match)

    def volver_inicio(self):
        if self.parent_window:
            self.parent_window.ir_a_carga()