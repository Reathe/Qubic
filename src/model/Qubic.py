from typing import Tuple

import itertools
import numpy

from model.Pion import Pion
from model.Pion.PionBlanc import PionBlanc
from model.Pion.PionNoir import PionNoir


class Qubic:
	"""
	Les blancs commencent toujours... Comme aux échecs :)
	"""

	def __init__(self, taille: int = 4):
		# self._curseur = Curseur((taille, taille, taille))
		self._plateau = [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]
		self._posable = list(itertools.product((i for i in range(len(self))), repeat=3))
		self._pose = []

	def __len__(self):
		return len(self._plateau)

	@property
	def taille(self):
		"""
		Returns:
			La taille du plateau
		"""
		return len(self)

	def get_pion(self, pos: Tuple[int, int, int]) -> Pion:
		"""
		Retourne le pion à la position pos_max
		Args:
			pos: La position

		Returns:
			Le pion
		"""
		return self._plateau[pos[0]][pos[1]][pos[2]]

	def poser(self, pos: Tuple[int, int, int]):
		if self.get_pion(pos) is None:
			pion_tour_blanc = {True: PionBlanc(), False: PionNoir()}
			self._plateau[pos[0]][pos[1]][pos[2]] = pion_tour_blanc.get(self.tour_blanc())
			self._posable.remove(pos)
			self._pose.append(pos)

	def tour_blanc(self) -> bool:
		return (len(self._pose) % 2 == 0) and len(self) ** 3 > len(self._pose)

	def tour_noir(self) -> bool:
		return len(self) ** 3 > len(self._pose) and not self.tour_blanc()

	@property
	def plateau(self):
		return self._plateau


def to_1d(pos, pos_max):
	return numpy.ravel_multi_index(pos, pos_max)


def to_3d(ind, pos_max):
	return numpy.unravel_index(ind, pos_max)


if __name__ == '__main__':
	Qbic = Qubic()
	Qbic.poser((0, 0, 0))
	print(numpy.asarray(Qbic.plateau))
