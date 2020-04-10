from ursina import *

from UI.Qubic.VuePion.VuePion import VuePion
from model.Pion.PionBlanc import PionBlanc


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
			               #texture='shore',
			               color=color.white,
			               highlight_color=color.lime,
			               **kwargs)
		else:
			return VuePion(position, self.qubic,
			               model='sphere',
			               #texture='shore',
			               color=color.black,
			               highlight_color=color.lime,
			               **kwargs)
