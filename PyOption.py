from ib_insync import *
import bullSpreadViewSmall as bsv
import sys
from PyQt5 import QtCore, QtWidgets

from localUtilities import logger


# ======== Logging ================================================


def main():
    logger.init_logger_singleton()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = bsv.Ui_MainPyOptionsWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # needed to add this with util.useQt()
    # the proper event loop for a # Qt app is set
    # but it will not start running this event loop.
    # For starting the loop the usual methods can be used, the simplest being IB.run() at the end of the program.
    IB.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
