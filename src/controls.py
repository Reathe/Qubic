import string

from ursina import *

from composite import Composite
from model.curseur import Curseur
from model.direction_tools import DERRIERE, DEVANT, GAUCHE, DROITE
from qubic_observer import QubicObserver, QubicSubject
from ui.qubic.vue_pion import VuePionFactory


class Controls(QubicObserver, Composite):
	def __init__(self, qubic, vue, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = qubic
		taille = self.qubic.taille
		self.curseur = Curseur((taille,) * 3)
		self.vue_curseur = VuePionFactory(qubic, vue.settings.vue_pion).create_pion((0, 0, 0))
		self.components.append(self.vue_curseur)
		_map = Map(qubic, position=(0.5, 0.3, 0))
		_map.toggle_on_click()
		_map.add_observers(self)
		self.components.append(_map)

	@staticmethod
	def get_controls(controls_type):
		link = {'Keyboard': ControlsKeyboard,
		        'Mouse': ControlsMouse
		        }
		return link.get(controls_type)

	def maj_vue(self):
		self.vue_curseur.position = self.curseur.pos
		self.vue_curseur.y *= self.vue_curseur.scale_y

	def notify(self, position):
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


class Map(Composite):
	class MapPart(QubicSubject, Button):
		def __init__(self, qubic, real_pos, *args, **kwargs):
			super().__init__(
				*args,
				**kwargs
			)
			self.qubic = qubic
			self.real_pos = real_pos
			# tooltip
			p = string.ascii_uppercase[real_pos[0]], real_pos[2] + 1
			self.tooltip = Tooltip("{}{}".format(*p))
			# toggle on click
			self.__next = self.__controle_on_click, self.color.tint(-0.2), self.color.tint(-0.4), 1
			self.on_click, self.highlight_color, self.pressed_color, self.pressed_scale = None, self.color, self.color, 1

		def __controle_on_click(self):
			pos = self.qubic.get_pos_with_gravity(self.real_pos)
			pos = pos[0], len(self.qubic) - 1, pos[2]
			self.qubic.poser(pos)
			self.notify_observers()

		def toggle_on_click(self):
			temp = self.__next
			on_click = None if temp[0] else self.__controle_on_click
			self.__next = on_click, self.highlight_color, self.pressed_color, self.pressed_scale
			self.on_click, self.highlight_color, self.pressed_color, self.pressed_scale = temp

		def on_mouse_enter(self):
			super().on_mouse_enter()
			self.notify_observers()

		def notify_observers(self):
			self.observers[0].notify(self.real_pos)

	def __init__(self, qubic, *args, **kwargs):
		super().__init__(*args, **kwargs, parent=camera.ui)
		for z in list(range(len(qubic)))[::-1]:
			for x in range(len(qubic)):
				m = self.MapPart(qubic, (x, 0, z),
				                 model='quad',
				                 scale=0.05,
				                 texture='white_cube',
				                 color=color.white,
				                 parent=self)
				# m.text = m.tooltip.text
				# m.text_entity.color = color.black
				self.components.append(m)
		grid_layout(self.components, len(qubic), len(qubic))

	def toggle_on_click(self):
		for sol in self.components:
			sol.toggle_on_click()

	def add_observers(self, *observers):
		for sol in self.components:
			sol.add_observers(*observers)
