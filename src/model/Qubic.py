from typing import Tuple, List, Optional

import itertools
import numpy

from model.Direction import DROITE, GAUCHE, HAUT, BAS, DERRIERE, DEVANT
from model.Pion.Pion import Pion
from model.Pion.PionBlanc import PionBlanc
from model.Pion.PionNoir import PionNoir


class Qubic:
	"""
	Les blancs commencent toujours... Comme aux échecs :)
	"""
	_plateau: List[List[List[Optional[Pion]]]]
	_posable: List[Tuple[int, int, int]]
	_pose: List[Tuple[int, int, int]]
	_gravite: bool
	_fini: bool

	def __init__(self, taille: int = 4, gravite: bool = True):
		# self._curseur = Curseur((taille, taille, taille))
		self._plateau = Qubic.__start_plateau(taille)
		self._posable = Qubic.__start_posable(taille)
		self._pose = []
		self._fini = False
		self._gravite = gravite

	@property
	def plateau(self) -> List[List[List[Optional[Pion]]]]:
		return self._plateau

	@property
	def fini(self) -> bool:
		return self._fini

	@property
	def taille(self) -> int:
		return len(self)

	def __len__(self):
		return len(self._plateau)

	def valid_pos(self, pos: Tuple[int, int, int]) -> bool:
		return all(map(lambda i: 0 <= i < len(self), pos))

	def get_pion(self, pos: Tuple[int, int, int]) -> Optional[Pion]:
		"""
		Retourne le pion à la position pos

		Args:
			pos: La position

		Returns:
			Le pion
		"""
		return self._plateau[pos[0]][pos[1]][pos[2]]

	def poser(self, pos: Tuple[int, int, int]):
		"""
		Pose un pion à la position pos dans le plateau si il n'y a rien
		Le type de pion posé est celui dont c'est le tour
		Si la gravité est activée, le pion va tomber jusqu'à ce qu'il tombe sur quelque chose

		Args:
			pos: La position
		"""

		if self._gravite:
			pion_sous = self.get_pion((pos[0], pos[1] - 1, pos[2]))
			while pos[1] > 0 and pion_sous is None:
				pos = (pos[0], pos[1] - 1, pos[2])
				pion_sous = self.get_pion((pos[0], pos[1] - 1, pos[2]))
		if self.get_pion(pos) is None:
			pion_tour_blanc = {True: PionBlanc(), False: PionNoir()}
			self._plateau[pos[0]][pos[1]][pos[2]] = pion_tour_blanc.get(self.tour_blanc())
			move = pos
			self._posable.remove(move)
			self._pose.append(move)

	def tour_blanc(self) -> bool:
		return (len(self._pose) % 2 == 0) and len(self) ** 3 > len(self._pose)

	def tour_noir(self) -> bool:
		return len(self) ** 3 > len(self._pose) and not self.tour_blanc()

	def annule_pose(self):
		if self._pose:
			last = self._pose.pop()
			self._posable.append(last)
			# noinspection PyTypeChecker
			self.plateau[last[0]][last[1]][last[2]] = None

	@staticmethod
	def __start_plateau(taille) -> List[List[List[Optional[Pion]]]]:
		return [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]

	@staticmethod
	def __start_posable(taille) -> List[Tuple[int, int, int]]:
		# noinspection PyTypeChecker
		return list(itertools.product((_ for _ in range(taille)), repeat=3))

	@property
	def posable(self):
		return self._posable

	def win(self, pos: Tuple[int, int, int]) -> bool:
		# TODO : Normalement ok, mais à test
		lst = list(itertools.product([0, self.taille - 1, -1], repeat=3))
		for direction in lst:
			if self.sum(pos, direction) == self.taille:
				self._fini = True
				return self.fini

		return False

	def sum(self, pos, direction):
		# TODO
		pass

	def reset(self):
		# TODO
		pass

	@property
	def pose(self):
		return self._pose


def to_1d(pos, pos_max) -> int:
	return int(numpy.ravel_multi_index(pos, pos_max))


def to_3d(ind, pos_max):
	return numpy.unravel_index(ind, pos_max)


if __name__ == '__main__':
	Qbic = Qubic()
	for x in range(len(Qbic)):
		for y in range(len(Qbic)):
			for z in range(len(Qbic)):
				Qbic.poser((x, y, z))
				print(Qbic.win((x, y, z)))
	print(Qbic.posable, Qbic.tour_noir() or Qbic.tour_blanc())

# print(Qbic.plateau, Qbic.pose, Qbic.posable)
