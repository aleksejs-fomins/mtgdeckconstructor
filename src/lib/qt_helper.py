import pandas as pd
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets


def qtable_get_horizontal_header(qtable):
    nColumn = qtable.columnCount()
    return [qtable.horizontalHeaderItem(i).text() for i in range(nColumn)]


def qtable_to_pandas(qtable, selected=False):
    '''
    :param qtable:       QTableWidget object
    :param selected:     Only return selected rows. If False, return whole table
    :return:             Pandas DataFrame corresponding to the QTable
    '''

    nRows = qtable.rowCount()
    nColumns = qtable.columnCount()
    columns = qtable_get_horizontal_header(qtable)

    if selected:
        items = qtable.selectedItems()
        textLst1D = [item.text() for item in items]
        textArr2D = np.array(textLst1D).reshape((len(textLst1D) // nColumns, nColumns))
        return pd.DataFrame(textArr2D, columns=columns)
    else:
        df = pd.DataFrame(columns=columns, index=range(nRows))
        for i in range(nRows):
            for j in range(nColumns):
                df.ix[i, j] = qtable.item(i, j).text()
        return df


def qtable_delete_selected(qtable):
    rowIdxs = [idx.row() for idx in qtable.selectionModel().selectedRows()]
    rowIdxsReverse = sorted(rowIdxs)[::-1]

    for idx in rowIdxsReverse:
        qtable.removeRow(idx)


def qtable_load_from_pandas(qtable, df, append=False):
    if not append:
        # self.gui.collectionCardsTable.clear()
        qtable.setRowCount(0)

        # Set columns of QTable as DataFrame columns
        qtable.setColumnCount(len(df.columns))
        qtable.setHorizontalHeaderLabels(list(df.columns))

    for idx, row in df.iterrows():
        rowIdxQtable = qtable.rowCount()

        qtable.insertRow(rowIdxQtable)
        for iCol, cell in enumerate(list(row)):
            qtable.setItem(rowIdxQtable, iCol, QtWidgets.QTableWidgetItem(cell))

    qtable.resizeColumnsToContents()
