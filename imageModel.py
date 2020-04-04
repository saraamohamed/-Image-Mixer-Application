## This is the abstract class that the students should implement

from modesEnum import Modes
import numpy as np
import cv2 as cv
#from main import ApplicationWindow

class ImageModel():

	"""
	A class that represents the ImageModel
	"""

	def __init__(self):
		pass

	def __init__(self, imgPath: str):
		self.imgPath = imgPath
		###
		# ALL the following properties should be assigned correctly after reading imgPath
		###
		self.imgByte =cv.cvtColor(cv.imread(self.imgPath), cv.COLOR_BGR2GRAY)
		self.dft = np.fft.fft2(self.imgByte)
		self.real =np.real(self.dft)
		self.size= self.imgByte.shape
		self.imaginary =1j*np.imag(self.dft)
		self.magnitude = np.abs(self.dft)
		self.phase = np.angle(self.dft)
		

	def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
		
		if mode == Modes.magnitudeAndPhase:
			Mixed_Mag = (self.magnitude * magnitudeOrRealRatio) + (imageToBeMixed.magnitude * (1 - magnitudeOrRealRatio))
			Mixed_Phase = (imageToBeMixed.phase * phaesOrImaginaryRatio) + (self.phase * (1 - phaesOrImaginaryRatio))
			Complex = Mixed_Mag * np.exp(Mixed_Phase * 1J)
			inverse = np.fft.ifft2(Complex)
			inverse = np.abs(inverse)
			return(inverse)

		elif mode == Modes.realAndImaginary:
			Mixed_Real = (self.real * magnitudeOrRealRatio) + (imageToBeMixed.real * (1 - magnitudeOrRealRatio))
			Mixed_Imag = (imageToBeMixed.imaginary * phaesOrImaginaryRatio) + (self.imaginary * (1 - phaesOrImaginaryRatio))
			Complex = Mixed_Real + (Mixed_Imag*1J)
			inverse = np.fft.ifft2(Complex)
			inverse = np.abs(inverse)
			return(inverse)

		elif mode == Modes.uniMagnitudeAndPhase:
			Mixed_Mag = np.ones(self.imgByte.shape)
			Mixed_Phase = np.zeros(self.imgByte.shape)
			Complex = Mixed_Mag * np.exp(Mixed_Phase * 1J)
			inverse = np.fft.ifft(Complex)
			inverse = np.abs(inverse)
			return(inverse)

		elif mode == Modes.uniPhase:
			Mixed_Mag = (self.magnitude * magnitudeOrRealRatio) + (imageToBeMixed.magnitude * (1 - magnitudeOrRealRatio))
			Mixed_Phase = np.zeros(self.imgByte.shape)
			Complex = Mixed_Mag * np.exp(Mixed_Phase * 1J)
			inverse = np.fft.ifft(Complex)
			inverse = np.abs(inverse)
			return(inverse)

		elif mode == Modes.uniMagnitude:
			Mixed_Phase = (self.phase * phaesOrImaginaryRatio) + (imageToBeMixed.phase * (1 - phaesOrImaginaryRatio))
			Mixed_Mag = np.ones(self.imgByte.shape)
			Complex = Mixed_Mag * np.exp(Mixed_Phase * 1J)
			inverse = np.fft.ifft(Complex)
			inverse = np.abs(inverse)
			return(inverse)

		
		pass


		"""
		a function that takes ImageModel object mag ratio, phase ration and
		return the magnitude of ifft of the mix
		return type ---> 2D numpy array

		please Add whatever functions realted to the image data in this file
		"""
		###
		# implement this function
		###