'''
TODO:
    * Functionality
        * Scryfall enable search using exact name. "!" suggested on their website does not work
    * Quality of life:
        * Proxies->Clear Selected - convert to DEL key
        * Implement Delete key for query results
        * Store most recent font size in a proxy file
'''


###############################
# Import system libraries
###############################
import os, sys, locale
import shutil
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
import src.lib.qt_helper as qt_helper
import src.lib.collection as collection
import src.lib.request_lib as request_lib
from src.lib.deck_lib import MagicDeck
import src.lib.proxy_lib as proxy_lib

#######################################
# Compile QT File
#######################################
os_lib.compile_form(os.path.join(thisdir, "MTG_GUI", 'mtg_ui.ui'))
os_lib.compile_form(os.path.join(thisdir, "MTG_GUI", 'new_deck.ui'))

from src.MTG_GUI.mtg_ui import Ui_MTG_UI
from src.MTG_GUI.new_deck import Ui_NewDeck

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
        self.dataDir = os.path.join(rootdir, "Data")
        self.decksDir = os.path.join(rootdir, "Decks")
        self.collectionDir = os.path.join(self.dataDir, "collection.h5")
        self.tmpFileName = os.path.join(self.decksDir, "tmpdeck.json")

        # Reacts
        self.gui.queryPushButton.clicked.connect(self.query_get)
        self.gui.queryAddCollectionPushButton.clicked.connect(self.update_collection)
        self.gui.mainTabWidget.currentChanged.connect(self.react_tab_change)
        self.gui.decksNewDeckPushButton.clicked.connect(self.new_deck_start_gui)
        self.gui.decksDecklistTable.cellDoubleClicked.connect(lambda iRow, iCol: self.load_deck_event(iRow, iCol))
        self.gui.collectionCardsTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.gui.collectionCardsTable.customContextMenuRequested.connect(self.collection_table_context_menu)
        # self.gui.proxyLoadLocalPushButton.clicked.connect(self.proxy_load_from_file)
        self.gui.proxyExportPDFPushButton.clicked.connect(self.proxy_export)
        self.gui.proxyClearPushButton.clicked.connect(self.proxy_clear_table)

        self.dialog.keyPressEvent = self.keyPressEvent

        self.gui.actionLoad_Local_Images.triggered.connect(self.proxy_load_from_file)
        self.gui.actionFrom_file.triggered.connect(self.collection_import_text)


    #############################
    #  Decks
    #############################

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

    def load_decks_list(self):
        # find all deck files under Decks folder
        decksPath = os.path.join(rootdir, "Decks")
        decksList = [f for f in os.listdir(decksPath) if os.path.isfile(os.path.join(decksPath, f))]
        decksDF = pd.DataFrame({"Decks" : decksList})

        qt_helper.qtable_load_from_pandas(self.gui.decksDecklistTable, decksDF)

    def load_deck_event(self, iRow, iCol):
        fileName = self.gui.decksDecklistTable.item(iRow, iCol).text()
        print(fileName)

    def refresh_decklist(self):
        pass

    #############################
    #  Queries and Collection
    #############################

    def query_get(self):
        txt = self.gui.queryLineEdit.text()
        queryDict = json.loads(txt)

        if self.gui.queryComboBox.currentText() == "Scryfall":
            df = request_lib.query_scryfall(queryDict)
            self.gui.responseTextEdit.append("Loaded query from Scryfall:" + str(queryDict))
        else:
            dfAll = collection.load_collection(self.collectionDir)
            df = collection.query_collection(dfAll, queryDict)
            self.gui.responseTextEdit.append("Loaded query from Local:" + str(queryDict))

        self.recentQueryDF = df
        self.display_collection(self.recentQueryDF)

    def update_collection(self):
        collection.update_collection(self.collectionDir, self.recentQueryDF)

    def display_collection(self, df):
        importantColumns = ['name', 'mana_cost', 'rarity', 'set', 'type_line']
        dfFilter = df[importantColumns]
        qt_helper.qtable_load_from_pandas(self.gui.collectionCardsTable, dfFilter)

    def react_tab_change(self, tabIdx):
        if tabIdx == 1:
            self.load_decks_list()

    def collection_table_context_menu(self, point):
        self._menu = QtWidgets.QMenu(self.gui.collectionCardsTable)
        actionAddToDeck = self._menu.addAction('Add to deck')
        actionAddToProxy = self._menu.addAction('Add to proxies')
        actionAddToDeck.triggered.connect(self.add_selected_cards_to_deck)
        actionAddToProxy.triggered.connect(self.proxy_add_from_collection)
        self._menu.popup(self.gui.collectionCardsTable.viewport().mapToGlobal(point))

    def collection_import_text(self):
        if hasattr(self, 'recentProxyDir'):
            thisPath = self.recentProxyDir
        else:
            thisPath = rootdir

        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.dialog, "Select proxy text file", thisPath, "*.txt", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if fname != "":
            self.recentProxyDir = os.path.dirname(fname)
            with open(fname, 'r') as f:
                lines = f.readlines()
                names = [' '.join(s.split(' ')[1 : -1]) for s in lines]

            rezDF = pd.DataFrame()
            for name in names:
                queryDict = {'name' : '!'+name}
                df = request_lib.query_scryfall(queryDict)
                rezDF = rezDF.append(df)
                self.gui.responseTextEdit.append("Loaded query from Scryfall:" + str(queryDict))

            self.recentQueryDF = rezDF
            self.display_collection(self.recentQueryDF)

    def add_selected_cards_to_deck(self):
        selectedRows = qt_helper.qtable_to_pandas(self.gui.collectionCardsTable, selected=True)
        selectedNames = list(selectedRows["name"])
        for name in selectedNames:
            self.currentDeckClass.add_card(name, "maindeck")

    #############################
    #  Proxies
    #############################

    def proxy_update_table(self, names, paths, origin):
        append = self.gui.proxyURLSTable.rowCount() != 0
        df = pd.DataFrame({'origin': [origin] * len(paths), 'name' : names, 'path': paths})
        qt_helper.qtable_load_from_pandas(self.gui.proxyURLSTable, df, append=append)

    def proxy_clear_table(self):
        qt_helper.qtable_delete_selected(self.gui.proxyURLSTable)

    def proxy_add_from_collection(self):
        selectedRows = qt_helper.qtable_to_pandas(self.gui.collectionCardsTable, selected=True)

        names = []
        urls = []
        for idx, row in selectedRows.iterrows():
            queryRows = collection.pd_query(self.recentQueryDF, {"name" : row["name"]})
            if len(queryRows) != 1:
                raise ValueError("Unexpected response", queryRows, "to query", dict(row))

            for idxQ, rowQ in queryRows.iterrows():
                names += [rowQ['name']]
                urls += [rowQ['image_uris']['large']]

        self.proxy_update_table(names, urls, "web")

    def proxy_load_from_file(self):
        if hasattr(self, 'recentProxyDir'):
            thisPath = self.recentProxyDir
        else:
            thisPath = rootdir

        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self.dialog, "Select proxy images", thisPath, "",
                                                        options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if len(paths) > 0:
            self.recentProxyDir = os.path.dirname(paths[0])
            names = [os.path.splitext(os.path.basename(path))[0] for path in paths]
            self.proxy_update_table(names, paths, "local")

    def proxy_export(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.dialog, "Save stacked proxies as...", rootdir, "",
                                                        options=QtWidgets.QFileDialog.DontUseNativeDialog)
        # Get rid of extension if any provided
        path = os.path.splitext(path)[0]

        # Load paper parameters from GUI
        paperSize = self.gui.proxyPaperSizeComboBox.currentText()
        paperOrientation = self.gui.proxyPaperOrientationComboBox.currentText()
        cardScale = self.gui.proxyScaleComboBox.currentText()
        cardScale = int(cardScale[:-1]) / 100.0

        df = qt_helper.qtable_to_pandas(self.gui.proxyURLSTable)
        imgs = proxy_lib.imgs_from_paths(df)
        proxy_lib.stack_imgs_pdf(imgs, path, paper=paperSize, orientation=paperOrientation, scale=cardScale)

    #############################
    #  Auxiliary
    #############################

    # React to key presses
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Plus or e.key() == QtCore.Qt.Key_Minus:
            self.fontsize += int(e.key() == QtCore.Qt.Key_Plus) - int(e.key() == QtCore.Qt.Key_Minus)
            self.updateSystemFontSize()

    def updateSystemFontSize(self):
        print("New font size", self.fontsize)
        self.gui.centralWidget.setStyleSheet("font-size: " + str(self.fontsize) + "pt;")
        self.gui.menuBar.setStyleSheet("font-size: " + str(self.fontsize) + "pt;")

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