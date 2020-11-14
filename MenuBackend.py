import sys
import sqlite3

import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QMessageBox

from MainMenu import Ui_MainMenu
from StudyMenu import Ui_StudyMenu
from ManagementMenu import Ui_ManageWindow

from NotesWindow import Ui_NotesWindow
from NoteWindow import Ui_NoteWindow

from GraphsWindow import Ui_BaseWindow


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
        self.graphsOption.mousePressEvent = self.open_graph

        self.goBackButton.mousePressEvent = self.go_back

    def open_graph(self, event):

        graph = GraphsWidget()
        graph.show()

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
        self.listWidget.itemClicked.connect(self.note_clicked)

        self.elements_dictionary = {}
        self.update_list()
        # ключ - номер в строчки в QListWidget, значение - id заметки

    def back(self, event):
        # возвращение в меню заметок
        show_management()
        self.hide()

    def add_note(self, event):  # добавляем заметку
        # подготавливаем id для новой заметки
        if self.elements_dictionary:
            max_id = max(self.elements_dictionary.values())

        else:
            max_id = 0

        # открываем окно для создания заметки и помечаем её как новую
        note = NoteWindow(max_id + 1, True)
        note.show()

    def remove_note(self, event):
        # удаляем заметку

        list_items = [x.row() for x in self.listWidget.selectedIndexes()]

        if not list_items:
            return None

        qm = QMessageBox
        qm.question(self, '',
                    "Вы действительно хотите удалить выделенные заметки?",
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

    def export_note(self, event):  # экспортируем выбранную заметку в файл .txt
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
        self.listWidget.clear()  # очищаем список заметок, чтобы заполинть его
        cur = self.con.cursor()
        # собираем данные из обновленной БД
        ids = cur.execute("SELECT id FROM notes").fetchall()
        names = cur.execute("SELECT name FROM notes").fetchall()

        for i, (note_id, note_name) in enumerate(zip(ids, names)):
            self.elements_dictionary[i] = note_id[0]  # актуализируем словарь

            #  обновляем список заметок
            self.listWidget.addItem(QListWidgetItem(str(note_name[0])))

    def note_clicked(self):  # пользователь решил отредактировать заметку
        # находим id заметки по её порядковому номеру
        note_id = self.elements_dictionary[self.listWidget.currentRow()]

        # открываем окно для редактирования заметки и помечаем её как не новую
        note = NoteWindow(note_id, False)
        note.show()


class NoteWindow(QMainWindow, Ui_NoteWindow):
    def __init__(self, note_id, is_new_note):
        super().__init__()
        self.setupUi(self)
        self.id = note_id

        self.con = sqlite3.connect("notes_db.sqlite")

        if not is_new_note:  # редактируем уже имеющуюся заметку
            cur = self.con.cursor()
            print(cur.execute("SELECT name FROM notes WHERE id=?", (note_id,)).fetchone()[0])
            self.nameInput.setText(cur.execute("SELECT name FROM notes WHERE id=?",
                                               (note_id, )).fetchone()[0])

            print(cur.execute("SELECT text FROM notes WHERE id=?", (note_id, )).fetchone())
            self.textEdit.setText(cur.execute(
                "SELECT text FROM notes WHERE id=?", (note_id, )).fetchone()[0])
            self.saveButton.mousePressEvent = self.edit_note

        else:  # создаём новую заметку
            self.saveButton.mousePressEvent = self.new_note

    def new_note(self, event):
        #  актуализируем информацию в БД
        cur = self.con.cursor()
        print(self.id)
        cur.execute("INSERT INTO notes(id, name, text) VALUES(?, ?, ?)",
                    (self.id, self.nameInput.text(), self.textEdit.toPlainText()))
        self.con.commit()

        # закрепляем за заметкой статус уже существующей
        self.saveButton.mousePressEvent = self.edit_note

        update_list()  # обновляем графическое представление БД

    def edit_note(self, event):
        cur = self.con.cursor()

        cur.execute('''UPDATE notes
SET name = ?, text = ?
WHERE id = ?''', (self.nameInput.text(), self.textEdit.toPlainText(), self.id))
        self.con.commit()

        update_list()  # обновляем графическое представление БД


class GraphsWidget(QMainWindow, Ui_BaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.goBackButton.mousePressEvent = self.go_back

        self.askButton.mousePressEvent = self.help
        self.calcButton.mousePressEvent = self.run

    def go_back(self):
        create_main_window()
        self.hide()

    def calc(self, string_function, x):
        try:  # если требуется постоянная функция y = x

            function = np.array([int(string_function) for _ in range(200)])

        except ValueError:

            try:
                functions = (" arcsin", " arccos", " arctan", " sin", " cos",
                             " tan", " exp", " log", " sqrt", " pi", " e")

                for math_function in functions:

                    # заменяем математические функции, удобные для восприятия человеком,
                    # на те, с которыми может работать matplotlib
                    if math_function in string_function:
                        string_function = string_function.replace(
                            math_function, f" np.{math_function[1:]}")

                function = eval(string_function)

            except (SyntaxError, NameError):
                return None  # в случае некорректного ввода

        return function

    def define_borders(self, border, edge):  # метод для определения границ графика

        if not border:  # значение по умолчанию
            return 100 * int(edge)  # edge - аргумент, указывающий, какойкрай обрабатывается

        if "pi" in border:  # в границах иногда может быть использовано число пи
            border.replace("pi", "np.pi")

            return eval(border)

        return int(border)

    def run(self, event):
        self.messageBox.setText('')
        mini, maxi = self.define_borders(self.leftBorderInput.text(), -1),\
            self.define_borders(self.rightBorderInput.text(), 1)  # границы

        fig, ax = plt.subplots()  # отрисовываем координатную плоскость

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        try:
            graphs = 2  # количество графиков; если их не будет, ничего не получится начертить
            x = np.linspace(mini, maxi, 200)
            y1, y2 = self.calc(
                ' ' + self.functionInput.text(), x), self.calc(' ' + self.functionInput_2.text(), x)
            try:
                ax.plot(x, y1, color="blue", label="y1(x)")  # рисуем график

            except (ValueError, TypeError, SyntaxError):  # если графика нет
                graphs -= 1

            try:
                ax.plot(x, y2, color="red", label="y2(x)")

            except (ValueError, TypeError, SyntaxError):
                graphs -= 1

            if not graphs:
                raise ValueError

        except TypeError:  # некорректно указаны границы функции
            self.messageBox.setText(self.messageBox.text() + "Неверно указаны границы\n")

        except ValueError:  # оба поля для ввода функции пустые, ошибка вызывается намеренно
            self.messageBox.setText(
                self.messageBox.text() + "Укажите корректно хотя бы один график\n")

        else:  # отрисовываем
            ax.plot(x, np.array([0 for _ in range(200)]), color="black")  # ось х
            ax.legend()
            plt.show()

    def help(self, event):  # нажатие на кнопку знака вопроса для вывода вспомогательной информации
        self.messageBox.setText(
            '''1) Вводите только правую часть уравнения
2) Математические функции и константы вводите в следующем виде:
sin(x), cos(x), tan(x), arcsin(x), arccos(x), arctan(x), exp(x), log(x),
sqrt(x), pi, e
и только в области определения
3) Арифметические действия указывайте в формате:
+ - * / **''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())
