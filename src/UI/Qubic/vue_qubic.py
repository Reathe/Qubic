from typing import List, Optional

from ursina import *

from controls import Controls, Map
from qubic_observer import QubicObserver
from ui.qamera.qamera_locked import QameraLocked
from ui.qubic.vue_pion import VuePion, VuePionFactory
from composite import Composite


class _Floor(Composite):
	def __init__(self, qubic, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for z in range(len(qubic)):
			for x in range(len(qubic)):
				m = Map.MapPart(qubic,
				                (x, 0, z),
				                model='cube',
				                origin=(0, 0.5),
				                position=(x, 0, z),
				                texture='white_cube',
				                color=color.white,
				                parent=self)
				m.scale_y = 0.5
				m.y = m.y * m.scale[1]
				self.components.append(m)

	def toggle_on_click(self):
		for sol in self.components:
			sol.toggle_on_click()

	def add_observers(self, *observers):
		for sol in self.components:
			sol.add_observers(*observers)


class _VueQubicSettings:
	def __init__(self):
		super().__init__()
		self.center = None
		self.vue_pion = 'Classic'
		self.control_method = 'Mouse'
		self.qamera_type = QameraLocked


class VueQubic(Composite, QubicObserver):
	pions: List[List[List[Optional[VuePion]]]]

	def __init__(self, qubic, *args, **kwargs):
		super().__init__(*args, **kwargs)
		taille = len(qubic)
		self.qubic = qubic
		qubic.add_observers(self)
		# TODO: controls depending on camera's position/angle
		self.settings = _VueQubicSettings()
		target = (taille / 2 - .5, 0, taille / 2 - .5)
		self.qamera = self.settings.qamera_type(target)
		sol = _Floor(qubic)
		self.components.append(sol)
		controls_type = Controls.get_controls(self.settings.control_method)
		self.controls = controls_type(qubic, self)
		self.components.append(self.controls)
		sol.add_observers(self.controls)
		self.pions = [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]

	# print("rota: {}".format(self.plateau))

	def notify(self, qubic):
		for x in range(len(qubic)):
			for y in range(len(qubic)):
				for z in range(len(qubic)):
					pion = qubic.plateau[x][y][z]
					if pion and self.pions[x][y][z] is None:
						self.pions[x][y][z] = VuePionFactory(qubic, self.settings.vue_pion).create_pion((x, y, z))
						self.components.append(self.pions[x][y][z])
					elif pion is None and self.pions[x][y][z]:
						self.components.remove(self.pions[x][y][z])
						destroy(self.pions[x][y][z])
						self.pions[x][y][z] = None
