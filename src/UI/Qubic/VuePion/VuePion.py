from ursina import *


class VuePion(Button):
	def __init__(self, qubic, **kwargs):
		self.qubic = qubic
		super().__init__(
			model='sphere',
			texture='shore',
			color=color.white,
			highlight_color=color.lime,
			**kwargs
		)

	def on_click(self):
		pos = tuple(self.position + (0, 1, 0))
		pos = int(pos[0]), int(pos[0]), int(pos[2])
		pos = self.qubic.get_pos_with_gravity(pos)
		print(pos)
		self.qubic.poser(pos)
