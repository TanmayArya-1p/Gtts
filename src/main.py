from gtts import gTTS
import googletrans
from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from playsound import playsound
import os
from threading import Thread
import PyPDF2

def ReverseDict(d):
    key_dict = []
    value_dict = []
    for i in d:
        value_dict.append(i)
        key_dict.append(d.get(i))
    
    return dict(zip(key_dict, value_dict))

def Capitilization(s):
	place = s[1:]
	s = s[0].upper() + place
	return s


class GttsWindow(QtWidgets.QMainWindow):
    
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.langs = ReverseDict(googletrans.LANGUAGES)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		for i in self.langs:
			self.ui.Language_Selector.addItem(Capitilization(i))

		self.ui.Convert.clicked.connect(self.ConvertFile)
		self.ui.ReadPDFButton.clicked.connect(self.ReadFromPDFFile)
		self.ui.ReadFileButton.clicked.connect(self.ReadFromTextFile)


	def ConvertFile(self):

		msg = QMessageBox()
		msg.setWindowTitle("gTTs Error")
		msg.setIcon(QMessageBox.Critical)
		msg.setStandardButtons(QMessageBox.Close)
		msg.setDefaultButton(QMessageBox.Close)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)


		if(str(self.ui.textEdit.toPlainText())!=""):
			print("here")
			tts = gTTS(str(self.ui.textEdit.toPlainText()) , lang=self.langs.get(self.ui.Language_Selector.currentText().lower()))
			print("here")
			self.audiopath = str(QtWidgets.QFileDialog.getSaveFileName(self,"Save MP3 File" , filter="MP3 Files (*.mp3)")[0])
			self.audiopath =  self.audiopath.replace(r"/" , chr(92))
			if(self.audiopath != ""):
				self.__SaveThread(tts)
				m = QMessageBox()
				m.setWindowTitle("gTTs Preview")
				m.setText(f"Do you want to preview '{str(self.audiopath.split(chr(92))[len(self.audiopath.split(chr(92)))-1])}' ?")
				m.setIcon(QMessageBox.Question)
				m.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
				m.setDefaultButton(QMessageBox.No)
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				m.setWindowIcon(icon)
				m.buttonClicked.connect(self.PreviewSound)
				m.exec_()
			else:
				m = QMessageBox()
				m.setWindowTitle("gTTs Error")
				m.setText(f"File not Saved")
				m.setIcon(QMessageBox.Critical)
				m.setStandardButtons(QMessageBox.Close)
				m.setDefaultButton(QMessageBox.Close)
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				m.setWindowIcon(icon)
				m.buttonClicked.connect(self.PreviewSound)
				m.exec_()
		else:
			msg.setText("No Text Inputted Into Input Field.")
			msg.exec_()


	def PreviewSound(self,pt):
		if(pt.text() == "&Yes"):
			if("tts.mp3" in list(os.listdir())):
				os.remove("tts.mp3")
			with open(str(self.audiopath) , "rb") as g:
				with open("tts.mp3" , "wb") as h:
					h.write(g.read())
					h.close()
					g.close()
			playsound("tts.mp3", False)
		else:
			pass


	def ReadFromTextFile(self):
		path = str(QtWidgets.QFileDialog.getOpenFileName(self , caption="Choose Text File" , filter="Text files (*.txt)")[0]).replace(r"/" , chr(92))
		try:
			with open(path , "r") as f:
				self.ui.textEdit.setText(f.read())
				f.close()
		except:
				m = QMessageBox()
				m.setWindowTitle("gTTs Error")
				m.setText("Text File Not Chosen.")
				m.setIcon(QMessageBox.Critical)
				m.setStandardButtons(QMessageBox.Close)
				m.setDefaultButton(QMessageBox.Close)
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				m.setWindowIcon(icon)
				m.exec_()


	def ReadFromPDFFile(self):
		path = str(QtWidgets.QFileDialog.getOpenFileName(self , caption="Choose PDF File" , filter="PDF files (*.pdf)")[0]).replace(r"/" , chr(92))
		try:
			otpt = """

			"""
			with open(path, "rb") as pdf_file:
				pdf_reader = PyPDF2.PdfFileReader(pdf_file)
				for i in range(0,pdf_reader.getNumPages()):
					otpt = otpt + pdf_reader.getPage(i).extractText()+"\n"
			self.ui.textEdit.setText(otpt)
		except:
				m = QMessageBox()
				m.setWindowTitle("gTTs Error")
				m.setText("PDF File Not Chosen.")
				m.setIcon(QMessageBox.Critical)
				m.setStandardButtons(QMessageBox.Close)
				m.setDefaultButton(QMessageBox.Close)
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				m.setWindowIcon(icon)
				m.exec_()


	def __SaveThread(self,tts_object):
		print("saving")
		tts_object.save(self.audiopath)




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = GttsWindow()
	ui.show()
	sys.exit(app.exec_())





