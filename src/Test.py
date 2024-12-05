from PyQt6.QtWidgets import (
    QTableView, QMessageBox, QComboBox,
    QDialog, QHBoxLayout, QVBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton
)
from PyQt6.QtSql import QSqlTableModel, QSqlQuery
from PyQt6.QtCore import Qt, pyqtSlot



class Model(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refresh()
        self.__authors = {}
        self.selectAuthors()

    @property
    def author_id(self, fio):
        return self.__authors[fio]

    @property
    def authors(self):
        return self.__authors.keys()

    def refresh(self):
        sql = """
            select t.id_test, t.tname, t.tcontent,
            a.fio from teats as t, teachers as a
            where t.teacher_id = a.id_teacher
            union
            select id_test, tname, tcontent, ''
            from tests where teacher_id is null;
        """
        self.setQuery(sql)

    def add(self, tname, tcontent, teacher):
        add_query = QSqlQuery()
        teacher_id = None if (teacher == "") else self.author_id(teacher)
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
        if sql_query.isActive():
            sql_query.first()
            return (sql_query.value('tname'),
                    sql_query.value('tcontent'),
                    sql_query.value('teacher'))

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

    @pyqtSlot()
    def add(self):
        dialog = Dialog(self)
        if dialog.exec():
            self.model().add(dialog.tname, dialog.tcontent, dialog.teacher)

    def delete(self):
        ans = QMessageBox.question(self, 'Задача', 'Вы уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().removeRow(self.currentIndex().row())
            self.model().select()

    @property
    def authors(self):
        self.model().selectAuthors()
        return self.model().authors()

class Dialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Задача')

        tname_lbl = QLabel('&Название', parent=self)
        self.__tname_edit = QLineEdit(parent=self)
        tname_lbl.setBuddy(self.__tname_edit)

        tcontent_lbl = QLabel('&Содержание', parent=self)
        self.__tcontent_edit = QTextEdit(parent=self)
        tcontent_lbl.setBuddy(self.__tcontent_edit)

        teacher_lbl = QLabel('&Автор', parent=self)
        self.__teacher_cmb = QComboBox(parent=self)
        teacher_lbl.setBuddy(self.__teacher_cmb)
        self.__teacher_cmb.addItem("")
        self.__teacher_cmb.addItems(parent.authors)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.addWidget(tname_lbl)
        lay.addWidget(self.__tname_edit)
        lay.addWidget(tcontent_lbl)
        lay.addWidget(self.__tcontent_edit)
        lay.addWidget(teacher_lbl)
        lay.addWidget(self.__teacher_cmb)

        hlay = QHBoxLayout()
        hlay.addStretch()
        hlay.addWidget(ok_btn)
        hlay.addWidget(cancel_btn)
        lay.addLayout(hlay)
        self.setLayout(lay)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.tcontent is None:
            return
        self.accept()

    @property
    def tname(self):
        result = self.__tname_edit.text().strip()
        if result == '':
            return None
        return result

    @tname.setter
    def tname(self, value):
        self.__tname_edit.setText(value)

    @property
    def tcontent(self):
        result = self.__tcontent_edit.toPlainText().strip()
        if result == '':
            return None
        return result

    @tcontent.setter
    def tcontent(self, value):
        self.__tcontent_edit.setPlainText(value)

    @property
    def teacher(self):
        return self.__teacher_cmb.currentText()

    @teacher.setter
    def teacher(self, value):
        self.__teacher_cmb.setCurrentText(value)



