#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, uic, QtGui
from pyqtgraph import PlotWidget
import datetime
import core
from ui.MainUi import Ui_MainWindow
from ui.SelectColumns import Ui_Dialog
from ui.Substitute import Ui_Dialog
from ui.Sort import Ui_Dialog
from ui.Padding import Ui_Dialog
from ui.AutoPadding import Ui_Dialog

class Sort(QtGui.QDialog):
	
	def __init__(self, *args, obj=None, **kwargs):
		super(Sort, self).__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		uic.loadUi(core.getPathPyFile() + '/ui/Sort.ui', self)

class Padding(QtGui.QDialog):
	
	def __init__(self, *args, obj=None, **kwargs):
		super(Padding, self).__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		uic.loadUi(core.getPathPyFile() + '/ui/Padding.ui', self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		
class About(QtGui.QDialog):
	
	def __init__(self, *args, obj=None, **kwargs):
		super(About, self).__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		uic.loadUi(core.getPathPyFile() + '/ui/About.ui', self)
		self.pushButton.clicked.connect(self.close)
		self.textBrowser.setHtml(core.load(core.getPathPyFile() + "/ui/about.html"))
		self.textBrowser.setOpenExternalLinks(True)
		
	def close(self):
		self.hide()
		
class AutoPadding(QtGui.QDialog):
	
	def __init__(self, *args, obj=None, **kwargs):
		super(AutoPadding, self).__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		uic.loadUi(core.getPathPyFile() + '/ui/AutoPadding.ui', self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)

class Substitute(QtGui.QDialog):
	
	def __init__(self, *args, obj=None, **kwargs):
		super(Substitute, self).__init__(*args, **kwargs)
		self.ui = Ui_Dialog()
		uic.loadUi(core.getPathPyFile() + '/ui/Substitute.ui', self)
		self.buttonBox.accepted.connect(self.onAccept)
		self.buttonBox.rejected.connect(self.reject)
		
	def onAccept(self):
		self.old = self.lineEdit.text()
		self.new = self.lineEdit_2.text()
		
class SelectColumns(QtGui.QDialog):
	
	def __init__(self, *args, obj=None, **kwargs):
		super(SelectColumns, self).__init__(*args, **kwargs)
		uic.loadUi(core.getPathPyFile() + '/ui/SelectColumns.ui', self)
		self.buttonBox.accepted.connect(self.onAccept)
		self.buttonBox.rejected.connect(self.reject)
		self.btnAdd.released.connect(self.onAdd)
		self.btnRemove.released.connect(self.onRemove)
		self.ret = None
	
	def setCount(self, n):
		for i in range(n):
			self.listWidget.addItem(str(i + 1))
		
	def onAccept(self):
		r = []
		for i in range(self.listWidget_2.count()):
			r.append(self.listWidget_2.item(i).text())
		self.ret = r
		self.hide()
		self.accept()
		
	def onAdd(self):
		selection = [item.text() for item in self.listWidget.selectedItems()]
		self.listWidget_2.addItems( selection )
		self.listWidget.clearSelection()

	def onRemove(self):
		for item in self.listWidget_2.selectedItems():
			self.listWidget_2.takeItem(self.listWidget_2.row(item))
	
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	def __init__(self, *args, obj=None, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		self.actionQuit.triggered.connect(self.onQuit)
		self.actionOpen.triggered.connect(self.onOpen)
		self.actionSave.triggered.connect(self.onSave)
		self.actionImport.triggered.connect(self.onImport)
		self.actionExport.triggered.connect(self.onExport)
		self.actionSaveAs.triggered.connect(self.onSaveAs)
		self.actionEgrep.triggered.connect(self.onEgrep)
		self.actionHead.triggered.connect(self.onHead)
		self.actionTail.triggered.connect(self.onTail)
		self.actionCut.triggered.connect(self.onCut)
		self.actionUndo.triggered.connect(self.onUndo)
		self.actionRedo.triggered.connect(self.onRedo)
		self.actionKeepOneLine.triggered.connect(self.onKeepOneLine)
		self.actionWhere.triggered.connect(self.onWhere)
		self.actionSubstitute.triggered.connect(self.onSubstitute)
		self.actionSelectFields.triggered.connect(self.onSelectFields)
		self.actionSort.triggered.connect(self.onSort)
		self.actionCustom.triggered.connect(self.onCustom)
		self.actionCount.triggered.connect(self.onCount)
		self.actionAppendField.triggered.connect(self.onAppendField)
		self.actionTranspose.triggered.connect(self.onTranspose)
		self.actionMean.triggered.connect(self.onMean)
		self.actionMax.triggered.connect(self.onMax)
		self.actionMin.triggered.connect(self.onMin)
		self.actionSum.triggered.connect(self.onSum)
		self.actionTable.triggered.connect(self.onTable)
		self.actionPadding.triggered.connect(self.onPadding)
		self.actionAutoPadding.triggered.connect(self.onAutoPadding)
		self.actionHistogram.triggered.connect(self.onHistogram)
		self.actionAbout.triggered.connect(self.onAbout)
		self.lineEdit_FS.editingFinished.connect(self.onChangeFS)
		self.lineEdit_RS.editingFinished.connect(self.onChangeRS)
		self.lineEditSearch.editingFinished.connect(self.onSearch)
		self.btnSearch.clicked.connect(self.onSearch)
		self.btnSearchClear.clicked.connect(self.onSearchClear)
		self.tabWidget.currentChanged.connect(self.onTabChange)
		self.filename = ""
		self.appName = "QtAwk"
		self.setWindowIcon(QtGui.QIcon(core.getPathPyFile() + '/ico/logo_32_v4.ico'))
		self.setWindowTitle( self.appName )
		#  self.showMaximized()
		self.label.setFocus()
		self.actionUndo.setDisabled(True)
		self.actionRedo.setDisabled(True)
		
		self.history = [] 		# (tableWidget, raw, cmd)
		self.undo = []
		self.FS = " " 			# Field separator
		self.RS = "\n" 			# Record separator
		self.init()
		self.actualTable = None
		self.lastResearch = None
		self.lineEdit_FS.setText(self.FS)
		
		### tests
	
		'''	
		self.FS = ":"
		self.lineEdit_FS.setText(self.FS)
		raw = core.load("/etc/passwd")
		self.addHistory(raw, "cat /etc/passwd")
		raw = core.call_pipe("head -n 5", self.history[-1][1])
		self.addHistory(raw, "head -n 5")
		'''
		
	def onTabChange(self):
		'''
		lorsque « table » est utilisé, il y a un bug si textEdit (tab 2 "script" ) est sélectionné, le tableWidget (tab 1 "text") affiche un seul champ avec les "|"
		'''
		'''
		t = self.history[-1][0]
		print("actual :", t)
		self.gridLayout_2.addWidget( t , 0, 0 )
		t.update()
		t.show()
		t.setVisible(True)
		print("="*50)
		for i in self.history:
			print(i[0])
		print("="*50)
		'''
		pass
		
	def init(self):
		for i in self.history:
			self.deleteTable(i[0])
		self.history = [] 		# (tableWidget, raw, cmd)
		self.undo = []
		self.textEdit.clear()
		self.listWidget.clear()
		
	def addTable(self, data, FS=None):
		"""
		return a tableWidget feed with data
		"""
		if FS is None:
			FS = self.FS
		# count rows and lines in data
		lines = []
		rows = data.split(self.RS)
		nb_col = {}
		for i in rows:
			try:
				line = i.split(FS)
			except:
				print("Field Separator is empty")
				return
			lines.append(line)
			nb_col[len(line)] = 1
		
		t = QtWidgets.QTableWidget(len(rows), max(nb_col))
		self.gridLayout_2.addWidget( t , 0, 0 )
		
		#insert data in table
		for r in range(len(rows)):
			line = lines[r]
			for l in range(len(line)):
				t.setItem(r , l, QtGui.QTableWidgetItem(line[l]))
		t.setVisible(True)
		self.actualTable = t
		return t

	def selectColumns(self):
		sc = SelectColumns()
		try:
			sc.setCount(self.actualTable.columnCount())
		except:
			QtWidgets.QMessageBox.about(self, "Warning", "No field available.")
			return False, None
		sc.show()
		ok = sc.exec_()
		return ok, sc.ret
	
	def onSelectFields(self):
		ok, ret = self.selectColumns()
		s = ["${}".format(i) for i in ret]
		fs = '"' + self.FS + '"'
		s = fs.join(s)
		self.apply( "awk '{}{{ print {} }}'".format(core.awk_begin("", self.FS, self.RS), s) )
		
	def onChangeRS(self):
		self.RS = core.escape_rs(self.lineEdit_RS.text())
		self.addTable(self.history[-1][1])
		
	def onChangeFS(self):
		self.FS = core.escape_rs(self.lineEdit_FS.text())
		self.addTable(self.history[-1][1])
		
	def refreshTable(self):
		t = self.history[-1][0]
		t.show()
		t.activateWindow()
		t.raise_()
		
	def deleteTable(self, t):
		t.hide()
		t.raise_()
		t.destroy()
	
	def search(self, table, pattern):
		for row in range(table.rowCount()):
			for col in range(table.columnCount()):
				try:
					v = table.item(row, col).text()
				except:
					v = ""
				if pattern in v:
					yield row, col
		
	def onSearchClear(self):
		self.lineEditSearch.setText("")
		
	def onSearch(self):
		p = self.lineEditSearch.text()
		if p == "":
			return
			
		if self.lastResearch != p:
			self.gen = self.search( self.history[-1][0], p)
			self.lastResearch = p
			
		try:
			row, col = self.gen.__next__()
			self.history[-1][0].setCurrentCell(row, col)
		except:
			self.gen.close()
			self.lastResearch = None
		
	def onUndo(self):
		if len(self.history) <= 1:
			print("nothing to undo")
			return
		self.undo.append(self.history.pop())
		self.updateScript()
		self.refreshTable()
		self.updateStateButtonUndoRedo()
		
	def onRedo(self):
		if len(self.undo) > 0:
			self.history.append(self.undo.pop())
		self.updateScript()
		self.refreshTable()
		self.updateStateButtonUndoRedo()
	
	def updateStateButtonUndoRedo(self):
		self.actionUndo.setDisabled(True)
		self.actionUndo.setDisabled(True)
		if len(self.history) <= 1:
			self.actionUndo.setDisabled(True)
		else:
			self.actionUndo.setDisabled(False)
		if len(self.undo) == 0:
			self.actionRedo.setDisabled(True)
		else:
			self.actionRedo.setDisabled(False)
		
	def updateScript(self):
		self.listWidget.clear()
		r = ""
		for i in range(len(self.history)):
			cmd = self.history[i][2]
			self.listWidget.addItem(cmd)
			r += cmd
			if i < len(self.history) - 1:
				r += " | "
		
		self.textEdit.setText(r)
		
	def addHistory(self, raw, cmd):
		self.history.append((self.addTable(raw), raw, cmd))
		self.updateScript()
		self.updateStateButtonUndoRedo()
	
	def apply(self, cmd):
		if len(self.history) == 0:
			data = None
		else:
			data = self.history[-1][1]
		self.addHistory(core.call_pipe(cmd, self.history[-1][1]), cmd)
	
	def onAppendField(self):
		msg = '''
Example :

	n		: the current line number			
	$1*$2		: multiply the field 1 and 2            
	$4$1		: concat field 4 and 1				
			'''
		args, ok = QtWidgets.QInputDialog.getText(self, "Append field", msg)
		if args == "":
			return
		if not ok:
			return
		
		self.apply( "awk '{}{{print $0\"{}\"{}; n++}}'".format(core.awk_begin("n=1;", self.FS, self.RS), self.FS, args) )
	
	def onCount(self):
		args, ok = QtWidgets.QInputDialog.getText(self, "Select a field", "Enter field number (example 5):")
		if args == "":
			return
		if not ok:
			return
			
		self.apply( "awk '{}'".format(core.get_script("count.awk").format( core.awk_begin("f={};".format(args), self.FS, self.RS) ) ) )
		return args
	
	def onMax( self ):
		args, ok = QtWidgets.QInputDialog.getText(self, "Select a field", "Enter field number (example 5):")
		if args == "":
			return
		if not ok:
			return
		self.apply("awk '{}'".format(core.get_script("max.awk").format( core.awk_begin("", self.FS, self.RS), args, ">") ) )
	
	def onMin( self ):
		args, ok = QtWidgets.QInputDialog.getText(self, "Select a field", "Enter field number (example 5):")
		if args == "":
			return
		if not ok:
			return
		self.apply("awk '{}'".format(core.get_script("max.awk").format( core.awk_begin("", self.FS, self.RS), args, "<") ) )
		
	def onMean( self ):
		args, ok = QtWidgets.QInputDialog.getText(self, "Select a field", "Enter field number (example 5):")
		if args == "":
			return
		if not ok:
			return
		self.apply("awk '{}'".format(core.get_script("mean.awk").format( core.awk_begin("", self.FS, self.RS), args) ) )
		
	def onSum( self ):
		args, ok = QtWidgets.QInputDialog.getText(self, "Select a field", "Enter field number (example 5):")
		if args == "":
			return
		if not ok:
			return
		self.apply("awk '{}'".format(core.get_script("sum.awk").format( core.awk_begin("", self.FS, self.RS), args) ) )
		
	def onTranspose(self):
		self.apply( "awk '{}'".format( core.get_script("transpose.awk").format(core.awk_begin("", self.FS, self.RS) ) ) )
	
	def onTable(self):
		if len(self.history) == 0:
			return
		
		msg = "By default, all fields are left aligned. If you want right aligned fields, select them on next window."
		ret = self.messageBox("Information", msg)
		if not ret:
			return
			
		ok, f = self.selectColumns()
		columns_align_right = ""
		for i in f:
			columns_align_right += "r[{}]=1;".format(i)

		msg = """
	Header ?
	
	0 : no header
	N : the Nth line will be a separator
		"""
		header, ok = QtWidgets.QInputDialog.getText(self, "Header ?", msg)
		
		if header.isdigit():
			if header == "0" or header == "":
				header = -1
			columns_align_right += "header={};".format(header)
		else:
			columns_align_right += "header=-1;"
		columns_align_right += "footer=-1;"
		
		self.apply( "awk '{}'".format( core.get_script( "table.awk").format(core.awk_begin("l=0;OFS = \"|\";ORS = \"\";" + columns_align_right, self.FS, self.RS ) ) ) )
		
		(tableWidget, raw, cmd) = self.history.pop()
		self.deleteTable(tableWidget)
		del tableWidget
		t = self.addTable(raw, "|")
		self.history.append( (t, raw, cmd) )
		
		try:
			for i in range(t.columnCount()):
					t.setItem(int(header) , i, QtGui.QTableWidgetItem("-"))
		except:
			print("Display header separator error")
			pass
		t.update()
		t.setVisible(True)
		
	def onHistogram(self):
		self.onCount()
		self.apply("awk '{}'".format(core.get_script("histogram.awk").format(core.awk_begin("l=0;", self.FS, self.RS) ) ) )

	def onPadding(self):
		form = Padding()
		for i in range(self.actualTable.columnCount()):
			form.comboBox.addItem(str(i+1))
		form.show()
		ok = form.exec_()
		
		l = form.comboBox.currentText()
		r = form.comboBox_2.currentText()
		width = form.lineEdit.text()
		l2 = '" "'.join( [ "${}".format(i) for i in range(self.actualTable.columnCount())] )
		
		if r ==  "left":
			l2 = l2.replace('${}'.format(l), '${}p'.format(l))
		else:
			l2 = l2.replace('${}'.format(l), 'p${}'.format(l))
			
		cmd = "awk '{}{{ p=\"\"; for (i = 1; i <= {} - length(${}); i++) {{ p = p\" \" }}; print {}}}'".format(core.awk_begin("", self.FS, self.RS), width, l, l2)
		self.apply(cmd)
	
	def onAutoPadding(self):
		form = AutoPadding()
		form.show()
		ok = form.exec_()
		r = form.comboBox.currentText()
		padding = ""
		if r ==  "right":
			padding = "right=1;"
		self.apply("awk '{}'".format( core.get_script("padding.awk").format(core.awk_begin("l=0;ORS = \"\";" + padding, self.FS, self.RS) ) ) )
		
	def onEgrep(self):
		self.onCommand("egrep")
		
	def onHead(self):
		self.onCommand("head")
			
	def onTail(self):
		self.onCommand("tail")
		
	def onCut(self):
		self.onCommand("cut")
	
	def onCustom(self):
		args, ok = QtWidgets.QInputDialog.getText(self, "Custom command", "Enter any command :")
		if args == "":
			return
		if ok:
			self.apply(args)
		
	def onKeepOneLine(self):
		args, ok = QtWidgets.QInputDialog.getText(self, "Keep one line", "Enter line number")
		if args == "":
			return
		if ok:
			self.apply( "awk '{}{{if (n=={}) {{print $0; exit}}; n++}}'".format(core.awk_begin("n=1;", self.FS, self.RS), args) )
	
	def onWhere(self):
		msg = """
Examples :

	$1 ~ /foo/      : select lines where first field contain "foo"	

	$7 !~ /^$/      : select lines where 7th field is not empty	

	(n>10 &&&& n<15)  : select only the lines 11 to 14.	
		"""
		args, ok = QtWidgets.QInputDialog.getText(self, "where condition", msg)
		if args == "":
			return
		if ok:
			self.apply( "awk '{}{{if ({}) {{print $0; }}; n++}}'".format(core.awk_begin("n=1;", self.FS, self.RS), args) )

	def onSubstitute(self):
		sub = Substitute()
		sub.show()
		ok = sub.exec_()
		if ok:	
			self.apply( "awk 'BEGIN{{RS=\"{}\";ORS=\"{}\"}}{{if (RT==\"\") printf \"%s\",$0; else print}}'".format(sub.old, sub.new) )
			
	def sortUi(self):
		ui = Sort()
		ui.show()
		ok = ui.exec_()
		r = ""
		
		if ok:
			r = ui.comboBox.currentText().split()[0]
			r = r[:-1]
			if ui.ignoreCase.isChecked():
				r += " -f"
			if ui.reverse.isChecked():
				r += " -r"
		
		return r

	def onSort(self	):
		ok, ret = self.selectColumns()
		if ok != QtWidgets.QDialog.Accepted:
			print("Sort aborted")
			return 
		
		columns = ""
		if len(ret) > 0:
			for i in ret:
				columns += '${}'.format(i)
		else :
			print("No field available")
			return

		args = self.sortUi()
		
		columns += '"{}"$0'.format(self.FS)
		cmd = "awk '{}{{ print {} }}'".format(core.awk_begin("", self.FS, self.RS), columns)
		cmd += "| sort {}".format(args)
		cmd += "| awk '{}'".format( core.get_script("remove_first_field.awk").format(core.awk_begin("", self.FS, self.RS)) )
		self.apply(cmd)
		
	def man(self, cmd):
		return "{}\nEnter parameters :\n".format(core.man(cmd))

	def onCommand(self, cmd, title=None, text=None):
		if title is None:
			title = cmd
		if text is None:
			text = self.man(cmd)
		args, ok = QtWidgets.QInputDialog.getText(self, title, text)
		if args == "":
			return
		if ok:
			self.apply( "{} {}".format(cmd, args) )
			
	def messageBox(self, title, msg):
		reply = QtWidgets.QMessageBox.warning(
				self, title, msg,
				QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
				QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			return True
		return False
	
	def onSave(self):
		if self.filename == "":
			self.onSaveAs()
		else:
			core.save(self.filename, self.textEdit.toPlainText() )
			core.chmod(self.filename)
	
	def setTitle(self, text):
		self.setWindowTitle( self.appName + " - " + text)
		
	def onSaveAs(self):
		fn = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '',"*")[0]
		self.filename = fn
		core.save(self.filename, self.textEdit.toPlainText() )
		core.chmod(self.filename)
		self.setTitle(fn)
		
	def onOpen(self):
		ret = self.messageBox("WARNING", "Open and run a script can harm your system and your data !")
		if not ret:
			return
		fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"*")[0]
		self.OpenFile(fn)
		
	def OpenFile(self, fn):
		d = [i.strip() for i in core.load(fn).split('|')]
		msg = "This script begin by :\n\n"
		msg += "\n".join(d[:10])
		msg += "\n\n Do you really want to run this script ?"
		ret = self.messageBox("Run this ?", msg)
		if not ret:
			return
		self.init()
		raw = core.call_external_command_without_pipe(d[0])
		self.addHistory(raw, d[0])
		d.pop(0)
		for i in d:
			raw = core.call_pipe(i, raw)
			self.addHistory(raw, i)
			
		self.setTitle(fn)
		self.filename = fn
		
	def onExport(self, fn):
		fn = QtWidgets.QFileDialog.getSaveFileName(self, 'Export output as+6', '',"*")[0]
		core.save(fn, self.history[-1][1] )
		
	def onImport(self, fn):
		fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"*")[0]
		if fn == "":
			return
		cmd = "cat {}".format(fn) 
		raw = core.call_external_command_without_pipe(cmd)
		self.history = []
		self.addHistory(raw, cmd)
		self.setTitle( fn )
		
	def onDelete(self):
		t = self.tableWidget
		c = t.currentRow()
		if c < 0:
			print("No row selected")
			return
		t.removeRow(t.currentRow())
		t.setcurrentt = -1
	
	def onAbout(self):
		a = About()
		a.exec_()
			
	def onQuit(self):
		exit(0)
	
	def getData(self):
		t = self.tableWidget
		r = t.rowCount()
		d = {}
		for j in range(3):
			d[j] = []
			for i in range(r):
				d[j].append(t.item(i, j).text())
		return d

def run():
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
	
if __name__ == "__main__":
	run()
