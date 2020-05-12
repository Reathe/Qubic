from abc import ABC, abstractmethod
from typing import Union, Tuple, Optional

from model.curseur import Curseur
from qubic_settings import Settings


class QubicAISettings(Settings):
	def __init__(self, *args, **kwargs):
		super().__init__('QubicAISettings', *args, **kwargs)
		self.default()

	def default(self):
		self.ai_type = 'AlphaBeta'

	def get_ai(self) -> 'AI':
		ai_dict = {
			'AlphaBeta': AlphaBeta
		}
		return ai_dict[self.ai_type]()


class AI(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@abstractmethod
	def play(self, qubic) -> Optional[Union[Curseur, Tuple[int, int, int]]]:
		pass


class AlphaBeta(AI):
	def play(self, qubic) -> Optional[Union[Curseur, Tuple[int, int, int]]]:
		pass
