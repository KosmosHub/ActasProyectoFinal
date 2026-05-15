import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from ui.upload_view import UploadView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Actas — DEM Ovalle")
        self.resize(850, 550)

        # Widget central principal y layout horizontal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==========================================
        # SIDEBAR (Menú lateral fijo)
        # ==========================================
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setObjectName("pnlSidebar")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        sidebar_layout.setSpacing(0)

        self.lbl_modulos = QLabel("  MÓDULOS")
        self.lbl_modulos.setObjectName("lblModulos")
        sidebar_layout.addWidget(self.lbl_modulos)
        sidebar_layout.addSpacing(10)

        # Botones del menú
        self.btn_nueva_acta = QPushButton("+  Nueva acta")
        self.btn_nueva_acta.setObjectName("btnSidebarActive")
        self.btn_nueva_acta.setCursor(Qt.PointingHandCursor)

        self.btn_historial = QPushButton("📄  Historial")
        self.btn_historial.setObjectName("btnSidebar")
        self.btn_historial.setCursor(Qt.PointingHandCursor)

        sidebar_layout.addWidget(self.btn_nueva_acta)
        sidebar_layout.addWidget(self.btn_historial)
        sidebar_layout.addStretch()

        main_layout.addWidget(self.sidebar)

        # ==========================================
        # PANEL PRINCIPAL (Donde cambian las pantallas)
        # ==========================================
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Conectar botones del menú a las funciones de navegación
        self.btn_nueva_acta.clicked.connect(self.ir_a_carga)
        self.btn_historial.clicked.connect(self.ir_a_historial)

        # Iniciar en la pantalla de carga
        self.ir_a_carga()
        self.cargar_estilos()

    # --- FUNCIONES DE NAVEGACIÓN ---

    def cambiar_contenido(self, widget):
        # Esta función cambia el panel derecho sin borrar el menú izquierdo
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)

    def ir_a_carga(self):
        # Genera una vista de carga limpia
        self.cambiar_contenido(UploadView(self))
        self.actualizar_botones_sidebar(self.btn_nueva_acta)

    def ir_a_historial(self):
        from ui.history_view import HistoryView
        # Datos simulados con campos de OC, Folio y Establecimiento para poder probar el buscador
        data_prueba = [
            {"fecha": "15/05/2026", "oc": "111-222-333", "folio": "712-9", "establecimiento": "Liceo Bicentenario Alejandro Álvarez", "estado": "Completado"},
            {"fecha": "14/05/2026", "oc": "444-555-666", "folio": "705-6", "establecimiento": "Escuela Antonio Tirado Lanas", "estado": "Completado"},
            {"fecha": "10/05/2026", "oc": "777-888-999", "folio": "935-0", "establecimiento": "Colegio de Artes Eliseo Videla", "estado": "Error parcial"},
        ]
        self.cambiar_contenido(HistoryView(data_prueba, self))
        self.actualizar_botones_sidebar(self.btn_historial)

    def actualizar_botones_sidebar(self, boton_activo):
        # Cambia el color del botón activo en el menú
        self.btn_nueva_acta.setObjectName("btnSidebar")
        self.btn_historial.setObjectName("btnSidebar")
        boton_activo.setObjectName("btnSidebarActive")
        
        self.btn_nueva_acta.style().unpolish(self.btn_nueva_acta)
        self.btn_nueva_acta.style().polish(self.btn_nueva_acta)
        self.btn_historial.style().unpolish(self.btn_historial)
        self.btn_historial.style().polish(self.btn_historial)

    def cargar_estilos(self):
        ruta_qss = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(ruta_qss):
            try:
                with open(ruta_qss, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error QSS: {e}")