from typing import List, Optional

from ursina import *

from controls import Controls
from qubic_observer import QubicObserver
from ui.qamera.qamera_locked import QameraLocked
from ui.qubic.vue_pion import VuePion, VuePionFactory
from composite import Composite


class _Sol(Button):
	def __init__(self, qubic, **kwargs):
		self.qubic = qubic
		super().__init__(
			model='cube',
			texture='white_cube',
			color=color.white,
			**kwargs
		)
		self.__next = self.__controle_on_click, self.color.tint(-0.2), self.color.tint(-0.4), 1
		self.on_click, self.highlight_color, self.pressed_color, self.pressed_scale = None, self.color, self.color, 1

	def __controle_on_click(self):
		pos = tuple(self.position + Vec3(0, len(self.qubic), 0))
		pos = int(pos[0]), int(pos[1]), int(pos[2])
		pos = self.qubic.get_pos_with_gravity(pos)
		self.qubic.poser(pos)

	def toggle_on_click(self):
		temp = self.__next
		on_click = None if temp[0] else self.__controle_on_click
		self.__next = on_click, self.highlight_color, self.pressed_color, self.pressed_scale
		self.on_click, self.highlight_color, self.pressed_color, self.pressed_scale = temp


class _VueQubicSettings:
	def __init__(self):
		super().__init__()
		self.center = None
		self.vue_pion = 'Classic'
		self.control_method = 'Keyboard'
		self.qamera_type = QameraLocked


class VueQubic(Composite, QubicObserver):
	pions: List[List[List[Optional[VuePion]]]]

	def __init__(self, qubic, *args, **kwargs):
		super().__init__(*args, **kwargs)
		taille = len(qubic)

		self.qubic = qubic
		qubic.add_observers(self)

		self.settings = _VueQubicSettings()
		target = (taille/2-.5, 0, taille/2-.5)
		self.qamera = self.settings.qamera_type(target)
		controls_type = Controls.get_controls(self.settings.control_method)
		self.controls = controls_type(qubic, self.settings.vue_pion)
		self.components.append(self.controls)

		self.pions = [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]
		for z in range(taille):
			for x in range(taille):
				self.components.append(_Sol(qubic, position=(x, -1, z), parent=scene))

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
