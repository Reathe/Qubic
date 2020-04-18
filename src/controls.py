from abc import ABC

from composite import Composite
from model.curseur import Curseur
from model.direction_tools import DERRIERE, DEVANT, GAUCHE, DROITE
from ui.qubic.vue_pion import VuePionFactory


class Controls(Composite, ABC):
	def __init__(self, qubic, vue, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = qubic
		taille = self.qubic.taille
		self.curseur = Curseur((taille,) * 3)
		self.vue_curseur = VuePionFactory(qubic, vue).create_pion((0, 0, 0), alpha=0.5)
		self.components.append(self.vue_curseur)

	@staticmethod
	def get_controls(controls_type):
		link = {'Keyboard': ControlsKeyboard,
		        'Mouse': ControlsMouse
		        }
		return link.get(controls_type)


class ControlsKeyboard(Controls):
	def __init__(self, qubic, vue, *args, **kwargs):
		super().__init__(qubic, vue, *args, **kwargs)

	def input(self, key):
		vect = (0, 0, 0)
		if key == 'down arrow':
			vect = DERRIERE
		elif key == 'up arrow':
			vect = DEVANT
		elif key == 'left arrow':
			vect = GAUCHE
		elif key == 'right arrow':
			vect = DROITE
		if self.curseur.valid_move(vect):
			self.curseur += vect
			self.curseur.pos = self.qubic.get_pos_with_gravity(self.curseur)
			self.maj_vue()
		if key == 'enter':
			self.qubic.poser(self.curseur)
			self.curseur.pos = self.qubic.get_pos_with_gravity(self.curseur)
			self.maj_vue()

	def maj_vue(self):
		self.vue_curseur.position = self.curseur.pos


class ControlsMouse(Controls):
	def __init__(self, qubic, *args, **kwargs):
		super().__init__(qubic, *args, **kwargs)
