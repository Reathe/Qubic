from abc import ABC, abstractmethod

from ursina import *


class Qamera(Entity, ABC):
	def __init__(self, **kwargs):
		super().__init__(name='qamera', **kwargs)

	@abstractmethod
	def set_default_settings(self):
		"""
		Met tous les paramètres de la caméra aux valeurs par défaut
		"""
		raise NotImplementedError

	@abstractmethod
	def save_settings(self):
		raise NotImplementedError

	@abstractmethod
	def load_settings(self):
		raise NotImplementedError

	@abstractmethod
	def reset_to_start(self):
		"""
		Met la caméra à la position à laquelle elle était au début de la partie (à sa création)
		"""
		raise NotImplementedError

	def update(self):
		pass

	def input(self, key):
		pass