# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(796, 583)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About Qtawk"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"data:image/png;base64,\n"
"iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI\n"
"WXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH5AsBDBsOyfm6uQAABQNJREFUeNrtnT1vHEUYgB9blkwQ\n"
"IEEQLVWQEFUIgjOBBAcFMEQogUShQShWyEdBQYHCTzAYGRIhJBoQEj8BAhFfBRYmTdK5wCBICSIp\n"
"CNiAgk1xd8pps+ezb3d2Z+6eR5pi1x83t++zs+/M7M6O0B9rxMkIsilGPQQKIAogw8pYidfeLRXX\n"
"fSXiXCQZ+k2a1iJJvmKph5cAUQBRAFEAUQBRAFEAUQBRAFEAUQBRAFEAUQBRAFEAUQBRAFEAqZuy\n"
"bgptALdWXPerhq96JmneiBlz2WWYwvBWAsFvl7cNV7kcSij47fKcYevNRu+jXxvw7yfr8HjO2fVy\n"
"hPWczqnnpOErzrGcAzsS6dmerecxw1d8HGDVwzTcAvyQs+9IhN8lr05LhtgkUAq2AADPJvjdnje8\n"
"5fJGQmMA7xiuMDRwKHgoc4BeOcEE9UwGLXjNj0MAVwhJlLEh/u67gW2tRPgn4Ct12NyZ11lSqsfT\n"
"6+QPhw3tYAvwJk4lD7QA+9f53YlN9CScREpEgIuZelwDDmywzr2KJCDAyQLjBUdavYYR4GjgsYn/\n"
"gGXgMnAJ+BDYoQDlcJ7mjGXRM7yOQatlYL6VmCpAn4y3JEhRgM7yK/C6AvTPCeDCJlqD2ARol3+A\n"
"FxSgXBp9CNAo8fNvB3YCrwFfAD9vQIQF4E4FKIe9fQiwN3CdRmnOWl5JsUuqAOWyg+vL3+eVWQUY\n"
"bAFodUefXEeCs6GaIYnnpDoH3AYs5vx8KoQEChAfV4H7gJkuEszGYquXgPAcizUxVIDqON5Fgq11\n"
"XgJWc/q5Eob3u1wOPqmzUssZG3faAgRnkQA3sPTbAqxkth/2RA3OQzn7PqpLgD8z208Yn0p6B1OZ\n"
"feMUnEDqV4CvM9vbjE8lnKM5WdTJq3UI8G5m+27HFCrrfT2a2XdXTstQSyJ42iSwMrITSPNVtwDQ\n"
"nHvv5EVP0Mr4OLO9vY5K5N1f/4AtQCWM5tR3e9UtwFngt8y+eXw8qwpWad5c2skrVQsANz5EMW6X\n"
"sDKyq5/sqUOAGeDfzL7Pqf5J4WHky8z2LXUIAPBSzr7vjU9wvsts31xnZRZykpIZk8Cg3MGNT0XV\n"
"xlbypyxPKkBQCk/LlzV6d7lLEvJeRBJIBcx2aQlmbAHibAFC8GkXCRZr7B0oQOBLQCfPtCTIci/w\n"
"B/AUDhZFQ6gZvH10v3v1M+Bv4EEP/+DT6xUzV4AzhJ9K9hJQc391gd4PQ16i+eDkKeARSrrrtUXd\n"
"D4cOtQBtDrea/lgew+51MLuVixF1bZNc1uYUzcUQUhWgXc4DNylA/0wB3wJ/JSrAaksCBSiB+4EP\n"
"gF+A32nebnYtsADTXF8karrA/zmhAGlQxjJx+3PEvKAAabCbcpacP0DaS+UONac3EPy5hA68AvTB\n"
"QYq/bXRgBBjmMflJ4J7WgVsCvtnkgY/hOBauh5MyNR34WOoxZixLoUE9r8yRinmM+F+a1TBMYThD\n"
"Oq/NmzFc5XIooeC3yz6TwHDJVioY3xLYQ/7LJmIjbz7Dl2iWQN4ybSORnu3Zeh7t9Ueu6jHYjCpA\n"
"cZZy9sV4Ccg72380STAJtAUogYPWWeYSGgOYM1xh2JVA8De1krg5QDk5wQT1TAYtFI2nApQjQLLT\n"
"wSaBDhSIAogCiAKIAogCiAKIAogCiAKIAogCiAKIAogCiAKIAogCyMDgCiHlsaXiz1tRgHhIdok2\n"
"LwHmAKIAMrT8D8PBVD8nTl7hAAAAAElFTkSuQmCC\" /> </p>\n"
"<p style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:600; vertical-align:top;\">Qtawk</span> </p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "close"))

