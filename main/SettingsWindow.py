# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(525, 245)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        SettingsWindow.setFont(font)
        SettingsWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        SettingsWindow.setStyleSheet("font: 8pt \"Segoe UI\";")
        self.SettingsWidget = QtWidgets.QWidget(SettingsWindow)
        self.SettingsWidget.setStyleSheet("background-color: rgb(23, 28, 37);")
        self.SettingsWidget.setObjectName("SettingsWidget")
        self.doneButton = QtWidgets.QLabel(self.SettingsWidget)
        self.doneButton.setGeometry(QtCore.QRect(10, 40, 71, 71))
        self.doneButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doneButton.setText("")
        self.doneButton.setPixmap(QtGui.QPixmap("ui/doneIcon.png"))
        self.doneButton.setObjectName("doneButton")
        self.titleBar = QtWidgets.QWidget(self.SettingsWidget)
        self.titleBar.setGeometry(QtCore.QRect(-10, -10, 541, 41))
        self.titleBar.setMouseTracking(False)
        self.titleBar.setStyleSheet("background-color: rgb(35, 41, 53);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Webdings\";")
        self.titleBar.setObjectName("titleBar")
        self.closeButton = QtWidgets.QPushButton(self.titleBar)
        self.closeButton.setGeometry(QtCore.QRect(500, 7, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(12)
        self.closeButton.setFont(font)
        self.closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeButton.setMouseTracking(False)
        self.closeButton.setStyleSheet("QPushButton::hover\n"
"{\n"
"    background-color : red;\n"
" }")
        self.closeButton.setFlat(True)
        self.closeButton.setObjectName("closeButton")
        self.hideButton = QtWidgets.QPushButton(self.titleBar)
        self.hideButton.setGeometry(QtCore.QRect(470, 10, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(12)
        self.hideButton.setFont(font)
        self.hideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.hideButton.setFlat(True)
        self.hideButton.setObjectName("hideButton")
        self.defaultButton = QtWidgets.QLabel(self.SettingsWidget)
        self.defaultButton.setGeometry(QtCore.QRect(10, 120, 71, 71))
        self.defaultButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.defaultButton.setText("")
        self.defaultButton.setPixmap(QtGui.QPixmap("ui/defaultIcon.svg.png"))
        self.defaultButton.setObjectName("defaultButton")
        self.colorBox = QtWidgets.QComboBox(self.SettingsWidget)
        self.colorBox.setGeometry(QtCore.QRect(220, 90, 251, 31))
        self.colorBox.setStyleSheet("color: rgb(50, 130, 184);\n"
"font: 12pt \"Segoe UI\";")
        self.colorBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.colorBox.setFrame(False)
        self.colorBox.setObjectName("colorBox")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.colorBox.addItem("")
        self.label = QtWidgets.QLabel(self.SettingsWidget)
        self.label.setGeometry(QtCore.QRect(100, 50, 221, 71))
        self.label.setStyleSheet("font: 12pt \"Segoe UI\";\n"
"color: rgb(50, 130, 184);")
        self.label.setObjectName("label")
        self.deadlineBox = QtWidgets.QCheckBox(self.SettingsWidget)
        self.deadlineBox.setGeometry(QtCore.QRect(100, 140, 211, 31))
        self.deadlineBox.setStyleSheet("font: 12pt \"Segoe UI\";\n"
"color: rgb(50, 130, 184);")
        self.deadlineBox.setObjectName("deadlineBox")
        self.undoneBox = QtWidgets.QCheckBox(self.SettingsWidget)
        self.undoneBox.setGeometry(QtCore.QRect(100, 190, 221, 31))
        self.undoneBox.setStyleSheet("font: 12pt \"Segoe UI\";\n"
"color: rgb(50, 130, 184);")
        self.undoneBox.setObjectName("undoneBox")
        self.doneButton.raise_()
        self.titleBar.raise_()
        self.defaultButton.raise_()
        self.label.raise_()
        self.colorBox.raise_()
        self.deadlineBox.raise_()
        self.undoneBox.raise_()
        SettingsWindow.setCentralWidget(self.SettingsWidget)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
        self.closeButton.setText(_translate("SettingsWindow", "r"))
        self.hideButton.setText(_translate("SettingsWindow", "0"))
        self.colorBox.setItemText(0, _translate("SettingsWindow", "Любой"))
        self.colorBox.setItemText(1, _translate("SettingsWindow", "Синий"))
        self.colorBox.setItemText(2, _translate("SettingsWindow", "Жёлтый"))
        self.colorBox.setItemText(3, _translate("SettingsWindow", "Зелёный"))
        self.colorBox.setItemText(4, _translate("SettingsWindow", "Фиолетовый"))
        self.label.setText(_translate("SettingsWindow", "<html><head/><body><p>Фильтровать планы:</p><p>По цвету</p></body></html>"))
        self.deadlineBox.setText(_translate("SettingsWindow", "Только с дедлайном"))
        self.undoneBox.setText(_translate("SettingsWindow", "Только несделанные"))
