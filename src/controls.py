from composite import Composite
from model.curseur import Curseur
from model.direction_tools import DERRIERE, DEVANT, GAUCHE, DROITE
from qubic_observer import QubicObserver
from ui.qubic.vue_pion import VuePionFactory


class Controls(QubicObserver, Composite):
	def __init__(self, qubic, vue, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = qubic
		taille = self.qubic.taille
		self.curseur = Curseur((taille,) * 3)
		self.vue_curseur = VuePionFactory(qubic, vue.settings.vue_pion).create_pion((0, 0, 0))
		self.components.append(self.vue_curseur)

	@staticmethod
	def get_controls(controls_type):
		link = {'Keyboard': ControlsKeyboard,
		        'Mouse': ControlsMouse
		        }
		return link.get(controls_type)

	def maj_vue(self):
		self.vue_curseur.position = self.curseur.pos
		self.vue_curseur.y *= 0.5

	def notify(self, truc):
		pass


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


class ControlsMouse(Controls):
	def __init__(self, qubic, vue, *args, **kwargs):
		super().__init__(qubic, vue, *args, **kwargs)
		for c in vue.components:
			if hasattr(c, 'toggle_on_click'):
				try:
					c.toggle_on_click()
				except Exception as ex:
					print(f"error on toggling buttons: {ex}")

	def notify(self, position):
		self.curseur.pos = int(position[0]), self.qubic.taille - 1, int(position[2])
		self.curseur.pos = self.qubic.get_pos_with_gravity(self.curseur)
		self.maj_vue()
