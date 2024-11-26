from PyQt6.QtWidgets import QMenuBar

class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        help_menu = self.addMenu('Справка')

        teacher_menu = self.addMenu('Учитель')


        self.__about = help_menu.addAction('О программе ...')
        self.__about_qt = help_menu.addAction('О библиотеке Qt...')
        self.__teacher_add = teacher_menu.addAction('Добавить')
        self.__teacher_update = teacher_menu.addAction('Редактировать')
        self.__teacher_delete = teacher_menu.addAction('Удалить')

    @property
    def about(self):
        return self.__about

    @property
    def about_qt(self):
        return self.__about_qt

    @property
    def teacher_add(self):
        return self.__teacher_add

    @property
    def teacher_update(self):
        return self.__teacher_update

    @property
    def teacher_delete(self):
        return self.__teacher_delete