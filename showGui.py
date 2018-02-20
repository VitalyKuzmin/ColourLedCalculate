# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'show.ui'
#
# Created: Thu Mar 02 05:48:17 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainDialog(object):
    def setupUi(self, mainDialog):
        mainDialog.setObjectName("mainDialog")
        mainDialog.resize(400, 300)
        self.ShowButton = QtGui.QPushButton("Calculate",mainDialog)
        self.ShowButton.setGeometry(QtCore.QRect(300, 260, 75, 23))
        self.ShowButton.setObjectName("ShowButton")
        self.nameEdit = QtGui.QLineEdit(mainDialog)
        self.nameEdit.setGeometry(QtCore.QRect(70, 50, 113, 20))
        self.nameEdit.setObjectName("nameEdit")
        self.nameEdit_2 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_2.setGeometry(QtCore.QRect(70, 80, 113, 20))
        self.nameEdit_2.setObjectName("nameEdit_2")
        self.nameEdit_3 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_3.setGeometry(QtCore.QRect(70, 110, 113, 20))
        self.nameEdit_3.setObjectName("nameEdit_3")
        self.nameEdit_4 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_4.setGeometry(QtCore.QRect(70, 140, 113, 20))
        self.nameEdit_4.setObjectName("nameEdit_4")
        self.nameEdit_5 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_5.setGeometry(QtCore.QRect(210, 50, 113, 20))
        self.nameEdit_5.setObjectName("nameEdit_5")
        self.nameEdit_6 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_6.setGeometry(QtCore.QRect(210, 80, 113, 20))
        self.nameEdit_6.setObjectName("nameEdit_6")
        self.nameEdit_7 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_7.setGeometry(QtCore.QRect(210, 110, 113, 20))
        self.nameEdit_7.setObjectName("nameEdit_7")
        self.nameEdit_8 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_8.setGeometry(QtCore.QRect(210, 140, 113, 20))
        self.nameEdit_8.setObjectName("nameEdit_8")
        self.nameEdit_9 = QtGui.QLineEdit(mainDialog)
        self.nameEdit_9.setGeometry(QtCore.QRect(140, 200, 113, 20))
        self.nameEdit_9.setObjectName("nameEdit_9")
        self.staticText_1 =  QtGui.QLabel("Red:",mainDialog);
        self.staticText_1.setGeometry(QtCore.QRect(20, 50, 113, 20))
        self.staticText_2 =  QtGui.QLabel("Green:",mainDialog);
        self.staticText_2.setGeometry(QtCore.QRect(20, 80, 113, 20))
        self.staticText_3 =  QtGui.QLabel("Blue:",mainDialog);
        self.staticText_3.setGeometry(QtCore.QRect(20, 110, 113, 20))
        self.staticText_4 =  QtGui.QLabel("Yellow:",mainDialog);
        self.staticText_4.setGeometry(QtCore.QRect(20, 140, 113, 20))
        self.staticText_5 =  QtGui.QLabel("Dominant wavelength",mainDialog);
        self.staticText_5.setGeometry(QtCore.QRect(70, 20, 113, 20))
    	self.staticText_5 =  QtGui.QLabel("Width spectra",mainDialog);
        self.staticText_5.setGeometry(QtCore.QRect(210, 20, 113, 20))
        self.staticText_6 =  QtGui.QLabel("Colour Temperature",mainDialog);
        self.staticText_6.setGeometry(QtCore.QRect(140, 180, 113, 20))
        #self.staticText_1.setObjectName("staticText_1")


        self.retranslateUi(mainDialog)
        QtCore.QMetaObject.connectSlotsByName(mainDialog)
        mainDialog.setTabOrder(self.nameEdit, self.nameEdit_2)
        mainDialog.setTabOrder(self.nameEdit_2, self.nameEdit_3)
        mainDialog.setTabOrder(self.nameEdit_3, self.nameEdit_4)
        mainDialog.setTabOrder(self.nameEdit_4, self.nameEdit_5)
        mainDialog.setTabOrder(self.nameEdit_5, self.nameEdit_6)
        mainDialog.setTabOrder(self.nameEdit_6, self.nameEdit_7)
        mainDialog.setTabOrder(self.nameEdit_7, self.nameEdit_8)
        mainDialog.setTabOrder(self.nameEdit_8, self.nameEdit_9)
        mainDialog.setTabOrder(self.nameEdit_9, self.ShowButton)

    def retranslateUi(self, mainDialog):
        mainDialog.setWindowTitle(QtGui.QApplication.translate("mainDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.ShowButton.setText(QtGui.QApplication.translate("mainDialog", "Calculate", None, QtGui.QApplication.UnicodeUTF8))

