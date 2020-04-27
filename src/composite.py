from abc import ABC
from typing import List

from ursina import *


class Composite(ABC, Entity):
	__components: List[Entity]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__components = []

	@property
	def components(self) -> List[Entity]:
		"""
		components of the composite objects
		"""
		return self.__components

	def setattr_components(self, **kwargs):
		"""
		sets the attributes to all components

		Exemple:
			comp.setattr_components(text='21', position=(0, 0, 0))

		Args:
			**kwargs: dict of attributes
		"""
		for key, value in kwargs.items():
			for c in self.components:
				setattr(c, key, value)

	def on_destroy(self):
		self._destroy_components()

	def _destroy_components(self):
		"""
		calls destroy oen every component
		"""
		for c in self.components:
			try:
				destroy(c)
			except Exception as ex:
				print(f'exception {ex} while destroying {c}')
		self.components.clear()
