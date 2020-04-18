from typing import Tuple
import json
from math import cos, sin, pi

from ursina import *

from model.direction_tools import mult_dir, add_dir
from ui.qamera.qamera import Qamera


class QameraLocked(Qamera):
	"""
	Une caméra qui tourne autour d'un cible.
	"""

	def __init__(self, target=(0, 0, 0), *args, **kwargs):
		super().__init__(*args, **kwargs)
		camera.parent = self
		camera.position = (0, 0, 0)
		self.alpha = None
		self.beta = None
		self.rayon = None
		self.target = target
		self.__settings = QameraLockedSettings()
		try:
			self.load_settings()
		except:
			self.set_default_settings()
			self.save_settings()

		self.update_pos()

	@property
	def rayon(self):
		return self.__r_cam

	@rayon.setter
	def rayon(self, r):
		if not r < 0:
			self.__r_cam = r

	@property
	def alpha(self):
		return self.__alpha_cam

	@alpha.setter
	def alpha(self, alpha):
		self.__alpha_cam = alpha
		self.__alpha_cam %= pi * 2

	@property
	def beta(self):
		return self.__beta_cam

	@beta.setter
	def beta(self, beta):
		if 0 <= beta <= pi / 2:
			self.__beta_cam = beta

	def reset_to_start(self):
		self.alpha = self.__settings.start_alpha
		self.beta = self.__settings.start_beta
		self.rayon = self.__settings.start_r

	@property
	def pos_xyz(self) -> Tuple[float, float, float]:
		# les axes x et z sont décidés par alpha et beta

		x = cos(self.alpha) * sin(self.beta) * self.rayon
		z = sin(self.alpha) * sin(self.beta) * self.rayon

		# beta est le seul paramètre de l'axe y
		y = cos(self.beta) * self.rayon

		return add_dir((x, y, z), self.target)

	def update_pos(self):
		"""
		Synchronise la position réelle de la camera
		avec les paramètres alpha et beta qui la representent
		"""
		self.position = self.pos_xyz
		self.rotation_x = (pi / 2 - self.beta) * 180 / pi
		self.rotation_y = -(pi / 2 + self.alpha) * 180 / pi

	def update(self):
		if mouse.left:
			self.alpha -= mouse.velocity[0] * self.__settings.sensibilite
			self.beta += mouse.velocity[1] * self.__settings.sensibilite
		# print_infos(self)
		self.update_pos()

	def input(self, key):
		"""
		Ursina function: la fonction appelée lorsqu'on appuie sur une touche

		Args:
			key: la touche
		"""
		if key == 'scroll up':
			self.rayon -= self.__settings.zoom_sensibilite
		elif key == 'scroll down':
			self.rayon += self.__settings.zoom_sensibilite
		elif key == 's':
			stgs = self.__settings
			stgs.start_alpha, stgs.start_beta, stgs.start_r = self.alpha, self.beta, self.rayon
			self.save_settings()

	def set_default_settings(self):
		self.__settings.default()
		self.reset_to_start()
		self.update_pos()

	def save_settings(self):
		self.__settings.save()

	def load_settings(self):
		self.__settings.load()
		self.reset_to_start()
		self.update_pos()


class QameraLockedSettings:
	def __init__(self):
		super().__init__()
		self.start_alpha = None
		self.start_beta = None
		self.start_r = None
		self.sensibilite = None
		self.zoom_sensibilite = None

	def default(self):
		self.start_alpha = 3 * pi / 4
		self.start_beta = pi / 4
		self.start_r = 20
		self.sensibilite = 1
		self.zoom_sensibilite = 5

	def save(self):
		print("Saving camera locked settings...")
		try:
			with open('QameraLockedSettings.json', 'w') as file:
				json.dump(self.__dict__, file)
		except:
			print("Failed to save")
			raise IOError

	def load(self):
		print("Loading camera locked settings...")
		try:
			with open('QameraLockedSettings.json', 'r') as file:
				self.__dict__ = json.load(file)
		except:
			print("Failed")
			raise IOError


# noinspection PyTypeChecker
def print_infos(qam):
	print()
	print('parents: {}'.format(qam.parent))
	print('world_pos: {}'.format(qam.world_position))
	print('pos: {}'.format(qam.position))
	print('rayon: {0:.0f}'.format(qam.rayon))
	print('world_rotation: {}'.format(mult_dir(1 / pi, mult_dir(pi / 180, qam.world_rotation))))
	print('rotation: {}'.format(mult_dir(1 / pi, mult_dir(pi / 180, qam.rotation))))
	print('alpha: {0:.2f}, beta: {1:.2f}'.format(qam.alpha / pi, qam.beta / pi))
	print('x:{0:.2f}, y:{1:.2f}, z:{2:.2f}'.format(qam.x, qam.y, qam.z))


"""main pour tester la camera"""
if __name__ == '__main__':
	window.borderless = False
	app = Ursina()


	class Voxel(Button):
		def __init__(self, position=(0, 0, 0)):
			super().__init__(
				parent=scene,
				position=position,
				model='cube',
				texture='white_cube',
				color=color.rgb(*mult_dir(10, position)),
				highlight_color=color.lime,
			)

		def input(self, key):
			if self.hovered:
				if key == 'left mouse down':
					Voxel(position=self.position + mouse.normal)

				if key == 'right mouse down':
					destroy(self)


	for z in range(8):
		for x in range(8):
			voxel = Voxel(position=(x, 0, z))
	for y in range(8):
		Voxel(position=(0, y, 0))

	qamera = QameraLocked(model='cube', collider='box', texture='white_cube', color=color.blue,
	                      highlight_color=color.lime)
	ed_cam = EditorCamera(enabled=False)

	position_info = Text(position=window.top_left)


	def update():
		if mouse.hovered_entity:
			position_info.text = '{}'.format(mouse.hovered_entity.world_position)


	change_pos_cam = qamera.update_pos


	def change_cam():
		if qamera.update_pos():
			qamera.update_pos = change_pos_cam
		else:
			qamera.update_pos = lambda: True
		ed_cam.enabled = not ed_cam.enabled


	qamera.on_click = change_cam


	def input(key):
		if key == 'tab':
			change_cam()


	app.run()
