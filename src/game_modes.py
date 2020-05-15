from abc import ABC
from random import randint

from ursina import *

from controls import LocalAIController, LocalController, OnlineController
from model.qubic import Qubic
from networking.client import Client
from ui.qubic.vue_qubic import VueQubic


class QubicMode(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.qubic = Qubic()


class OneVOne(QubicMode):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.vue = VueQubic(self.qubic, LocalController(self.qubic))


class Online(QubicMode):
	def __init__(self, client: Client, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client = client
		self.vue = VueQubic(self.qubic, OnlineController(self.client))
		self.auto_update = Sequence(0.1, Func(self.update_qubic), loop=True)
		self.auto_update.start()

	def update_qubic(self):
		obs = self.qubic.observers
		self.qubic.__dict__ = self.client.get_qubic().__dict__
		self.qubic.remove_observers()
		self.qubic.add_observers(*obs)
		self.qubic.notify_observers()
		self.vue.controls.notify(self.vue.controls.curseur.pos)


class OneVSAI(QubicMode):
	def __init__(self, ai_start: bool = None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		controller = LocalAIController(self.qubic)
		self.vue = VueQubic(self.qubic, controller)
		if ai_start is True or (ai_start is None and randint(0, 99) < 50):
			controller.find_and_place()
