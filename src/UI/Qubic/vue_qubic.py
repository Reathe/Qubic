from typing import List, Optional

from ursina import *

from qubic_observer import QubicObserver
from ui.qubic.vue_pion import VuePion, VuePionFactory


class _Sol(Button):
	def __init__(self, qubic, **kwargs):
		self.qubic = qubic
		super().__init__(
			model='cube',
			texture='white_cube',
			highlight_color=color.lime,
			**kwargs
		)

	def on_click(self):
		pos = tuple(self.position + Vec3(0, len(self.qubic), 0))
		pos = int(pos[0]), int(pos[1]), int(pos[2])
		pos = self.qubic.get_pos_with_gravity(pos)
		self.qubic.poser(pos)


class _VueQubicSettings:
	def __init__(self):
		super().__init__()
		self.center = None
		self.vue_pion = 'Classic'


class VueQubic(Entity, QubicObserver):
	pions: List[List[List[Optional[VuePion]]]]

	def __init__(self, qubic, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def __init__(self, qubic, **kwargs):
		super().__init__(**kwargs)
		taille = len(qubic)
		self.qubic = qubic
		qubic.add_observers(self)
		self.settings = _VueQubicSettings()
		self.pions = [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]
		for z in range(taille):
			for x in range(taille):
				_Sol(self.qubic, position=(x, -1, z), parent=self)

	# print("rota: {}".format(self.plateau))

	def notify(self, qubic):
		for x in range(len(qubic)):
			for y in range(len(qubic)):
				for z in range(len(qubic)):
					pion = qubic.plateau[x][y][z]
					if pion and self.pions[x][y][z] is None:
						self.pions[x][y][z] = VuePionFactory(qubic, self.settings.vue_pion).create_pion((x, y, z))
					elif pion is None and self.pions[x][y][z]:
						destroy(self.pions[x][y][z])
