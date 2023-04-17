from components.window import Window
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication([])
    window = Window()
    app.exec()

if __name__ == "__main__":
    main()