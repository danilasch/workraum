import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from bin.MainMenu import Ui_MainMenu
from bin.StudyMenu import Ui_StudyMenu
from bin.ManagementMenu import Ui_ManageWindow

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
        # self.notes = NotesWindow()
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
