from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QTableWidget, 
                             QTableWidgetItem, QLabel, QPushButton, QLineEdit, 
                             QComboBox, QHeaderView)
from PyQt5.QtCore import Qt
from ui.success_view import SuccessView

class FileLoadedView(QWidget):
    def __init__(self, file_info, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.file_info = file_info
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        titulo = QLabel("<b>Detalles del Documento</b>")
        titulo.setStyleSheet("font-size: 16px;")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.input_oc = QLineEdit()
        self.input_oc.setText(str(file_info.get('orden_compra', '')))
        form_layout.addRow("Orden de Compra:", self.input_oc)

        self.input_proveedor = QLineEdit()
        self.input_proveedor.setText(str(file_info.get('proveedor_nombre', '')))
        form_layout.addRow("Proveedor:", self.input_proveedor)

        self.input_rut = QLineEdit()
        self.input_rut.setText(str(file_info.get('proveedor_rut', '')))
        form_layout.addRow("RUT Proveedor:", self.input_rut)

        self.combo_financiamiento = QComboBox()
        self.combo_financiamiento.addItems(["Seleccione...", "SEP", "FAEP", "PIE", "FONDOS PROPIOS"])
        
        finan_actual = str(file_info.get('financiamiento', ''))
        index = self.combo_financiamiento.findText(finan_actual)
        if index >= 0:
            self.combo_financiamiento.setCurrentIndex(index)
            
        form_layout.addRow("Financiamiento:", self.combo_financiamiento)
        layout.addLayout(form_layout)

        label_tabla = QLabel("<b>Vista Previa de Distribución:</b>")
        label_tabla.setStyleSheet("margin-top: 10px;")
        layout.addWidget(label_tabla)

        self.table = QTableWidget()
        datos = file_info.get("preview", [])
        self.table.setColumnCount(3)
        self.table.setRowCount(len(datos))
        self.table.setHorizontalHeaderLabels(["Establecimiento / RBD", "Ítems", "Total ($)"])

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)

        for i, fila in enumerate(datos):
            nombre = str(fila.get("nombre", "N/A"))
            items = str(fila.get("productos", 0))
            total_num = fila.get("total", 0)
            total_formato = f"$ {total_num:,.0f}".replace(",", ".")

            self.table.setItem(i, 0, QTableWidgetItem(nombre))
            item_cant = QTableWidgetItem(items); item_cant.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, item_cant)
            item_total = QTableWidgetItem(total_formato); item_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(i, 2, item_total)

        layout.addWidget(self.table)

        self.btn_confirm = QPushButton("✅ Generar todas las Actas y Guardar")
        self.btn_confirm.setObjectName("btnConfirmar")
        self.btn_confirm.setFixedHeight(45)
        self.btn_confirm.setCursor(Qt.PointingHandCursor)
        self.btn_confirm.clicked.connect(self.finalizar)
        layout.addWidget(self.btn_confirm)

    def finalizar(self):
        import main
        self.file_info.update({
            "orden_compra": self.input_oc.text(),
            "proveedor_nombre": self.input_proveedor.text(),
            "proveedor_rut": self.input_rut.text(),
            "financiamiento": self.combo_financiamiento.currentText()
        })

        try:
            resultado = main.procesar_final(self.file_info['nombre_excel'], self.file_info)
            if resultado is not None:
                vista_exito = SuccessView(resultado, self.parent_window)
                if self.parent_window:
                    # Cambiamos usando la nueva función
                    self.parent_window.cambiar_contenido(vista_exito)
            else:
                self.btn_confirm.setText("❌ ERROR: Archivo vacío o ilegible")
                self.btn_confirm.setObjectName("btnError")
                self.btn_confirm.style().unpolish(self.btn_confirm); self.btn_confirm.style().polish(self.btn_confirm)
                
        except Exception as e:
            self.btn_confirm.setText(f"❌ Error crítico: {str(e)[:30]}...")