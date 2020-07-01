###############################
# Import system libraries
###############################
import os, sys, locale
import requests
import json
import pandas as pd
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

        # Reacts
        self.gui.queryPushButton.clicked.connect(self.get_query)
        self.gui.queryAddCollectionPushButton.clicked.connect(self.query_add_to_collection)

        # Example request: 'https://api.scryfall.com/cards/search?q=c%3Dwhite+cmc%3D1'
    def get_query(self):
        txt = self.gui.queryLineEdit.text()
        dict = json.loads(txt)

        cardsSite = "https://api.scryfall.com/cards/search?q="
        req = cardsSite + "+".join([str(k) + "%3D" + str(v) for k, v in dict.items()])
        r = requests.get(req)
        rJSON = r.json()

        importantColumns = ['name', 'mana_cost', 'power', 'toughness', 'rarity', 'set', 'type_line']
        df = pd.DataFrame(rJSON['data'])
        df = df[importantColumns]

        self.gui.responseTextEdit.setText(str(df))

        self.recentQueryDF = df


    def query_add_to_collection(self):
        self.display_dataframe_collection(self.recentQueryDF)


    def display_dataframe_collection(self, df):
        # Set columns of QTable as DataFrame columns
        self.gui.collectionCardsTable.setColumnCount(len(df.columns))
        self.gui.collectionCardsTable.setHorizontalHeaderLabels(list(df.columns))

        for idx, row in df.iterrows():
            rowIdxQtable = self.gui.collectionCardsTable.rowCount()

            self.gui.collectionCardsTable.insertRow(rowIdxQtable)
            for iCol, cell in enumerate(list(row)):
                self.gui.collectionCardsTable.setItem(rowIdxQtable, iCol, QtWidgets.QTableWidgetItem(cell))

        self.gui.collectionCardsTable.resizeColumnsToContents()


        # tableWidget.setRowCount(len(data))

        # for i in range(0, len(data)):
        #     for j in range(0, len(data.columns)):
        #         item1 = str(data.iloc[i, j])
        #         tableWidget.setItem(i, j, QTableWidgetItem(item1))
        # return tableWidget




        # For each row in DataFrame add that row as new row to QTable





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