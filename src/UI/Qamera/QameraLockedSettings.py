from math import pi
import json


class QameraLockedSettings:
	def __init__(self):
		self.start_alpha = None
		self.start_beta = None
		self.start_r = None
		self.sensibilite = None
		self.zoom_sensibilite = None

	def default(self):
		self.start_alpha = 3 * pi / 4
		self.start_beta = pi / 4
		self.start_r = 20
		self.sensibilite = 1
		self.zoom_sensibilite = 5

	def save(self):
		print("Saving camera locked settings...")
		try:
			with open('QameraLockedSettings.json', 'w') as file:
				json.dump(self.__dict__, file)
		except:
			print("Failed to save")
			raise IOError

	def load(self):
		print("Loading camera locked settings...")
		try:
			with open('QameraLockedSettings.json', 'r') as file:
				self.__dict__ = json.load(file)
		except:
			print("Failed")
			raise IOError
