import sys
import sqlite3
import datetime as dt

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QMessageBox

from BaseWindowClass import BaseWindow

from NotesWindow import Ui_NotesWindow
from NoteWindow import Ui_NoteWindow
from ToDoMenu import Ui_ToDoMenu
from ToDoWindow import Ui_ToDoWindow


# def create_main_window():
#     global app, ex
#     app = QApplication(sys.argv)
#     ex = MainMenu()
#     ex.show()
#     sys.exit(app.exec())


def switch_to_notes():
    notes.show()
    notes.setGeometry(todos.geometry())
    todos.hide()


def switch_to_todo():
    todos.show()
    todos.setGeometry(notes.geometry())
    notes.hide()


def update_notes_list():
    notes.update_list()


def update_todo_list():
    todos.update_table()


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
        qm.setText('Вы действительно хотите удалить выделенный стикер?')
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
        self.drag_active = False  # флаг для drag and drop стикера
        self.spacer.mousePressEvent = self.spacerMousePressEvent

        self.closeButton.mousePressEvent = self.edit_note

        self.con = sqlite3.connect("notes_db.sqlite")
        cur = self.con.cursor()

        if not is_new_note:  # редактируем уже имеющийся стикер

            self.nameInput.setText(cur.execute(
                "SELECT name FROM notes WHERE id = ?", (note_id,)).fetchone()[0])

            self.textEdit.setText(cur.execute(
                "SELECT text FROM notes WHERE id=?", (note_id,)).fetchone()[0])

        else:  # создаём новый стикер
            self.nameInput.setText("Новый стикер")

            cur.execute("INSERT INTO notes(id, name, text) VALUES(?, ?, ?)",
                        (self.id, self.nameInput.text(), self.textEdit.toPlainText()))
            self.con.commit()

            update_notes_list()

    def spacerMousePressEvent(self, e):  # метод для drag and drop: запоминаем изначальную позицию
        self.previous_pos = e.globalPos()
        self.drag_active = True

    def mouseMoveEvent(self, e):  # метод для drag and drop: меняем позицию стикера
        if self.drag_active:
            delta = e.globalPos() - self.previous_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.previous_pos = e.globalPos()


    def mouseReleaseEvent(self, e):
        if self.drag_active:
            self.drag_active = False

    def edit_note(self, event):
        cur = self.con.cursor()

        cur.execute('''UPDATE notes
SET name = ?, text = ?
WHERE id = ?''', (self.nameInput.text(), self.textEdit.toPlainText(), self.id))
        self.con.commit()

        update_notes_list()  # обновляем графическое представление БД
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
        self.tableWidget.itemClicked.connect(self.todo_clicked)
        self.tableWidget.itemDoubleClicked.connect(self.todo_double_clicked)
        self.calendarButton.mousePressEvent = self.open_calender
        self.settingsButton.mousePressEvent = self.open_settings
        # ToDo сделать кнопку помощи

        self.elements_dictionary = {}
        # ключ - номер в строчки в QTableWidget, значение - id стикера
        self.tableWidget.setColumnWidth(1, 10)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.update_table()

    def switch_to_notes(self, event):
        switch_to_notes()

    def add_todo(self, event):
        if self.elements_dictionary:
            max_id = max(self.elements_dictionary.values())
        else:
            max_id = 0

        # открываем окно для создания плана
        todo = ToDoWindow(max_id + 1, True)
        todo.show()

    def remove_todo(self, event):
        # удаляем стикер

        list_items = [x.row() for x in self.tableWidget.selectedIndexes()]

        if not list_items:
            return None

        qm = QMessageBox()

        qm.setWindowTitle('Подтверждение удаления')
        qm.setText('Вы действительно хотите удалить выделенный план?')
        qm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        qm.setStyleSheet("background-color: rgb(23, 28, 37); color: rgb(255, 255, 255)")
        button_yes = qm.button(QMessageBox.Yes)
        button_yes.setText('Да')
        button_no = qm.button(QMessageBox.No)
        button_no.setText('Нет')
        qm.exec_()

        if qm.clickedButton() == button_yes:  # необходимо подтвердить удаление
            todo_ids = [self.elements_dictionary[elem] for elem in list_items]
            cur = self.con.cursor()
            cur.execute("DELETE FROM todos WHERE id IN (" + ", ".join(
                '?' * len(todo_ids)) + ")", todo_ids)
            self.con.commit()
            self.update_table()

        else:
            qm.close()

    def export_todo(self, event):
        pass  # ToDo Экспорт в .docx текущего листа

    def todo_clicked(self):
        if self.tableWidget.currentColumn() == 0:
            cur = self.con.cursor()
            current_id = self.elements_dictionary[self.tableWidget.currentRow()]
            current_done = cur.execute("SELECT done FROM todos WHERE id = ?",
                                       (current_id, ))
            cur.execute(
                '''UPDATE todos
SET done = ?
WHERE id = ?''', (not current_done, current_id))

    def todo_double_clicked(self):
        if self.tableWidget.currentColumn() == 1:
            todo_id = self.elements_dictionary[self.tableWidget.currentRow()]

            todo = ToDoWindow(todo_id, False)
            todo.show()

    def open_todo(self):
        # находим id стикера по её порядковому номеру
        todo_id = self.elements_dictionary[self.tableWidget.currentRow()]

        # открываем окно для редактирования стикера и помечаем её как не новую
        todo = ToDoWindow(todo_id, False)
        todo.show()

    def open_calender(self, event):
        pass  # ToDo календарь, в котором отмечены все имеющие задачи с датами

    def open_settings(self, event):
        pass

    def update_table(self):
        self.tableWidget.clear()
        cur = self.con.cursor()
        ids = cur.execute("SELECT id FROM todos").fetchall()
        todo_inf = cur.execute("SELECT name, color_id, done FROM todos").fetchall()
        colors = cur.execute("SELECT color_id from todos").fetchall()
        colors_dict = {}
        for color_id in colors:
            color_code = cur.execute(
                "SELECT color_code FROM colors WHERE color_id = ?", (color_id[0],)).fetchone()[0]
            colors_dict[color_id[0]] = color_code

        if ids:
            self.tableWidget.setRowCount(len(ids))
            self.tableWidget.setColumnCount(2)
            for i, (todo_id, (todo_name, todo_color, todo_done)) in enumerate(zip(ids, todo_inf)):
                self.elements_dictionary[i] = todo_id[0]

                name, done = QTableWidgetItem(todo_name), QTableWidgetItem()
                name.setBackground(QColor(*map(int, colors_dict[todo_color].split(', '))))
                self.tableWidget.setItem(i, 1, name)

                if todo_done:
                    done.setText('a')
                else:
                    done.setText('r')

                done.setBackground(QColor(*map(int, colors_dict[todo_color].split(', '))))
                done.setFont(QFont("Webdings"))
                self.tableWidget.setItem(i, 0, done)


