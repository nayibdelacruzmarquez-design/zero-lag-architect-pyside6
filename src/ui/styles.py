DARK_STYLE = """
QMainWindow {
    background-color: #0f172a;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #f1f5f9;
}

QLabel {
    font-size: 13px;
}

/* Tarjeta de Título */
#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #38bdf8;
    padding-bottom: 5px;
}

/* Botones Profesionales */
QPushButton {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #475569;
}

QPushButton:pressed {
    background-color: #0f172a;
}

/* Botón de Cancelación con Alto Contraste */
QPushButton#btnCancelar {
    background-color: #7f1d1d;
    border: 1px solid #991b1b;
    color: #fecaca;
}

QPushButton#btnCancelar:hover {
    background-color: #991b1b;
}

/* Barra de Progreso Fluida */
QProgressBar {
    border: 1px solid #334155;
    border-radius: 4px;
    text-align: center;
    background-color: #1e293b;
    font-weight: bold;
}

QProgressBar::chunk {
    background-color: #0284c7;
    border-radius: 3px;
}

/* Consola de Log Forense */
QTextEdit {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 6px;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    color: #38bdf8;
    padding: 8px;
}
"""