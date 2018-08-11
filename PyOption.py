from ib_insync import *
import buildMainQT5View as bsv
import sys
from PyQt5 import QtCore, QtWidgets

from localUtilities import logger


# ======== Logging ================================================
# todo 1- connect COntract row with The Greeks Row in Vertical Spreads
# todo 2- click on Contract and it will be highlighted in The greeks

#todo move out Call/Put button in Vertical Spreads

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
