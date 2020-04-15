from ursina import *

from model.pion import PionBlanc


class VuePion(Entity):
	def __init__(self, position, qubic, **kwargs):
		self.qubic = qubic
		super().__init__(
			position=position,
			**kwargs
		)


class VuePionFactory:
	def __init__(self, qubic, pion='Classic'):
		"""
		Args:
			pion: le type de pion (le skin)
			qubic: le qubic
		"""
		pion_types = {'Classic': self.create_classic}
		self.create_pion = pion_types.get(pion)
		self.qubic = qubic

	def create_classic(self, position, **kwargs):
		if self.qubic.get_pion(position) == PionBlanc:
			return VuePion(position, self.qubic,
			               model='sphere',
			               # texture='shore',
			               color=color.white,
			               highlight_color=color.lime,
			               **kwargs)
		else:
			return VuePion(position, self.qubic,
			               model='sphere',
			               # texture='shore',
			               color=color.black,
			               highlight_color=color.lime,
			               **kwargs)
