import sys
import sqlite3

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QMessageBox

from BaseWindowClass import BaseWindow

from NotesWindow import Ui_NotesWindow
from NoteWindow import Ui_NoteWindow
from ToDoMenu import Ui_ToDoMenu


# def create_main_window():
#     global app, ex
#     app = QApplication(sys.argv)
#     ex = MainMenu()
#     ex.show()
#     sys.exit(app.exec())


def switch_to_notes():
    notes.show()
    notes.setGeometry(todo.geometry())
    todo.hide()


def switch_to_todo():
    todo.show()
    todo.setGeometry(notes.geometry())
    notes.hide()


def update_list():
    notes.update_list()


class NotesWindow(BaseWindow, Ui_NotesWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.titleBar, self.closeButton = self.titleBar, self.closeButton

        self.con = sqlite3.connect("notes_db.sqlite")

        # свернуть и закрыть - функции кнопок верхней панели
        self.closeButton.clicked.connect(self.close)
        # self.closeButton.mouseMoveEvent = self.closeButton.setStyleSheet("background-color: red")
        self.hideButton.clicked.connect(self.showMinimized)
        self.titleBar.mousePressEvent = self.titleBarMousePressEvent

        # события для кнопок слева
        self.goToToDo.mousePressEvent = self.switch_to_todo
        self.addButton.mousePressEvent = self.add_note
        self.removeButton.mousePressEvent = self.remove_note
        self.exportButton.mousePressEvent = self.export_note
        self.listWidget.itemDoubleClicked.connect(self.note_clicked)
        # ToDo сделать кнопку помощи

        self.elements_dictionary = {}
        self.update_list()
        # ключ - номер в строчки в QListWidget, значение - id стикера

    def switch_to_todo(self, event):
        switch_to_todo()

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

        qm = QMessageBox()

        qm.setWindowTitle('Подтверждение удаления')
        qm.setText('Вы действительно хотите удалить выделенные стикеры?')
        qm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        qm.setStyleSheet("background-color: rgb(23, 28, 37); color: rgb(255, 255, 255)")
        button_yes = qm.button(QMessageBox.Yes)
        button_yes.setText('Да')
        button_no = qm.button(QMessageBox.No)
        button_no.setText('Нет')
        qm.exec_()

        if qm.clickedButton() == button_yes:  # необходимо подтвердить удаление
            note_id = self.elements_dictionary[list_items[0]]
            cur = self.con.cursor()
            cur.execute("DELETE FROM notes WHERE id = ?", (note_id, ))
            self.con.commit()
            self.update_list()

        else:
            qm.close()

    def export_note(self, event):  # экспортируем выбраный стикер в файл .txt
        file_name = QFileDialog.getSaveFileName(
            self, 'Сохранить в текстовый документ', '/',
            'Текстовый документ (*.txt)')[0]
        if file_name:
            cur = self.con.cursor()
            file = open(file_name, 'w')
            text = cur.execute(
                "SELECT text FROM notes WHERE id = ?",
                (self.elements_dictionary[self.listWidget.selectedIndexes()[0].row()],)).fetchone()[
                0]
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
        self.spacer.mousePressEvent = self.spacerMousePressEvent

        self.con = sqlite3.connect("notes_db.sqlite")

        if not is_new_note:  # редактируем уже имеющийся стикер
            cur = self.con.cursor()
            self.nameInput.setText(cur.execute("SELECT name FROM notes WHERE id = ?",
                                               (note_id,)).fetchone()[0])

            self.textEdit.setText(cur.execute(
                "SELECT text FROM notes WHERE id=?", (note_id,)).fetchone()[0])
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

    def spacerMousePressEvent(self, e):  # метод для drag and drop: запоминаем изначальную позицию
        self.previous_pos = e.globalPos()
        self._drag_active = True

    def mouseMoveEvent(self, e):  # метод для drag and drop: меняем позицию стикера
        if self._drag_active:
            delta = e.globalPos() - self.previous_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.previous_pos = e.globalPos()


    def mouseReleaseEvent(self, e):
        if self._drag_active:
            self._drag_active = False

    def edit_note(self, event):
        cur = self.con.cursor()

        cur.execute('''UPDATE notes
SET name = ?, text = ?
WHERE id = ?''', (self.nameInput.text(), self.textEdit.toPlainText(), self.id))
        self.con.commit()

        update_list()  # обновляем графическое представление БД
        self.close()


class ToDoMenu(BaseWindow, Ui_ToDoMenu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.titleBar, self.closeButton = self.titleBar, self.closeButton

        self.con = sqlite3.connect("notes_db.sqlite")

        # свернуть и закрыть - функции кнопок верхней панели
        self.closeButton.clicked.connect(self.close)
        # self.closeButton.mouseHoverEvent = self.closeButton.setStyleSheet("background-color: red")
        self.hideButton.clicked.connect(self.showMinimized)
        self.titleBar.mousePressEvent = self.titleBarMousePressEvent

        # события для кнопок слева
        self.goToNotes.mousePressEvent = self.switch_to_notes
        self.addButton.mousePressEvent = self.add_todo
        self.removeButton.mousePressEvent = self.remove_todo
        self.exportButton.mousePressEvent = self.export_todo
        self.listWidget.itemDoubleClicked.connect(self.todo_clicked)
        self.calendarButton.mousePressEvent = self.open_calender
        self.settingsButton.mousePressEvent = self.open_settings
        # ToDo сделать кнопку помощи

        # self.elements_dictionary = {}
        # self.update_list()
        # ключ - номер в строчки в QListWidget, значение - id стикера

    def switch_to_notes(self, event):
        switch_to_notes()

    def add_todo(self, event):
        pass

    def remove_todo(self, event):
        pass

    def export_todo(self, event):
        pass

    def todo_clicked(self):
        pass

    def open_calender(self, event):
        pass

    def open_settings(self, event):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notes = NotesWindow()
    todo = ToDoMenu()
    notes.show()
    sys.exit(app.exec())
