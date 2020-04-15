from abc import ABC

from ursina import *

from model.qubic import Qubic
from ui.qubic.vue_qubic import VueQubic


class QubicMode(ABC):
	def __init__(self):
		pass


class OneVOne(QubicMode):
	def __init__(self):
		super().__init__()
		self.qubic = Qubic()
		self.vue = VueQubic(self.qubic)
