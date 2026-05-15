import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QFileDialog, QLineEdit, QComboBox, QGridLayout, QCompleter, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.file_loaded_view import FileLoadedView
from core.database import obtener_proveedores_dict
import main

class DropZone(QFrame):
    file_dropped = pyqtSignal(str)
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setObjectName("dropZone")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        self.lblArrastra = QLabel("Arrastra el archivo .xlsx o .xls aquí")
        self.lblArrastra.setStyleSheet("color: #aaaaaa; font-weight: bold; font-size: 15px; border: none;")
        self.lblArrastra.setAlignment(Qt.AlignCenter)
        
        self.btnSeleccionar = QPushButton("Seleccionar archivo")
        self.btnSeleccionar.setFixedSize(180, 35)
        self.btnSeleccionar.setCursor(Qt.PointingHandCursor)
        self.btnSeleccionar.clicked.connect(self.clicked.emit)
        
        layout.addWidget(self.lblArrastra)
        layout.addWidget(self.btnSeleccionar, alignment=Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].isLocalFile():
                if urls[0].toLocalFile().endswith(('.xls', '.xlsx')):
                    event.accept()
                    self.setProperty("hover", True)
                    self.style().unpolish(self); self.style().polish(self)
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setProperty("hover", False)
        self.style().unpolish(self); self.style().polish(self)

    def dropEvent(self, event):
        self.setProperty("hover", False)
        self.style().unpolish(self); self.style().polish(self)
        urls = event.mimeData().urls()
        if urls:
            self.file_dropped.emit(urls[0].toLocalFile())

class UploadView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.selected_file = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # 1. pnlDropZone (Arriba)
        self.drop_zone = DropZone()
        self.drop_zone.setFixedHeight(170)
        self.drop_zone.file_dropped.connect(self.archivo_cargado)
        self.drop_zone.clicked.connect(self.seleccionar_archivo_manual)
        layout.addWidget(self.drop_zone)

        # 2. Grid de Entradas
        grid = QGridLayout()
        grid.setSpacing(15)

        self.combo_finan = QComboBox()
        self.combo_finan.addItems(["Seleccionar Financiamiento...", "SEP", "FAEP", "PIE", "FONDOS PROPIOS"])
        
        self.input_oc = QLineEdit()
        self.input_oc.setPlaceholderText("Escriba Orden de compra")

        self.input_proveedor = QLineEdit()
        self.input_proveedor.setPlaceholderText("Nombre del proveedor")

        self.input_rut = QLineEdit()
        self.input_rut.setPlaceholderText("RUT del proveedor")

        self.memoria = obtener_proveedores_dict()
        completer = QCompleter(list(self.memoria.keys()))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.input_proveedor.setCompleter(completer)
        completer.activated.connect(self.autocompletar_rut)

        grid.addWidget(self.combo_finan, 0, 0)
        grid.addWidget(self.input_oc, 0, 1)
        grid.addWidget(self.input_proveedor, 1, 0)
        grid.addWidget(self.input_rut, 1, 1)

        layout.addLayout(grid)

        # 3. button1 (Estado del archivo)
        self.btn_status = QPushButton("Sin Archivo seleccionado")
        self.btn_status.setObjectName("btnStatus")
        self.btn_status.setFixedHeight(45)
        self.btn_status.setCursor(Qt.PointingHandCursor)
        self.btn_status.clicked.connect(self.seleccionar_archivo_manual)
        layout.addWidget(self.btn_status)

        layout.addStretch()

        # 4. Botones inferiores
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("btnCancelar")
        self.btn_cancelar.setFixedSize(110, 45)
        self.btn_cancelar.setCursor(Qt.PointingHandCursor)
        
        self.btn_procesar = QPushButton("Procesar actas")
        self.btn_procesar.setObjectName("btnProcesar")
        self.btn_procesar.setFixedSize(140, 45)
        self.btn_procesar.setCursor(Qt.PointingHandCursor)
        self.btn_procesar.setEnabled(False)
        self.btn_procesar.clicked.connect(self.procesar_inicial)

        bottom_layout.addWidget(self.btn_cancelar)
        bottom_layout.addWidget(self.btn_procesar)

        layout.addLayout(bottom_layout)

        self.input_oc.textChanged.connect(self.validar_formulario)
        self.input_proveedor.textChanged.connect(self.validar_formulario)
        self.input_rut.textChanged.connect(self.validar_formulario)
        self.combo_finan.currentIndexChanged.connect(self.validar_formulario)

    def autocompletar_rut(self, nombre_proveedor):
        self.input_rut.setText(self.memoria.get(nombre_proveedor, ""))
        self.validar_formulario()

    def validar_formulario(self):
        oc = self.input_oc.text().strip()
        prov = self.input_proveedor.text().strip()
        rut = self.input_rut.text().strip()
        finan = self.combo_finan.currentIndex() > 0
        self.btn_procesar.setEnabled(all([oc, prov, rut, finan, self.selected_file]))

    def archivo_cargado(self, file_path):
        self.selected_file = file_path
        self.btn_status.setText(f"✅ Archivo seleccionado: {os.path.basename(file_path)}")
        self.btn_status.setObjectName("btnStatusActive")
        self.btn_status.style().unpolish(self.btn_status)
        self.btn_status.style().polish(self.btn_status)
        self.validar_formulario()

    def seleccionar_archivo_manual(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir Excel", "", "Excel Files (*.xlsx *.xls)")
        if path: self.archivo_cargado(path)

    def procesar_inicial(self):
        import main
        try:
            datos_previa = main.analizar_excel_previa(self.selected_file)
            if not datos_previa:
                self.btn_status.setText("❌ Error: No se detectaron colegios válidos.")
                self.btn_status.setObjectName("btnStatusError")
                self.btn_status.style().unpolish(self.btn_status); self.btn_status.style().polish(self.btn_status)
                return

            file_info = {
                "preview": datos_previa,
                "nombre_excel": self.selected_file,
                "orden_compra": self.input_oc.text(),
                "proveedor": self.input_proveedor.text(),
                "rut_proveedor": self.input_rut.text(),
                "proveedor_nombre": self.input_proveedor.text(),
                "proveedor_rut": self.input_rut.text(),
                "financiamiento": self.combo_finan.currentText()
            }
            # Cambiamos usando la nueva función
            self.parent_window.cambiar_contenido(FileLoadedView(file_info, self.parent_window))
            
        except Exception as e:
            self.btn_status.setText(f"❌ Error: {e}")