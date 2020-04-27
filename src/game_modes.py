from abc import ABC

from model.qubic import Qubic
from ui.qubic.vue_qubic import VueQubic


class QubicMode(ABC):
	def __init__(self):
		self.qubic = Qubic()
		self.vue = VueQubic(self.qubic)


class OneVOne(QubicMode):
	def __init__(self):
		super().__init__()
