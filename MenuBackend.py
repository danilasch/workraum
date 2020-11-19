import sys
import sqlite3

import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QMessageBox

from MainMenu import Ui_MainMenu
from StudyMenu import Ui_StudyMenu
from ManagementMenu import Ui_ManageWindow

from NotesWindow import Ui_NotesWindow
from NoteWindow import Ui_NoteWindow

from bin.GraphsWindow import Ui_BaseWindow


def create_main_window():
    global app, ex
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())


def show_main_window():
    ex.show()


def show_management():
    ex.show_management()


def update_list():
    ex.update_list()


class MainMenu(QMainWindow, Ui_MainMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.studyName.mousePressEvent = self.open_study
        self.studyOption.mousePressEvent = self.open_study
        self.managementName.mousePressEvent = self.open_management
        self.managementName.mousePressEvent = self.open_management

    def open_study(self, event):
        study = StudyMenu()
        study.show()
        self.hide()

    def open_management(self, event):
        self.manage = ManagementMenu()
        self.manage.show()
        self.hide()

    def update_list(self):
        self.manage.notes.update_list()

    def show_management(self):
        self.manage.show()


class StudyMenu(QMainWindow, Ui_StudyMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphsName.mousePressEvent = self.open_graph
        # self.graphsOption.mousePressEvent = self.open_graph

        self.goBackButton.mousePressEvent = self.go_back

    # def open_graph(self, event):
    #     graph = GraphsWidget()
    #     graph.show()

    def go_back(self, event):
        show_main_window()
        self.hide()


class ManagementMenu(QMainWindow, Ui_ManageWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.notesName.mousePressEvent = self.open_notes
        self.notesOption.mousePressEvent = self.open_notes

        self.todoName.mousePressEvent = self.open_todo
        self.todoName.mousePressEvent = self.open_todo

        self.goBackButton.mousePressEvent = self.go_back

    def open_notes(self, event):
        self.notes = NotesWindow()
        self.notes.show()
        self.hide()

    def open_todo(self, event):
        pass
        # study = StudyMenu()
        # study.show()
        # self.hide()

    def go_back(self, event):
        show_main_window()
        self.hide()


class NotesWindow(QMainWindow, Ui_NotesWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.con = sqlite3.connect("notes_db.sqlite")

        self.goBackButton.mousePressEvent = self.back

        self.addButton.mousePressEvent = self.add_note
        self.removeButton.mousePressEvent = self.remove_note
        self.exportButton.mousePressEvent = self.export_note
        self.listWidget.itemDoubleClicked.connect(self.note_clicked)

        self.elements_dictionary = {}
        self.update_list()
        # ключ - номер в строчки в QListWidget, значение - id стикера

    def back(self, event):
        # возвращение в меню заметок
        show_management()
        self.hide()

    def add_note(self, event):  # добавляем стикер
        # подготавливаем id для нового стикера
        if self.elements_dictionary:
            max_id = max(self.elements_dictionary.values())

        else:
            max_id = 0

        # открываем окно для создания стикера и помечаем её как новую
        note = NoteWindow(max_id + 1, True)
        note.show()

    def remove_note(self, event):
        # удаляем стикер

        list_items = [x.row() for x in self.listWidget.selectedIndexes()]

        if not list_items:
            return None

        qm = QMessageBox
        qm.question(self, '',
                    "Вы действительно хотите удалить выделенные стикеры?",
                    qm.Yes | qm.No)

        if qm.Yes:  # необходимо подтвердить удаление
            ids = [self.elements_dictionary[i] for i in list_items]
            cur = self.con.cursor()
            cur.execute("DELETE FROM notes WHERE id in (" + ", ".join(
                        '?' * len(ids)) + ")", ids)
            self.con.commit()
            self.update_list()

        else:
            qm.close(self)

    def export_note(self, event):  # экспортируем выбраный стикер в файл .txt
        cur = self.con.cursor()
        fname = QFileDialog.getSaveFileName(
            self, 'Сохранить в текстовый документ', '/',
            'Текстовый документ (*.txt)')[0]

        file = open(fname, 'w')
        text = cur.execute(
            "SELECT text FROM notes WHERE id = ?",
            (self.elements_dictionary[self.listWidget.selectedIndexes()[0].row()],)).fetchone()[0]
        file.write(text)
        file.close()

    def update_list(self):
        self.listWidget.clear()  # очищаем список стикеров, чтобы заполинть его
        cur = self.con.cursor()
        # собираем данные из обновленной БД
        ids = cur.execute("SELECT id FROM notes").fetchall()
        names = cur.execute("SELECT name FROM notes").fetchall()

        for i, (note_id, note_name) in enumerate(zip(ids, names)):
            self.elements_dictionary[i] = note_id[0]  # актуализируем словарь

            #  обновляем список стикеров
            self.listWidget.addItem(QListWidgetItem(str(note_name[0])))

    def note_clicked(self):  # пользователь решил отредактировать стикер
        # находим id стикера по её порядковому номеру
        note_id = self.elements_dictionary[self.listWidget.currentRow()]

        # открываем окно для редактирования стикера и помечаем её как не новую
        note = NoteWindow(note_id, False)
        note.show()


class NoteWindow(QMainWindow, Ui_NoteWindow):
    def __init__(self, note_id, is_new_note):
        super().__init__()
        self.setupUi(self)
        self.id = note_id

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self._drag_active = False  # флаг для drag and drop стикера

        self.con = sqlite3.connect("notes_db.sqlite")

        if not is_new_note:  # редактируем уже имеющийся стикер
            cur = self.con.cursor()
            self.nameInput.setText(cur.execute("SELECT name FROM notes WHERE id=?",
                                               (note_id, )).fetchone()[0])

            self.textEdit.setText(cur.execute(
                "SELECT text FROM notes WHERE id=?", (note_id, )).fetchone()[0])
            self.closeButton.mousePressEvent = self.edit_note

        else:  # создаём новый стикер
            self.nameInput.setText("Новый стикер")

            cur = self.con.cursor()
            cur.execute("INSERT INTO notes(id, name, text) VALUES(?, ?, ?)",
                        (self.id, self.nameInput.text(), self.textEdit.toPlainText()))
            self.con.commit()

            # закрепляем за стикером статус уже существующей
            self.closeButton.mousePressEvent = self.edit_note

            update_list()

    def mousePressEvent(self, e):  # метод для drag and drop: запоминаем изначальную позицию
        self.previous_pos = e.globalPos()

    def mouseMoveEvent(self, e):  # метод для drag and drop: меняем позицию стикера
        delta = e.globalPos() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPos()

        self._drag_active = True

    def mouseReleaseEvent(self, e):
        if self._drag_active:
            self._drag_active = False

    # def new_note(self, event):
    #     #  актуализируем информацию в БД
    #     cur = self.con.cursor()
    #     cur.execute("INSERT INTO notes(id, name, text) VALUES(?, ?, ?)",
    #                 (self.id, self.nameInput.text(), self.textEdit.toPlainText()))
    #     self.con.commit()
    #
    #     # закрепляем за стикером статус уже существующей
    #     self.closeButton.mousePressEvent = self.edit_note
    #
    #     update_list()  # обновляем графическое представление БД
    #     self.close()

    def edit_note(self, event):
        cur = self.con.cursor()

        cur.execute('''UPDATE notes
SET name = ?, text = ?
WHERE id = ?''', (self.nameInput.text(), self.textEdit.toPlainText(), self.id))
        self.con.commit()

        update_list()  # обновляем графическое представление БД
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())
