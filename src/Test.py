from PyQt6.QtWidgets import (
    QTableView, QMessageBox, QComboBox,
    QDialog, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton
)
from PyQt6.QtSql import QSqlTableModel, QSqlQuery, QSqlRecord
from PyQt6.QtCore import Qt, pyqtSlot

class Model(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTable('tests')
        self.setEditStrategy(self.EditStrategy.OnManualSubmit)
        self.select()


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(800)
        # self.conn = conn
        model = Model(parent=self)
        self.setModel(model)
        model.setHeaderData(1, Qt.Orientation.Horizontal, "Название")
        model.setHeaderData(2, Qt.Orientation.Horizontal, "Содержание")
        model.setHeaderData(3, Qt.Orientation.Horizontal, "Автор")
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        #self.hideColumn(0)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.ResizeMode.Fixed)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, hh.ResizeMode.Stretch)
        # self.selectAuthors()

    def add(self):
        self.model().insertRow(self.model().rowCount())


    def delete(self):
        self.model().removeRow(self.currentIndex().row())
        self.model().select()


