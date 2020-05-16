from abc import ABC, abstractmethod
from copy import deepcopy
from random import randint
from typing import Optional, Tuple, Union

from ursina import *

from model.curseur import Curseur
from model.pion import PionBlanc, PionNoir
from model.qubic import Qubic
from qubic_settings import Settings


class QubicAISettings(Settings):
	def __init__(self, *args, **kwargs):
		super().__init__('QubicAISettings', *args, **kwargs)
		self.default()

	def default(self):
		self.ai_type = 'NegaMax'

	def get_ai(self) -> 'AI':
		ai_dict = {
			'NegaMax': NegaMax,
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


def _val(qubic):
	val = 0
	if qubic.winner == PionBlanc:
		val = -64  # - (len(qubic.pose) // 2 + len(qubic.pos) % 2)
	elif qubic.winner == PionNoir:
		val = 64
	return val


class NegaMax(AI):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.opp = None
		self.notify = None
		self.best_move = None
		self.depth = None
		self.text = None

	def play(self, qubic: Qubic, notify=False) -> Optional[Union[Curseur, Tuple[int, int, int]]]:
		b = -65
		self.notify = notify
		self.depth = 0
		self.best_move = None
		self.opp = (len(qubic.pose) + 1) % 2
		self._nega_max(qubic if self.notify else deepcopy(qubic), b)
		return self.best_move

	def _nega_max(self, qubic: Qubic, mini_score):
		if qubic.fini or self.depth == 4:
			if self.depth % 2 == self.opp:
				return -_val(qubic)  # opp node
			else:
				return _val(qubic)  # play node
		best_score = -999
		possible_moves = deepcopy(qubic.posable)
		for pos in possible_moves:
			# if self.depth == 0:
			# 	if self.text:
			# 		destroy(self.text)
			# 	self.text = Text(f'Calculating... ({(possible_moves.index(pos) / len(possible_moves)) * 100}%)',
			# 	                 origin=(-0.5, 0), position=(-0.5 * window.aspect_ratio, 0.4))
			qubic.poser(pos, notify=self.notify)
			self.depth += 1
			current_score = self._nega_max(qubic, best_score)
			self.depth -= 1
			if self.notify:
				time.sleep(0.07)
			qubic.annule_coup(self.notify)
			if current_score > best_score or (current_score == best_score and randint(0, 99) < 0):
				best_score = current_score
				if self.depth == 0:
					self.best_move = pos
			if -best_score <= mini_score:
				return -best_score
		return -best_score
