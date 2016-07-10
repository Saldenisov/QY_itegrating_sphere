import sys, os

from PyQt5.QtWidgets import QApplication
from models import MainModel
from controllers import MainController
from logs_pack import initialize_logger


def main():
    initialize_logger(
        os.path.join(os.path.dirname(__file__), 'LOG'), "MAIN")
    app = QApplication(sys.argv)
    model = MainModel(app_folder=os.path.dirname(__file__),
                      developing=False)
    MainController(model)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
