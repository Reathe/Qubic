from panda3d.core import *

from composite import Composite


class Lights(Composite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		render.setShaderAuto()
		alight = AmbientLight('alight')
		alight.setColor(0.45)
		alnp = render.attachNewNode(alight)
		self.ambient = alnp
		self.components.append(self.ambient)

		dlight = DirectionalLight('dlight')
		dlight.setColor((0.35, 0.35, 0.35, 1))
		dlnp = render.attachNewNode(dlight)
		dlnp.setHpr(0, 230, 0)
		self.sun = dlnp
		self.components.append(self.sun)

		plight = PointLight('plight')
		plight.setColor(1)
		plight.setAttenuation((1, 0, 0.025))
		# plight.setShadowCaster(True, 1024, 1024)
		plnp = render.attachNewNode(plight)
		x, y, z = 0, 10, -3
		plnp.setPos(x, z, y)

		self.point = plnp
		self.components.append(self.point)
		self.lights_on()

	# Entity(model='bulb', scale=0.01, position=(x, y, z), origin=(0, -0.5))

	def lights_on(self):
		for light in self.components:
			render.setLight(light)

	def lights_off(self):
		for light in self.components:
			render.clearLight(light)

	def on_destroy(self):
		self.lights_off()
		super().on_destroy()
