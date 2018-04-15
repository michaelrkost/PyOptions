from ib_insync import *
import bullSpreadViewSmall as bsv
import sys
from PyQt5 import QtCore, QtWidgets
# ========================================================


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = bsv.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
