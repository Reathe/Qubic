from ursina import *


class VuePion(Entity):
	def __init__(self, position, qubic, **kwargs):
		self.qubic = qubic
		super().__init__(
			position=position,
			**kwargs
		)