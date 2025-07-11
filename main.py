import sys
from PyQt5.QtWidgets import QApplication
from database import Database
from ui_main import MainWindow

def main():
    app = QApplication(sys.argv)
    db = Database()
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
