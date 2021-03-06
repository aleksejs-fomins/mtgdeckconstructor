# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/alyosha/work/git/mtgdeckconstructor/src/MTG_GUI/mtg_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MTG_UI(object):
    def setupUi(self, MTG_UI):
        MTG_UI.setObjectName("MTG_UI")
        MTG_UI.resize(944, 718)
        self.centralWidget = QtWidgets.QWidget(MTG_UI)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainTabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.mainTabWidget.setObjectName("mainTabWidget")
        self.collectionTab = QtWidgets.QWidget()
        self.collectionTab.setObjectName("collectionTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.collectionTab)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.collectionCardsTable = QtWidgets.QTableWidget(self.collectionTab)
        self.collectionCardsTable.setObjectName("collectionCardsTable")
        self.collectionCardsTable.setColumnCount(0)
        self.collectionCardsTable.setRowCount(0)
        self.collectionCardsTable.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.collectionCardsTable)
        self.mainTabWidget.addTab(self.collectionTab, "")
        self.decksTab = QtWidgets.QWidget()
        self.decksTab.setObjectName("decksTab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.decksTab)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.decksControlLayout = QtWidgets.QVBoxLayout()
        self.decksControlLayout.setSpacing(6)
        self.decksControlLayout.setObjectName("decksControlLayout")
        self.decksFormatComboBox = QtWidgets.QComboBox(self.decksTab)
        self.decksFormatComboBox.setObjectName("decksFormatComboBox")
        self.decksFormatComboBox.addItem("")
        self.decksFormatComboBox.addItem("")
        self.decksFormatComboBox.addItem("")
        self.decksControlLayout.addWidget(self.decksFormatComboBox)
        self.decksDecklistTable = QtWidgets.QTableWidget(self.decksTab)
        self.decksDecklistTable.setShowGrid(False)
        self.decksDecklistTable.setObjectName("decksDecklistTable")
        self.decksDecklistTable.setColumnCount(0)
        self.decksDecklistTable.setRowCount(0)
        self.decksDecklistTable.horizontalHeader().setVisible(False)
        self.decksDecklistTable.verticalHeader().setVisible(False)
        self.decksControlLayout.addWidget(self.decksDecklistTable)
        self.decksNewDeckPushButton = QtWidgets.QPushButton(self.decksTab)
        self.decksNewDeckPushButton.setObjectName("decksNewDeckPushButton")
        self.decksControlLayout.addWidget(self.decksNewDeckPushButton)
        self.decksZoneComboBox = QtWidgets.QComboBox(self.decksTab)
        self.decksZoneComboBox.setObjectName("decksZoneComboBox")
        self.decksControlLayout.addWidget(self.decksZoneComboBox)
        self.decksCardImageFrame = QtWidgets.QFrame(self.decksTab)
        self.decksCardImageFrame.setMinimumSize(QtCore.QSize(0, 300))
        self.decksCardImageFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.decksCardImageFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.decksCardImageFrame.setObjectName("decksCardImageFrame")
        self.decksControlLayout.addWidget(self.decksCardImageFrame)
        self.horizontalLayout.addLayout(self.decksControlLayout)
        self.decksCardsTable = QtWidgets.QTableWidget(self.decksTab)
        self.decksCardsTable.setMinimumSize(QtCore.QSize(600, 0))
        self.decksCardsTable.setObjectName("decksCardsTable")
        self.decksCardsTable.setColumnCount(0)
        self.decksCardsTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.decksCardsTable)
        self.mainTabWidget.addTab(self.decksTab, "")
        self.proxyTab = QtWidgets.QWidget()
        self.proxyTab.setObjectName("proxyTab")
        self.mainTabWidget.addTab(self.proxyTab, "")
        self.Scryfall = QtWidgets.QWidget()
        self.Scryfall.setObjectName("Scryfall")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Scryfall)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.queryLineEdit = QtWidgets.QLineEdit(self.Scryfall)
        self.queryLineEdit.setObjectName("queryLineEdit")
        self.verticalLayout_2.addWidget(self.queryLineEdit)
        self.queryPushButton = QtWidgets.QPushButton(self.Scryfall)
        self.queryPushButton.setObjectName("queryPushButton")
        self.verticalLayout_2.addWidget(self.queryPushButton)
        self.responseTextEdit = QtWidgets.QTextEdit(self.Scryfall)
        self.responseTextEdit.setObjectName("responseTextEdit")
        self.verticalLayout_2.addWidget(self.responseTextEdit)
        self.queryAddCollectionPushButton = QtWidgets.QPushButton(self.Scryfall)
        self.queryAddCollectionPushButton.setObjectName("queryAddCollectionPushButton")
        self.verticalLayout_2.addWidget(self.queryAddCollectionPushButton)
        self.mainTabWidget.addTab(self.Scryfall, "")
        self.verticalLayout.addWidget(self.mainTabWidget)
        MTG_UI.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MTG_UI)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 944, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        MTG_UI.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MTG_UI)
        self.mainToolBar.setObjectName("mainToolBar")
        MTG_UI.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MTG_UI)
        self.statusBar.setObjectName("statusBar")
        MTG_UI.setStatusBar(self.statusBar)
        self.actionNew_Standar_Deck = QtWidgets.QAction(MTG_UI)
        self.actionNew_Standar_Deck.setObjectName("actionNew_Standar_Deck")
        self.actionCommander_Deck = QtWidgets.QAction(MTG_UI)
        self.actionCommander_Deck.setObjectName("actionCommander_Deck")
        self.actionNewDeck = QtWidgets.QAction(MTG_UI)
        self.actionNewDeck.setObjectName("actionNewDeck")
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MTG_UI)
        self.mainTabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MTG_UI)

    def retranslateUi(self, MTG_UI):
        _translate = QtCore.QCoreApplication.translate
        MTG_UI.setWindowTitle(_translate("MTG_UI", "MTG_UI"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.collectionTab), _translate("MTG_UI", "Collection"))
        self.decksFormatComboBox.setItemText(0, _translate("MTG_UI", "---Select Deck Type---"))
        self.decksFormatComboBox.setItemText(1, _translate("MTG_UI", "Standard"))
        self.decksFormatComboBox.setItemText(2, _translate("MTG_UI", "Commander"))
        self.decksNewDeckPushButton.setText(_translate("MTG_UI", "New Deck"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.decksTab), _translate("MTG_UI", "Decks"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.proxyTab), _translate("MTG_UI", "Proxy PDF"))
        self.queryLineEdit.setText(_translate("MTG_UI", "{\"set\" : \"c20\", \"type\" : \"human\"}"))
        self.queryPushButton.setText(_translate("MTG_UI", "Query"))
        self.queryAddCollectionPushButton.setText(_translate("MTG_UI", "Add To Collection"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.Scryfall), _translate("MTG_UI", "Scryfall"))
        self.menuFile.setTitle(_translate("MTG_UI", "File"))
        self.menuEdit.setTitle(_translate("MTG_UI", "Edit"))
        self.actionNew_Standar_Deck.setText(_translate("MTG_UI", "Standar Deck"))
        self.actionCommander_Deck.setText(_translate("MTG_UI", "Commander Deck"))
        self.actionNewDeck.setText(_translate("MTG_UI", "New Deck"))