class ToDoWindow(BaseWindow, Ui_ToDoWindow):
    def __init__(self, todo_id, is_new_note):
        super().__init__()
        self.setupUi(self)
        self.id = todo_id
        self.is_new = is_new_note
        
        self.drag_active = False  # флаг для drag and drop плана
        self.spacer.mousePressEvent = self.titleBarMousePressEvent  # ToDo

        self.doneButton.mousePressEvent = self.edit_todo  # ToDo
        self.goBackButton.mousePressEvent = self.go_back
        self.colorBox.currentIndexChanged.connect(self.change_color)  # ToDo
        self.deadlineBox.stateChanged.connect(self.change_date)

        self.con = sqlite3.connect("notes_db.sqlite")
        cur = self.con.cursor()

        if not is_new_note:

            self.nameInput.setText(cur.execute(
                "SELECT name FROM todos WHERE id = ?", (todo_id,)).fetchone()[0])

            self.infoEdit.setText(cur.execute(
                "SELECT info FROM todos WHERE id=?", (todo_id,)).fetchone()[0])

            color_id = cur.execute(
                "SELECT color_id FROM todos WHERE id = ?", (todo_id,)).fetchone()[0]
            self.colorBox.setCurrentIndex(color_id - 1)
            self.change_color()

            date = cur.execute(
                "SELECT date FROM todos WHERE id=?",  (todo_id,)).fetchone()[0]
            if date:
                self.deadlineBox.setChecked(True)
                self.dateEdit.setDate(dt.date.fromisoformat(date))

        else:
            self.nameInput.setText("Новый план")
            self.dateEdit.setDate(dt.date.today())

            cur.execute(
                "INSERT INTO todos(id, name, info, color_id, done) VALUES(?, ?, ?, ?, ?)",
                (self.id, self.nameInput.text(), self.infoEdit.toPlainText(),
                 1, False))
            self.con.commit()
            update_todo_list()

    def edit_todo(self, event):
        cur = self.con.cursor()

        if self.deadlineBox.isChecked():
            date = self.dateEdit.date().toString("yyyy-MM-dd")
        else:
            date = None
        cur.execute('''UPDATE todos
        SET name = ?, info = ?, color_id = ?, date = ?
        WHERE id = ?''',
                    (self.nameInput.text(), self.infoEdit.toPlainText(),
                     self.colorBox.currentIndex() + 1, date, self.id))
        self.con.commit()
        update_todo_list()

    def change_color(self):
        cur = self.con.cursor()
        color = cur.execute(
            "SELECT color_code FROM colors WHERE color_id = ?", (self.colorBox.currentIndex() + 1, )
        ).fetchone()[0]
        self.spacer.setStyleSheet(f"background-color: rgb({color})")

    def go_back(self, event):
        self.close()

    def change_date(self):
        self.dateEdit.setEnabled(self.deadlineBox.isChecked())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notes = NotesWindow()
    todos = ToDoMenu()
    notes.show()
    sys.exit(app.exec())
