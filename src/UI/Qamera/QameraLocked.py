from typing import Tuple

from math import cos, sin, pi
from ursina import *

from UI.Qamera.Qamera import Qamera
from UI.Qamera.QameraLockedSettings import QameraLockedSettings
from model.Direction import mult_dir


# noinspection PyTypeChecker
def print_infos(cam):
	print()
	print('parents: {}'.format(cam.parent))
	print('world_pos: {}'.format(cam.world_position))
	print('pos: {}'.format(cam.position))
	print('rayon: {0:.0f}'.format(cam.rayon))
	print('world_rotation: {}'.format(mult_dir(1 / pi, mult_dir(pi / 180, cam.world_rotation))))
	print('rotation: {}'.format(mult_dir(1 / pi, mult_dir(pi / 180, cam.rotation))))
	print('alpha: {0:.2f}, beta: {1:.2f}'.format(cam.alpha / pi, cam.beta / pi))
	print('x:{0:.2f}, y:{1:.2f}, z:{2:.2f}'.format(cam.x, cam.y, cam.z))


class QameraLocked(Qamera):
	"""
	Une caméra qui tourne autour d'un cible. La cible est (0,0,0) par défaut.
	"""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		camera.parent = self
		camera.position = (0, 0, 0)
		self.alpha = None
		self.beta = None
		self.rayon = None
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

		return x, y, z

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
