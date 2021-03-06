import string
from abc import ABC, abstractmethod
from math import atan2, cos, pi, sin
from threading import Thread

from ursina import *

from composite import Composite
from model.ai import QubicAISettings
from model.curseur import Curseur
from model.direction_tools import DERRIERE, DEVANT, DROITE, GAUCHE
from qubic_observer import QubicObserver, QubicSubject
from ui.qubic.vue_pion import VuePionFactory


class Controller(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, *kwargs)

	@abstractmethod
	def place_piece(self, pos):
		pass


class EmptyController(Controller):
	def place_piece(self, pos):
		pass


class LocalController(Controller):
	def __init__(self, qubic, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = qubic

	def place_piece(self, pos):
		self.qubic.poser(pos)


class LocalAIController(LocalController):
	def __init__(self, qubic, *args, **kwargs):
		super().__init__(qubic, *args, **kwargs)
		self.settings = QubicAISettings()
		self.thread = None
		try:
			self.settings.load()
		except IOError:
			self.settings.default()
			self.settings.save()
		self.ai = self.settings.get_ai()

	def place_piece(self, pos):
		if not self.thread or not self.thread.is_alive():
			self.thread = Thread(target=self.__place_piece, args=(pos,))
			self.thread.start()

	def __place_piece(self, pos):
		len_pose = len(self.qubic.pose)
		super().place_piece(pos)
		if len(self.qubic.pose) > len_pose:
			self.find_and_place()

	def find_and_place(self):
		pos = self.ai.play(self.qubic)
		if pos:
			super().place_piece(pos)


class OnlineController(Controller):
	def __init__(self, client, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client = client

	def place_piece(self, pos):
		t = Thread(target=self.__place_piece, args=(pos,)).start()

	def __place_piece(self, pos):
		if not self.client.qubic_place(pos):
			# TODO: show to user
			print("Place error")


class Controls(QubicObserver, Composite):
	def __init__(self, qubic, vue, controller, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = qubic
		self.controller = controller
		taille = self.qubic.taille
		self.curseur = Curseur((taille,) * 3)
		self.vue_curseur = VuePionFactory(qubic, vue.settings.vue_pion).create_pion((0, 0, 0))
		self.components.append(self.vue_curseur)
		x, y = vue.settings.control_map_position
		x, y = ((x - 50) / 100) * window.aspect_ratio, (y - 50) / 100
		_map = Map(qubic, controller, position=(x, y))
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
		self.curseur.pos = int(position[0]), self.qubic.taille - 1, int(position[2])
		self.curseur.pos = self.qubic.get_pos_with_gravity(self.curseur)
		self.maj_vue()


class ControlsKeyboard(Controls):
	def __init__(self, qubic, vue, controller, *args, **kwargs):
		super().__init__(qubic, vue, controller, *args, **kwargs)
		vue.qamera.add_observers(self)
		self.angle = 0

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

		def rotate(vect, angle):
			"""
			rotates the vector by the angle relative to the x and z axis, for exemple if vect=(1,0,0)
			and angle = pi/2, then vect will rotate by 45 degrees making a (0,0,-1) vector
			Args:
				vect: the initial direction vector
				angle: the angle of rotation

			Returns: the new angle

			"""
			if vect == (0, 0, 0):
				return vect
			x, y, z = vect
			theta = atan2(z, x) - angle
			x, z = round(cos(theta)), round(sin(theta))
			return x, y, z

		vect = rotate(vect, self.angle)

		if self.curseur.valid_move(vect):
			self.curseur += vect
			self.curseur.pos = self.qubic.get_pos_with_gravity(self.curseur)
			self.maj_vue()
		if key == 'enter':
			self.controller.place_piece(self.curseur)
			self.curseur.pos = self.qubic.get_pos_with_gravity(self.curseur)
			self.maj_vue()

	def notify(self, angle):
		try:
			super().notify(angle)
		except:
			if self.angle != (angle % 360) / 180 * pi:
				self.angle = (angle % 360) / 180 * pi


class ControlsMouse(Controls):
	def __init__(self, qubic, vue, controller, *args, **kwargs):
		super().__init__(qubic, vue, controller, *args, **kwargs)
		vue.board.add_observers(self)
		for c in vue.components:
			if hasattr(c, 'toggle_on_click'):
				try:
					c.toggle_on_click()
				except Exception as ex:
					print(f"error on toggling buttons: {ex}")


class Map(Composite):
	class MapPart(QubicSubject, Button):
		def __init__(self, qubic, real_pos, controller, *args, **kwargs):
			super().__init__(
				*args,
				**kwargs
			)
			self.controller = controller
			self.qubic = qubic
			self.real_pos = real_pos
			# toggle on click
			self.__next = self.__controle_on_click, self.color.tint(-0.2), self.color.tint(-0.4), 1
			self.on_click, self.highlight_color, self.pressed_color, self.pressed_scale = None, self.color, self.color, 1

		@property
		def real_pos(self):
			return self._real_pos

		@real_pos.setter
		def real_pos(self, value):
			self._real_pos = value
			# tooltip
			if len(self.qubic) <= 26:
				p = string.ascii_uppercase[self.real_pos[0]], self.real_pos[2] + 1
				self.tooltip = Tooltip("{}{}".format(*p))
			else:
				p = self.real_pos[0] + 1, self.real_pos[2] + 1
				self.tooltip = Tooltip("{},{}".format(*p))

		def __controle_on_click(self):
			pos = self.qubic.get_pos_with_gravity(self.real_pos)
			pos = pos[0], len(self.qubic) - 1, pos[2]
			self.controller.place_piece(pos)
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
			for ob in self.observers:
				ob.notify(self.real_pos)

	def __init__(self, qubic, controller, origin=(0.5, 0), *args, **kwargs):
		super().__init__(*args, **kwargs, parent=camera.ui)
		for z in list(range(len(qubic))):
			for x in list(range(len(qubic)))[::-1]:
				m = self.MapPart(qubic, (x, 0, z),
				                 controller,
				                 model='quad',
				                 scale=.2 / len(qubic),
				                 texture='white_cube',
				                 color=color.white,
				                 parent=self)
				# m.text = m.tooltip.text
				# m.text_entity.color = color.black
				self.components.append(m)
		grid_layout(self.components, len(qubic), len(qubic), origin=origin)

	def toggle_on_click(self):
		for sol in self.components:
			sol.toggle_on_click()

	def add_observers(self, *observers):
		for sol in self.components:
			sol.add_observers(*observers)
