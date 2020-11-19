# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        MainMenu.setObjectName("MainMenu")
        MainMenu.resize(1200, 800)
        MainMenu.setMinimumSize(QtCore.QSize(1200, 800))
        MainMenu.setMaximumSize(QtCore.QSize(1200, 800))
        MainMenu.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BaseWidget = QtWidgets.QWidget(MainMenu)
        self.BaseWidget.setStyleSheet("background-color: rgb(250, 245, 230);")
        self.BaseWidget.setObjectName("BaseWidget")
        self.manageOption = QtWidgets.QLabel(self.BaseWidget)
        self.manageOption.setGeometry(QtCore.QRect(120, 190, 351, 501))
        self.manageOption.setText("")
        self.manageOption.setPixmap(QtGui.QPixmap("ui/ui/option mid.png"))
        self.manageOption.setObjectName("manageOption")
        self.studyOption = QtWidgets.QLabel(self.BaseWidget)
        self.studyOption.setGeometry(QtCore.QRect(720, 190, 351, 501))
        self.studyOption.setText("")
        self.studyOption.setPixmap(QtGui.QPixmap("ui/ui/option mid.png"))
        self.studyOption.setObjectName("studyOption")
        self.workRaum = QtWidgets.QLabel(self.BaseWidget)
        self.workRaum.setGeometry(QtCore.QRect(400, 50, 401, 91))
        self.workRaum.setStyleSheet("font: 48pt \"Segoe UI\";")
        self.workRaum.setObjectName("workRaum")
        self.managementName = QtWidgets.QLabel(self.BaseWidget)
        self.managementName.setGeometry(QtCore.QRect(140, 230, 301, 281))
        self.managementName.setStyleSheet("background-color: rgb(237, 250, 255);\n"
"color: rgb(41, 171, 135);\n"
"font: 20pt \"Segoe UI\";")
        self.managementName.setObjectName("managementName")
        self.studyName = QtWidgets.QLabel(self.BaseWidget)
        self.studyName.setGeometry(QtCore.QRect(770, 210, 221, 331))
        self.studyName.setStyleSheet("background-color: rgb(237, 250, 255);\n"
"color: rgb(194, 112, 226);\n"
"font: 20pt \"Segoe UI\";")
        self.studyName.setObjectName("studyName")
        MainMenu.setCentralWidget(self.BaseWidget)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "MainWindow"))
        self.workRaum.setText(_translate("MainMenu", "WorkRaum"))
        self.managementName.setText(_translate("MainMenu", "<html><head/><body><p align=\"center\">Мой рабочий стол</p><p align=\"center\"><br/></p><p align=\"center\">- Заметки</p><p align=\"center\">- Записная Книжка</p></body></html>"))
        self.studyName.setText(_translate("MainMenu", "<html><head/><body><p align=\"center\">Моя учёба</p><p align=\"center\"><br/></p><p align=\"center\">- Построение</p><p align=\"center\">графиков</p></body></html>"))
