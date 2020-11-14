import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QMessageBox

from NotesWindow import Ui_NotesWindow
from NoteWindow import Ui_NoteWindow


def update_list():
    ex.update_list()


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
        pass

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NotesWindow()
    ex.show()
    sys.exit(app.exec())
