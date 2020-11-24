from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.drag_active = False  # флаг для drag and drop стикера

    def titleBarMousePressEvent(self, e):  # метод для drag and drop: запоминаем изначальную позицию
            self.previous_pos = e.globalPos()
            self.drag_active = True

    def mouseMoveEvent(self, e):  # метод для drag and drop: меняем позицию окна
        if self.drag_active:
            delta = e.globalPos() - self.previous_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.previous_pos = e.globalPos()

    def mouseReleaseEvent(self, e):
        if self.drag_active:
            self.drag_active = False
