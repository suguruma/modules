from PyQt5.QtCore import (Qt, QModelIndex, QAbstractItemModel)
from PyQt5.QtWidgets import (QTreeView, QAbstractItemView)

class Model(QAbstractItemModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = []
        self.headers = []

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.items[index.row()][index.column()]
            except:
                return
        return

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]

    def removeRows(self, rowIndexes):
        for row in sorted(rowIndexes, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row + 1)
            del self.items[row]
            self.endRemoveRows()

    def flags(self, index):
        return super(Model, self).flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.items[index.row()][index.column()] = value
            return True
        return False

    def addRow(self, no, id, posX, posY):
        self.beginInsertRows(QModelIndex(), len(self.items), 1)
        self.items.append([no, id, posX, posY])
        self.endInsertRows()

    def itemsClear(self):
        self.items = []

    def setHeaders(self, _headers):
        self.headers = _headers

class View(QTreeView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setItemsExpandable(False)
        self.setIndentation(0)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def drawBranches(self, painter, rect, index):
        return
