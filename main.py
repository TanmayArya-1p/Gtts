from gtts import gTTS
import googletrans
from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from playsound import playsound
import os
from threading import Thread

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
		self.folderpath = "C:\TTS_Output"
		self.filename = "tts.mp3"

		self.ui.Path.setText(self.folderpath)
		self.ui.file_name.setText(self.filename)

		for i in self.langs:
			self.ui.Language_Selector.addItem(Capitilization(i))

		self.ui.Open_File_Location.clicked.connect(self.ChooseOutput)
		self.ui.Convert.clicked.connect(self.ConvertFile)

	def ChooseOutput(self):
		self.folderpath = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Output Folder'))
		self.folderpath =  self.folderpath.replace(r"/" , chr(92))
		print(f"Changed Path : {self.folderpath}")
		self.ui.Path.setText(self.folderpath)

	def ConvertFile(self):
		self.filename = str(self.ui.file_name.text())

		msg = QMessageBox()
		msg.setWindowTitle("gTTs Error")
		msg.setIcon(QMessageBox.Critical)
		msg.setStandardButtons(QMessageBox.Close)
		msg.setDefaultButton(QMessageBox.Close)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)


		if((self.filename != "" ) and (str(self.ui.textEdit.toPlainText())!="")):
			tts = gTTS(str(self.ui.textEdit.toPlainText()) , lang=self.langs.get(self.ui.Language_Selector.currentText().lower()))

			if((self.filename.endswith(".mp3"))):
				tts.save(f"{self.folderpath}"+chr(92) +str(self.filename))
				self.audiopath = f"{self.folderpath}"+chr(92) +str(self.filename)
				m = QMessageBox()
				m.setWindowTitle("gTTs Preview")
				m.setText(f"Do you want to preview '{self.filename}'?")
				m.setIcon(QMessageBox.Question)
				m.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
				m.setDefaultButton(QMessageBox.No)
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("gtts.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				m.setWindowIcon(icon)
				m.buttonClicked.connect(self.PreviewSound)
				m.exec_()
				

			else:
				msg.setText("File Name does not end with '.mp3' ")
				msg.setInformativeText("Supported Formats : '.mp3'")
				msg.exec_()
		

		elif((self.filename == "" ) and (str(self.ui.textEdit.toPlainText())=="")):
			msg.setText("Both File Name and Text Input Fields are empty.")
			msg.exec_()
			
		elif((self.filename == "" )):
			msg.setText("File Name Fields is empty.")
			msg.exec_()
			
		elif((str(self.ui.textEdit.toPlainText())=="")):
			msg.setText("No Text Inputted Into Input Field.")
			msg.exec_()

	def PreviewSound(self,pt):
		print(pt.text())
		if(pt.text() == "&Yes"):
			with open(self.audiopath , "rb") as g:
				with open("tts.mp3" , "wb") as h:
					h.write(g.read())
					h.close()
					g.close()
			playsound("tts.mp3", False)
		else:
			pass




		

	


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = GttsWindow()
	ui.show()
	sys.exit(app.exec_())





