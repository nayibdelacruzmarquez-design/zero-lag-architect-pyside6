import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    # Inicializa el bucle de eventos principal (Event Loop) de PySide6
    app = QApplication(sys.argv)

    # Instancia y muestra la ventana principal con arquitectura asíncrona
    window = MainWindow()
    window.show()

    # Mantiene la aplicación viva e intercepta códigos de cierre del OS
    sys.exit(app.exec())


if __name__ == "__main__":
    main()