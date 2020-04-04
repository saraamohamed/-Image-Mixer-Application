from PyQt5 import QtWidgets, QtCore, uic
from PyQt5 import  QtGui
import pyqtgraph as pg
import task3 as ui
import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QMessageBox)
import numpy as np
from scipy import fftpack
from pyqtgraph import PlotWidget
from pathlib import Path
import cv2 as cv
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib import pyplot as plt
import task3 as ui
from imageModel import ImageModel
from modesEnum import Modes
import logging


class ApplicationWindow(ui.Ui_MainWindow):
	def __init__(self, mainApp):
		super(ApplicationWindow, self).setupUi(mainApp) 

		self.load.triggered.connect(self.load_image)
		self.images=[0,0]

		# widget listes
		self.widget_parameters=[self.widget2,self.widget4]
		self.widgets=self.widget_parameters+[self.widget1,self.widget3,self.widget5,self.widget6]
		for x in range(len (self.widgets)):
				self.widgets[x].ui.histogram.hide()
				self.widgets[x].ui.roiBtn.hide()
				self.widgets[x].ui.menuBtn.hide()
				self.widgets[x].ui.roiPlot.hide()

		self.comboBoxes_mix=[self.comboBox_6,self.comboBox_7,self.comboBox_4,self.comboBox_8]
		self.slider = [self.horizontalSlider_1,self.horizontalSlider_2]
		self.comboBox_1.currentIndexChanged.connect(lambda: self.select_parameter(0))
		self.comboBox_2.currentIndexChanged.connect(lambda: self.select_parameter(1))
		self.comboBox_3.currentIndexChanged.connect(self.Output_select)
		for i in range(len(self.comboBoxes_mix)):
			self.comboBoxes_mix[i].currentIndexChanged.connect(self.mix_parameters)

		for i in range(len(self.slider)):
			self.getGain(self.slider[i], i)
	
		self.Output_Flag=False
		self.loadCheck=0

	def load_image(self):
		self.load_img =QtWidgets.QFileDialog.getOpenFileName(None, "Open File", "E:\mozakra\DSP\Photos")
		if self.load_img[0]:
			self.imageObj= ImageModel(self.load_img[0])
			if self.loadCheck == 0:
				self.images[0]=self.imageObj
				self.widget1.show()
				self.widget1.setImage(((self.images[0]).imgByte).T)
				self.comboBox_1.setEnabled(True)
				self.loadCheck=1
				

			elif self.loadCheck == 1:
				if( cv.cvtColor(cv.imread(self.load_img[0]), cv.COLOR_BGR2GRAY).shape == self.images[0].imgByte.shape):
					self.images[1]=self.imageObj
					self.widget3.show()
					self.widget3.setImage(((self.images[1]).imgByte).T)
					self.loadCheck=2
					self.comboBox_2.setEnabled(True)			
				
				else:
					self.MessageError = QMessageBox()
					self.MessageError.setWindowTitle("Error")
					self.MessageError.setText("Please load a same size images")
					self.MessageError.setIcon(QMessageBox.Critical)
					self.ret=self.MessageError.exec()

			elif self.loadCheck == 2 :
				self.MessageError = QMessageBox()
				self.MessageError.setWindowTitle("load")
				self.MessageError.setText("DO you want to load another images")
				self.MessageError.setIcon(QMessageBox.Warning)
				self.MessageError.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
				self.MessageError.buttonClicked.connect(self.popup_button(x))
				self.MessageError.setDefaultButton(QMessageBox.Yes)  # setting default button to Yes
				self.ret=self.MessageError.exec()


	def popup_button(self, i):
		logging.info('Choosing if want to load another two imeges')
		print(i.text())	
		self.action=i.text()
		if self.action == '&Yes':
			self.loadCheck=0
			self.widget_show.plotItem.clear()
			self.widget_parameters.plotItem.clear()
			
		else :
			self.MessageError.close()
			

	def getGain(self, slider, i):
		logging.info('getting the gain of slider')
		slider.valueChanged.connect(self.mix_parameters)

	def Output_select(self):
		logging.info('Choosing Output widget if it esist')
		if str (((self.comboBox_7.currentText()) != '') & ((self.comboBox_6.currentText()) != '')):
			self.comboBox_3.currentIndexChanged.connect(self.mix_parameters)
		else :
			self.Output_Flag=False


	def select_parameter(self,currentIndex):
		logging.info('Choosing only one parameter to show')
		if currentIndex ==0 :
			self.image1_Data=[(20*np.log(np.fft.fftshift(self.images[0].magnitude))),((self.images[0].phase)),(20*np.log(self.images[0].real)),np.abs((self.images[0].imaginary))]
			self.widget2.show()
			self.widget2.setImage((self.image1_Data[self.comboBox_1.currentIndex()]).T)

		if currentIndex ==1 :
			self.image2_Data=[(20*np.log(np.fft.fftshift(self.images[1].magnitude))),((self.images[1].phase)),(20*np.log(self.images[1].real)),np.abs((self.images[1].imaginary))]
			self.widget4.show()
			self.widget4.setImage((self.image2_Data[self.comboBox_2.currentIndex()]).T)

		else:
			pass


		
	def mix_parameters(self):
		logging.info('Chooseeing and mixing 2 imeges parameters')
		self.mix_img1 = self.comboBox_4.currentIndex()
		self.mix_img2= self.comboBox_8.currentIndex()
		self.slide_ratio1=self.slider[0].value()/100
		self.slide_ratio2=self.slider[1].value()/100

		# first hide  all parameters of the 2nd mixing combobox
		self.hideRows=[0,1,2,3,4,5]
		for i in range(len(self.hideRows)):
			self.comboBox_7.view().setRowHidden(self.hideRows[i],False)

		if (str(self.comboBox_6.currentText())) == 'Magnitude':
			self.hideRows=[0,2,3,4]
			for i in range(len(self.hideRows)):
				self.comboBox_7.view().setRowHidden(self.hideRows[i],True)

			if (str(self.comboBox_7.currentText())) == 'Phase':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img1].mix(self.images[self.mix_img2], self.slide_ratio1, self.slide_ratio2, Modes.magnitudeAndPhase)
				print (self.mixing_result)

			elif (str(self.comboBox_7.currentText())) == 'Uniform Phase':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img1].mix(self.images[self.mix_img2], self.slide_ratio1, self.slide_ratio2, Modes.uniPhase)


		elif (str(self.comboBox_6.currentText())) == 'Phase':
			self.hideRows=[1,2,3,5]
			for i in range(len(self.hideRows)):
				self.comboBox_7.view().setRowHidden(self.hideRows[i],True)

			if (str(self.comboBox_7.currentText())) == 'Magnitude':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img2].mix(self.images[self.mix_img1], self.slide_ratio2, self.slide_ratio1, Modes.magnitudeAndPhase)
				print (self.mixing_result)

			elif (str(self.comboBox_7.currentText())) == 'Uniform Magnitude':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img2].mix(self.images[self.mix_img1],self.slide_ratio2, self.slide_ratio1, Modes.uniMagnitude)


		elif (str(self.comboBox_6.currentText())) == 'Uniform Magnitude':
			self.hideRows=[0,2,3,4]
			for i in range(len(self.hideRows)):
				self.comboBox_7.view().setRowHidden(self.hideRows[i],True)

			if (str(self.comboBox_7.currentText())) == 'Phase':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img1].mix(self.images[self.mix_img2], self.slide_ratio1, self.slide_ratio2, Modes.uniMagnitude)
				print (self.mixing_result)

			elif (str(self.comboBox_7.currentText())) == 'Uniform Phase':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img1].mix(self.images[self.mix_img2], self.slide_ratio1, self.slide_ratio2, Modes.uniMagnitudeAndPhase)


		elif (str(self.comboBox_6.currentText())) == 'Uniform Phase':
			self.hideRows=[1,2,3,5]
			for i in range(len(self.hideRows)):
				self.comboBox_7.view().setRowHidden(self.hideRows[i],True)


			if (str(self.comboBox_7.currentText())) == 'Magnitude':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img2].mix(self.images[self.mix_img1], self.slide_ratio2, self.slide_ratio1, Modes.uniPhase)
				print (self.mixing_result)

			elif (str(self.comboBox_7.currentText())) == 'Uniform Magnitude':
				self.Output_Flag= True
				self.mixing_result = self.images[self.mix_img2].mix(self.images[self.mix_img1], self.slide_ratio2, self.slide_ratio1, Modes.uniMagnitudeAndPhase)



		elif (str(self.comboBox_6.currentText())) == 'Real':
			self.hideRows=[0,1,2,4,5]
			for i in range(len(self.hideRows)):
				self.comboBox_7.view().setRowHidden(self.hideRows[i],True)

			if (str(self.comboBox_7.currentText())) == 'Imaginary':
				self.mixing_result = self.images[self.mix_img1].mix(self.images[self.mix_img2], self.slide_ratio1, self.slide_ratio2, Modes.realAndImaginary)
				print (self.mixing_result)
				self.Output_Flag= True


		elif (str(self.comboBox_6.currentText())) == 'Imaginary':
			self.hideRows=[0,1,3,4,5]
			for i in range(len(self.hideRows)):
				self.comboBox_7.view().setRowHidden(self.hideRows[i],True)

			if (str(self.comboBox_7.currentText())) == 'Real':
				self.mixing_result = self.images[self.mix_img2].mix(self.images[self.mix_img1], self.slide_ratio2, self.slide_ratio1, Modes.realAndImaginary)
				print (self.mixing_result)
				self.Output_Flag= True


		if self.Output_Flag == True:
			if (str(self.comboBox_3.currentText())) == 'Output 1':
				self.widget5.show()
				self.widget5.setImage((self.mixing_result).T)

			elif (str(self.comboBox_3.currentText())) == 'Output 2':
				self.widget6.show()
				self.widget6.setImage((self.mixing_result).T)
		else:
			pass





def main():
	app = QtWidgets.QApplication(sys.argv)
	application = QtWidgets.QMainWindow()
	Window = ApplicationWindow(application)
	application.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
