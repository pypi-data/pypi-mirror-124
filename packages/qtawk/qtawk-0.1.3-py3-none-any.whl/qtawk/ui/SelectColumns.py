# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectColumns.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 744)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btnAdd = QtWidgets.QToolButton(Dialog)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout.addWidget(self.btnAdd)
        self.btnRemove = QtWidgets.QToolButton(Dialog)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.btnRemove.setIcon(icon)
        self.btnRemove.setObjectName("btnRemove")
        self.verticalLayout.addWidget(self.btnRemove)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.listWidget_2 = QtWidgets.QListWidget(Dialog)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_4.addWidget(self.listWidget_2)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select columns"))
        self.label.setText(_translate("Dialog", "available :"))
        self.btnAdd.setText(_translate("Dialog", "..."))
        self.btnRemove.setText(_translate("Dialog", "..."))
        self.label_2.setText(_translate("Dialog", "selected :"))

