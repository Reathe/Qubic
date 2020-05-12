from abc import ABC, abstractmethod
from random import randint
from typing import Union, Tuple, Optional

from model.curseur import Curseur
from model.qubic import Qubic
from qubic_settings import Settings


class QubicAISettings(Settings):
	def __init__(self, *args, **kwargs):
		super().__init__('QubicAISettings', *args, **kwargs)
		self.default()

	def default(self):
		self.ai_type = 'AlphaBeta'

	def get_ai(self) -> 'AI':
		ai_dict = {
			'AlphaBeta': AlphaBeta,
			'Random': Random
		}
		return ai_dict[self.ai_type]()


class AI(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@abstractmethod
	def play(self, qubic: Qubic) -> Optional[Union[Curseur, Tuple[int, int, int]]]:
		pass


class Random(AI):
	def play(self, qubic: Qubic) -> Optional[Union[Curseur, Tuple[int, int, int]]]:
		if not qubic.fini:
			ind = randint(0, len(qubic.posable) - 1)
			pos = qubic.posable[ind]
			return pos


class AlphaBeta(AI):
	def play(self, qubic: Qubic) -> Optional[Union[Curseur, Tuple[int, int, int]]]:
		pass
