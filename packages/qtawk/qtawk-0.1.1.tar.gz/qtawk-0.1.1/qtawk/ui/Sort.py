# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sort.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 164)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.ignoreCase = QtWidgets.QCheckBox(Dialog)
        self.ignoreCase.setObjectName("ignoreCase")
        self.verticalLayout.addWidget(self.ignoreCase)
        self.reverse = QtWidgets.QCheckBox(Dialog)
        self.reverse.setObjectName("reverse")
        self.verticalLayout.addWidget(self.reverse)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sort options"))
        self.comboBox.setItemText(0, _translate("Dialog", "-d, --dictionary-order"))
        self.comboBox.setItemText(1, _translate("Dialog", "-n, --numeric-sort"))
        self.comboBox.setItemText(2, _translate("Dialog", "-R, --random-sort"))
        self.comboBox.setItemText(3, _translate("Dialog", "-M, --month-sort"))
        self.comboBox.setItemText(4, _translate("Dialog", "-h, --human-numeric-sort"))
        self.ignoreCase.setText(_translate("Dialog", "-f, --ignore-case"))
        self.reverse.setText(_translate("Dialog", "-r, --reverse"))

