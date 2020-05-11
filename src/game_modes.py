from abc import ABC

from ursina import *

from controls import LocalController, OnlineController
from model.qubic import Qubic
from networking.client import Client
from ui.qubic.vue_qubic import VueQubic


class QubicMode(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


class OneVOne(QubicMode):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = Qubic()
		self.vue = VueQubic(self.qubic, LocalController(self.qubic))


class Online(QubicMode):
	def __init__(self, client: Client, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client = client
		self.qubic = Qubic()
		self.vue = VueQubic(self.qubic, OnlineController(self.client))
		self.auto_update = Sequence(0.1, Func(update_qubic, self), loop=True)
		self.auto_update.start()


def update_qubic(self):
	obs = self.qubic.observers
	self.qubic = self.client.get_qubic()
	self.qubic.add_observers(*obs)
	self.qubic.notify_observers()
