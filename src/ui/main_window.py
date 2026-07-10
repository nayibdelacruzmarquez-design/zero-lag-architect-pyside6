from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, \
    QTextEdit
from PySide6.QtCore import Slot
from src.ui.styles import DARK_STYLE
from src.workers.csv_worker import CSVWorker
from src.workers.api_worker import APIWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zero-Lag Architect | Dashboard Estratégico")
        self.resize(750, 500)
        self.setStyleSheet(DARK_STYLE)

        # Inicialización de Workers vacíos
        self.csv_worker = None
        self.api_worker = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)

        # Cabecera de la Aplicación
        self.lbl_titulo = QLabel("🚀 Operación: Zero-Lag Architect")
        self.lbl_titulo.setObjectName("titleLabel")
        self.lbl_subtitulo = QLabel("Dashboard de Diagnóstico Forense y Concurrencia Avanzada")
        self.lbl_subtitulo.setStyleSheet("color: #64748b; font-size: 12px;")

        main_layout.addWidget(self.lbl_titulo)
        main_layout.addWidget(self.lbl_subtitulo)

        # Panel de Control (Botones)
        layout_botones = QHBoxLayout()
        self.btn_procesar_csv = QPushButton("Procesar CSV (1M Filas)")
        self.btn_consultar_api = QPushButton("Sincronizar API Lenta")
        self.btn_cancelar = QPushButton("Cancelar Operación")
        self.btn_cancelar.setObjectName("btnCancelar")
        self.btn_cancelar.setEnabled(False)

        layout_botones.addWidget(self.btn_procesar_csv)
        layout_botones.addWidget(self.btn_consultar_api)
        layout_botones.addWidget(self.btn_cancelar)
        main_layout.addLayout(layout_botones)

        # Indicadores de Estado (Feedback UX)
        self.lbl_status = QLabel("Estado del Main Thread: Esperando acciones del usuario...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        main_layout.addWidget(self.lbl_status)
        main_layout.addWidget(self.progress_bar)

        # Consola Forense de Eventos
        self.txt_console = QTextEdit()
        self.txt_console.setReadOnly(True)
        self.txt_console.append("--- Consola de Diagnóstico Iniciada ---")
        main_layout.addWidget(self.txt_console)

        # Conexión de Eventos / Slots del Main Thread
        self.btn_procesar_csv.clicked.connect(self.start_csv_processing)
        self.btn_consultar_api.clicked.connect(self.start_api_consultation)
        self.btn_cancelar.clicked.connect(self.cancel_current_worker)

    @Slot()
    def start_csv_processing(self):
        self.toggle_ui_state(processing=True)
        self.progress_bar.setValue(0)
        self.txt_console.append("\n[Main Thread] Solicitando análisis masivo...")

        # Instanciamos el orquestador multiproceso
        self.csv_worker = CSVWorker(ruta_csv="data/datos_1M.csv")

        # Conectamos las señales seguras entre hilos
        self.csv_worker.progress.connect(self.update_progress)
        self.csv_worker.log_message.connect(self.write_to_console)
        self.csv_worker.finished.connect(self.on_csv_finished)

        # Arrancamos el hilo secundario
        self.csv_worker.start()

    @Slot()
    def start_api_consultation(self):
        self.toggle_ui_state(processing=True)
        self.progress_bar.setValue(25)  # Efecto visual intermedio para red

        self.api_worker = APIWorker()
        self.api_worker.log_message.connect(self.write_to_console)
        self.api_worker.finished.connect(self.on_api_finished)

        self.api_worker.start()

    @Slot()
    def cancel_current_worker(self):
        if self.csv_worker and self.csv_worker.isRunning():
            self.txt_console.append("\n[User Action] Enviando señal de aborto inmediato...")
            self.csv_worker.cancel()

    @Slot(int)
    def update_progress(self, val):
        self.progress_bar.setValue(val)
        self.lbl_status.setText(f"Procesando fragmentos en subprocesos activos... ({val}%)")

    @Slot(str)
    def write_to_console(self, text):
        self.txt_console.append(text)

    @Slot(dict)
    def on_csv_finished(self, result):
        self.toggle_ui_state(processing=False)
        self.txt_console.append(f"[Resultado]: {result['msg']}")
        self.lbl_status.setText("Estado del Main Thread: Ininterrumpido / Listo.")
        if result['status'] == 'Success':
            self.progress_bar.setValue(100)

    @Slot(dict)
    def on_api_finished(self, result):
        self.toggle_ui_state(processing=False)
        self.progress_bar.setValue(100)
        self.txt_console.append(f"[Resultado API]: {result['msg']}")
        self.lbl_status.setText("Estado del Main Thread: Ininterrumpido / Listo.")

    def toggle_ui_state(self, processing: bool):
        """Previene re-entrada y controla el botón de cancelación."""
        self.btn_procesar_csv.setEnabled(not processing)
        self.btn_consultar_api.setEnabled(not processing)
        self.btn_cancelar.setEnabled(processing)