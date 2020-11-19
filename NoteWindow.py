# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NoteWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NoteWindow(object):
    def setupUi(self, NoteWindow):
        NoteWindow.setObjectName("NoteWindow")
        NoteWindow.resize(350, 450)
        NoteWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.NoteWindow_2 = QtWidgets.QWidget(NoteWindow)
        self.NoteWindow_2.setStyleSheet("background-color: rgb(23, 28, 37);")
        self.NoteWindow_2.setObjectName("NoteWindow_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.NoteWindow_2)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(325, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nameInput = QtWidgets.QLineEdit(self.NoteWindow_2)
        self.nameInput.setMaximumSize(QtCore.QSize(16777215, 40))
        self.nameInput.setStyleSheet("font: 87 italic 12pt \"Segoe UI Black\";\n"
"alternate-background-color: rgb(15, 76, 117);\n"
"color: rgb(50, 130, 184);\n"
"background-color: rgb(14, 23, 38);\n"
"border-color: rgb(15, 76, 117);")
        self.nameInput.setText("")
        self.nameInput.setMaxLength(100)
        self.nameInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.nameInput.setObjectName("nameInput")
        self.horizontalLayout.addWidget(self.nameInput)
        self.closeButton = QtWidgets.QLabel(self.NoteWindow_2)
        self.closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeButton.setText("")
        self.closeButton.setPixmap(QtGui.QPixmap("ui/closeButton.png"))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(self.NoteWindow_2)
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEdit.setStyleSheet("font: 12pt \"Segoe UI\";\n"
"color: rgb(50, 130, 184);\n"
"background-color: rgb(14, 23, 38);\n"
"")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        NoteWindow.setCentralWidget(self.NoteWindow_2)

        self.retranslateUi(NoteWindow)
        QtCore.QMetaObject.connectSlotsByName(NoteWindow)

    def retranslateUi(self, NoteWindow):
        _translate = QtCore.QCoreApplication.translate
        NoteWindow.setWindowTitle(_translate("NoteWindow", "MainWindow"))
