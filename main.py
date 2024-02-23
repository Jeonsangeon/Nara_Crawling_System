from PySide6.QtWidgets import QApplication
from main_system.main_system import MainSystem

if __name__ == '__main__':
    app = QApplication()
    window = MainSystem()
    window.show()
    app.exec()