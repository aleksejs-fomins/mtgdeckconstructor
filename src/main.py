###############################
# Import system libraries
###############################
import os, sys, locale
import shutil
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
# Import local libraries
#######################################

import src.lib.os_lib as os_lib
from src.lib.deck_lib import MagicDeck

from src.MTG_GUI.mtg_ui import Ui_MTG_UI
from src.MTG_GUI.new_deck import Ui_NewDeck

#######################################
# Compile QT File
#######################################
os_lib.compile_form(os.path.join(thisdir, "MTG_GUI", 'mtg_ui.ui'))
os_lib.compile_form(os.path.join(thisdir, "MTG_GUI", 'new_deck.ui'))

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

        # Variables
        self.decksDir = os.path.join(rootdir, "Decks")
        self.tmpFileName = os.path.join(self.decksDir, "tmpdeck.json")

        # Reacts
        self.gui.queryPushButton.clicked.connect(self.get_query)
        self.gui.queryAddCollectionPushButton.clicked.connect(self.query_add_to_collection)
        self.gui.mainTabWidget.currentChanged.connect(self.react_tab_change)
        self.gui.decksNewDeckPushButton.clicked.connect(self.new_deck_start_gui)

    def new_deck_start_gui(self):
        # Init
        self.newDeckDialog = QtWidgets.QWidget()
        self.newDeckDialog.show()
        self.newDeckGUI = Ui_NewDeck()
        self.newDeckGUI.setupUi(self.newDeckDialog)

        # Actions:
        self.newDeckGUI.newDeckDuplicatePushButton.clicked.connect(self.import_deck)
        self.newDeckGUI.newDeckCancelPushButton.clicked.connect(self.newDeckDialog.close)
        self.newDeckGUI.newDeckOkPushButton.clicked.connect(self.new_deck)

    def new_deck(self):
        deckName = self.newDeckGUI.newDeckNameLineEdit.text()
        format = self.newDeckGUI.newDeckTypeComboBox.currentText()
        importFilePath = self.newDeckGUI.newDeckDuplicateLineEdit.text()
        if importFilePath != "":
            shutil.copyfile(importFilePath, self.tmpFileName)
            self.currentDeckClass = MagicDeck(deckName, format, self.tmpFileName, importDeck=True)
        else:
            self.currentDeckClass = MagicDeck(deckName, format, self.tmpFileName, importDeck=False)

        self.newDeckDialog.close()


    def import_deck(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self.newDeckDialog, "Choose Deck to import", rootdir, "Deck Files (*.json)", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        self.newDeckGUI.newDeckDuplicateLineEdit.setText(path)

    # def save_deck_as(self):
    #     path, _ = QtWidgets.QFileDialog.getSaveFileName(self.newDeckDialog, "Save new deck as", rootdir,
    #                                                     "Deck Files (*.json)",
    #                                                     options=QtWidgets.QFileDialog.DontUseNativeDialog)



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


    def react_tab_change(self, tabIdx):
        if (tabIdx == 1):
            self.loadDecksList()


    def loadDecksList(self):
        # lear current content of table
        self.gui.decksDecklistTable.setRowCount(0)
        self.gui.decksDecklistTable.setColumnCount(1)

        # find all deck files under Decks folder
        decksPath = os.path.join(rootdir, "Decks")
        decksList = [f for f in os.listdir(decksPath) if os.path.isfile(os.path.join(decksPath, f))]

        # display list of decks in Decks table
        for deck in decksList:
            currentTableRowIndex = self.gui.decksDecklistTable.rowCount()
            self.gui.decksDecklistTable.insertRow(currentTableRowIndex)
            self.gui.decksDecklistTable.setItem(currentTableRowIndex, 0, QtWidgets.QTableWidgetItem(deck))

        self.gui.decksDecklistTable.resizeColumnsToContents()



        #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        # When the Decks tab is selected load the list of decks stored locally on the drive



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