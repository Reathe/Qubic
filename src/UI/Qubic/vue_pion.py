from ursina import *

from model.pion import PionBlanc, PionNoir


class VuePion(Entity):
	def __init__(self, position, qubic, *args, **kwargs):
		self.qubic = qubic
		super().__init__(
			position=position,
			*args, **kwargs
		)


class VuePionFactory:
	def __init__(self, qubic, pion='Classic'):
		"""
		Args:
			pion: le type de pion (le skin)
			qubic: le qubic
		"""
		super().__init__()
		pion_types = {'Classic': self.create_classic}
		self.create_pion = pion_types.get(pion)
		self.qubic = qubic

	def create_classic(self, position, **kwargs):
		vp = VuePion(position, self.qubic,
		             model='classic',
		             origin=(0, -0.5),
		             # texture='classic',
		             **kwargs)
		vp.scale = 0.5
		vp.y = vp.y * vp.scale[1]
		if self.qubic.get_pion(position) == PionBlanc:
			vp.color = color.white
		elif self.qubic.get_pion(position) == PionNoir:
			vp.color = color.dark_gray
		else:
			vp.color = color.black50
		return vp
