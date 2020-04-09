from math import pi


class QameraLockedSettings:
	def __init__(self):
		self.start_alpha = None
		self.start_beta = None
		self.start_r = None
		self.sensibilite = None
		self.zoom_sensibilite = None
		self.default()

	def default(self):
		self.start_alpha = 3 * pi / 4
		self.start_beta = pi / 4
		self.start_r = 20
		self.sensibilite = 1
		self.zoom_sensibilite = 5

	# TODO: ça
	def save(self):
		pass

	def load(self):
		pass
