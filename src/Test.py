

from PyQt6.QtWidgets import (
    QTableView, QMessageBox, QComboBox,
    QDialog, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton
)
from PyQt6.QtSql import QSqlTableModel, QSqlQuery, QSqlRecord
from PyQt6.QtCore import Qt, pyqtSlot

from src.Teacher import Dialog


class Model(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refresh()
        self.__authors = {}
        self.selectAuthors()
        # self.setTable('tests')
        # self.setEditStrategy(self.EditStrategy.OnManualSubmit)
        # self.select()
    @property
    def author_id(self, fio):
        return self.__authors[fio]

    def refresh(self):
        sql = """
            select t.id_test, t.tname, t.tcontent, a.fio from teats as t, teachers as a
            where t.teacher_id = a.id_teacher;
        """
        self.setQuery(sql)

    def add(self, tname, tcontent, teacher):
        add_query = QSqlQuery()
        teacher_id =self.author_id(teacher)
        INSERT = """
            insert into tests (tname, tcontent, teacher_id)
            values(:tname, :tcontent, :teacher_id);
        """
        add_query.prepare(INSERT)
        add_query.bindValue(':tname', tname)
        add_query.bindValue(':tcontent', tcontent)
        add_query.bindValue(':id_teacher', teacher_id)
        add_query.exec()
        self.refresh()

    def select_one(self, id_test):
        sql_query = QSqlQuery()
        SELECT_ONE = '''
            select tname, tcontent, teacher_id
            from tests
            where id_test = :id_test;
        '''
        sql_query.prepare(SELECT_ONE)
        sql_query.bindValue(':id_test', id_test)
        sql_query.exec()

    def update(self, tname, tcontent, teacher, id_test):
        upd_query = QSqlQuery()
        teacher_id = self.author_id(teacher)
        UPDATE = """
            update tests set
            tname = :tname,
            tcontent = :tcontent, 
            teacher_id = :teacher_id
            where id_test = :id_test
        """
        upd_query.prepare(UPDATE)
        upd_query.bindValue(':tname', tname)
        upd_query.bindValue(':tcontent', tcontent)
        upd_query.bindValue(':teacher_id', teacher_id)
        upd_query.bindValue(':id_test', id_test)
        upd_query.exec()
        self.refresh()

    def delete(self, id_test):
        sql_query = QSqlQuery()
        DELETE = """
            delete from tests where id_test = :id_test
        """
        sql_query.prepare(DELETE)
        sql_query.bindValue(':id_test', id_test)
        sql_query.exec()
        self.refresh()


    def selectAuthors(self):
        sql_query = QSqlQuery()
        SELECT = """
            select id_teacher, fio from teachers ; 
        """
        sql_query.exec(SELECT)
        if sql_query.isActive():
            sql_query.first()
            while sql_query.isValid():
                self.__authors[sql_query.value('fio')] = sql_query.value('id_teacher')
                sql_query.next()

class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(800)
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
        self.selectAuthors()
        self.setItemDelegateForColumn(3, ComboBoxDelegate(parent=self))

    def add(self):
        # self.model().insertRow(self.model().rowCount())
        dialog = Dialog(self)
        if dialog.exec():
            rec = self.conn.record('tests')
            rec.setValue('id_test', self.model().rowCount())
            rec.setValue('tname', dialog.tname)
            rec.setValue('tcontent', dialog.tcontent)
            rec.setValue('teacher_id', None if dialog.teacher =="" else self.__authors[dialog.teacher])
            self.model().select()


    def delete(self):
        ans = QMessageBox.question(self, 'Задача', 'Вы уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().removeRow(self.currentIndex().row())
            self.model().select()



    @property
    def authors(self):
        return self.__authors.keys()



