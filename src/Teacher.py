
from PyQt6.QtWidgets import QPushButton, QTextEdit, QTableView, QMessageBox, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtSql import QSqlQueryModel, QSqlQuery


class Model(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refresh()

    def refresh(self):
        sql = '''
                    select id_teacher, fio, phone, email, comnt
                    from teachers
                '''
        self.setQuery(sql)


    def update(self, fio, phone, email, comnt, id_teacher):
        update_query = QSqlQuery()
        UPDATE = """
            update teachers set
                fio = :fio, 
                phone = :phone,
                email = :email,
                comnt = :comnt
            where id_teacher = :id_teacher ;
        """
        update_query.prepare(UPDATE)
        update_query.bindValue(':fio', fio)
        update_query.bindValue(':phone', phone)
        update_query.bindValue(':email', email)
        update_query.bindValue(':comnt', comnt)
        update_query.bindValue('id_teacher', id_teacher)
        ans = update_query.exec()
        print(ans, update_query.lastQuery())
        update_query.clear()
        self.refresh()

    def get_teacher(self, id_teacher):
        get_query = QSqlQuery()
        sql = '''
            select fio, phone, email, comnt
            from teachers where id_teacher = :id_teacher
        '''
        get_query.prepare(sql)
        get_query.bindValue(':id_teacher', id_teacher)
        get_query.exec()


    def add(self, fio, phone, email, comnt):
        add_query = QSqlQuery()
        INSERT = """
                    insert into teachers (fio, phone, email, comnt)
                    values (:fio, :phone, :email, :comnt);
                """
        add_query.prepare(INSERT)
        add_query.bindValue(':fio', fio)
        add_query.bindValue(':phone', phone)
        add_query.bindValue(':email', email)
        add_query.bindValue(':comnt', comnt)
        ans = add_query.exec()
        print(ans, add_query.lastQuery())
        add_query.clear()
        self.refresh()

class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)

    pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dialog = Dialog(parent=self)
        if dialog.exec():
            self.model().add(dialog.fio, dialog.phone, dialog.email, dialog.cmnt)

    pyqtSlot()
    def update(self):
        dialog = Dialog(parent=self)
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        dialog.fio, dialog.phone, dialog.email, dialog.cmnt = self.model().get_teacher(id_teacher)
        if dialog.exec():
            self.model().update(dialog.fio, dialog.phone, dialog.email, dialog.cmnt, id_teacher)

    pyqtSlot()
    def delete(self):
        QMessageBox.information(self, 'Учитель', 'Удаление')

class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Учитель')

        fio_lbl = QLabel('Фамилия И. О.', parent=self)
        self.__fio_edt = QLineEdit(parent=self)
        fio_lbl.setBuddy(self.__fio_edt)

        phone_lbl = QLabel('телефон', parent=self)
        self.__phone_edt = QLineEdit(parent=self)
        phone_lbl.setBuddy(self.__phone_edt)

        email_lbl = QLabel('e-mail', parent=self)
        self.__email_edt = QLineEdit(parent=self)
        email_lbl.setBuddy(self.__email_edt)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)
        comment_lbl.setBuddy(self.__comment_edt)

        ok_btn = QPushButton('Ok', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        cancel_btn.clicked.connect(self.reject)

        lay = QVBoxLayout()
        lay.addWidget(fio_lbl)
        lay.addWidget(self.__fio_edt)
        lay.addWidget(phone_lbl)
        lay.addWidget(self.__phone_edt)
        lay.addWidget(email_lbl)
        lay.addWidget(self.__email_edt)
        lay.addWidget(comment_lbl)
        lay.addWidget(self.__comment_edt)

        hlay = QHBoxLayout()
        hlay.addStretch()
        hlay.addWidget(ok_btn)
        hlay.addWidget(cancel_btn)
        lay.addLayout(hlay)

        self.setLayout(lay)

        ok_btn.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            return
        self.accept()


    @property
    def fio(self):
        result = self.__fio_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @fio.setter
    def fio(self, value):
        self.__fio_edt.setText(value)

    @property
    def phone(self):
        result = self.__phone_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @phone.setter
    def phone(self, value):
        self.__phone_edt.setText(value)

    @property
    def email(self):
        result = self.__email_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @email.setter
    def email(self, value):
        self.__email_edt.setText(value)

    @property
    def cmnt(self):
        result = self.__comment_edt.toPlainText().strip()
        if result == '':
            return None
        else:
            return result

    @cmnt.setter
    def cmnt(self, value):
        self.__comment_edt.setText(value)