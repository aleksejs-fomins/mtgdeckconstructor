###############################
# Import system libraries
###############################
import os, sys, locale
from PyQt5 import QtGui, QtCore, QtWidgets

###############################
# Export Root Directory
###############################
thisdir = os.path.dirname(os.path.abspath(__file__))
rootdir = os.path.dirname(thisdir)
sys.path.append(rootdir)

#######################################
# Compile QT File
#######################################
ui_ui_path = os.path.join(thisdir, "MTG_GUI", 'mtg_ui.ui')
ui_py_path = os.path.join(thisdir, "MTG_GUI", 'mtg_ui.py')
qtCompilePrefStr = 'pyuic5 ' + ui_ui_path + ' -o ' + ui_py_path
print("Compiling QT GUI file", qtCompilePrefStr)
os.system(qtCompilePrefStr)

#######################################
# Import local libraries
#######################################

from src.MTG_GUI.mtg_ui import Ui_MTG_UI

#######################################################
# Main Window
#######################################################
class MtgGUI():
    def __init__(self, dialog):

        # Init
        self.dialog = dialog
        self.gui = Ui_MTG_UI()
        self.gui.setupUi(dialog)

        # GUI-Constants
        self.fontsize = 15


#######################################################
## Start the QT window
#######################################################
if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    locale.setlocale(locale.LC_TIME, "en_GB.utf8")
    classInstance = MtgGUI(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())