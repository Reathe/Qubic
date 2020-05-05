from ursina import *

from composite import Composite


class OnlineMenu(Composite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.components.append(self.__titre())

	def __titre(self, **kwargs):
		return Text(text='Qubic',
		            position=(0 * window.aspect_ratio, 0.25),
		            origin=(0, 0),
		            scale=2,
		            **kwargs)
