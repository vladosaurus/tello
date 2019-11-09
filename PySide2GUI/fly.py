import sys
from PyQt5 import QtWidgets
from ui.mainDialog import MainWindow


def main():
    application = QtWidgets.QApplication(sys.argv)

    mainWnd = MainWindow()
    mainWnd.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
