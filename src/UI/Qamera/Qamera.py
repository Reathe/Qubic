from abc import abstractmethod

from ursina import *

from qubic_observer import QubicSubject


class Qamera(QubicSubject, Entity):
	def __init__(self, *args, **kwargs):
		super().__init__(name='qamera', *args, **kwargs)

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
