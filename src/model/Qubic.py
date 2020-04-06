from typing import Tuple, List, Optional, Union

import itertools
import numpy

from model.Curseur import Curseur
from model.Direction import DROITE, HAUT, DEVANT, mult_dir, add_dir
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

	def valid_pos(self, pos: Union[Tuple[int, int, int], Curseur]) -> bool:
		"""
		Args:
			pos:

		Returns:
		Vrai si la position n'est pas hors du jeu
		"""
		return all(map(lambda i: 0 <= i < len(self), pos))

	def get_pion(self, pos: Union[Tuple[int, int, int], Curseur]) -> Optional[Pion]:
		"""
		Retourne le pion à la position pos

		Args:
			pos: La position

		Returns:
			Le pion
		"""
		return self._plateau[pos[0]][pos[1]][pos[2]]

	def poser(self, pos: Union[Tuple[int, int, int], Curseur]):
		"""
		Pose un pion à la position pos dans le plateau si il n'y a rien
		Le type de pion posé est celui dont c'est le tour
		Si la gravité est activée, le pion va tomber jusqu'à ce qu'il tombe sur quelque chose

		Args:
			pos: La position
		"""
		pos = pos[0], pos[1], pos[2]
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
		"""
		Returns: Vrai si c'est aux blancs de jouer, faux sinon
		"""
		return (len(self._pose) % 2 == 0) and len(self) ** 3 > len(self._pose)

	def tour_noir(self) -> bool:
		"""
		Returns: Vrai si c'est aux noirs de jouer, faux sinon
		"""
		return len(self) ** 3 > len(self._pose) and not self.tour_blanc()

	def annule_coup(self):
		"""
		Annule le dernier coup joué si il y en a un
		"""
		if self._pose:
			last = self._pose.pop()
			self._posable.append(last)
			self.plateau[last[0]][last[1]][last[2]] = None

	@staticmethod
	def __start_plateau(taille) -> List[List[List[Optional[Pion]]]]:
		return [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]

	@staticmethod
	def __start_posable(taille) -> List[Tuple[int, int, int]]:
		# noinspection PyTypeChecker
		return list(itertools.product((_ for _ in range(taille)), repeat=3))

	def win(self, pos: Union[Tuple[int, int, int], Curseur]) -> bool:
		"""
		Retourne si la partie a été gagnée
		Args:
			pos:

		Returns:

		"""
		# TODO : Normalement ok, mais à test
		pos = pos[0], pos[1], pos[2]
		lst = list(itertools.product([True, False], repeat=3))
		axe: Tuple[int, int, int]
		for axe in lst:
			if self.__sum(pos, axe) == self.taille:
				self._fini = True
				return self.fini

		return False

	def __sum(self, pos: Tuple[int, int, int], axes: Tuple[int, int, int]) -> int:
		# TODO: à test, pas sûr de moi du tout
		pion = self.get_pion(pos)
		deb = 0  # len(self)-1
		test_pos = pos
		somme = 0
		deplacement = [DROITE if axes[0] else (0, 0, 0),
		               HAUT if axes[1] else (0, 0, 0),
		               DEVANT if axes[2] else (0, 0, 0)]
		if deb != 0:
			deplacement = list(map(mult_dir, [-1] * len(deplacement), deplacement))
		deplacement = add_dir(*deplacement)
		x, y, z = tuple(map(lambda p, axe: deb if axe else p, pos, axes))
		curr_pos = x, y, z
		if deplacement == (0, 0, 0):
			return 0
		while self.valid_pos(curr_pos) and self.get_pion(curr_pos):
			somme += 1
			add_dir(curr_pos, deplacement)
		return somme

	def reset(self):
		"""
		Réinitialise le plateau
		"""
		self._plateau = Qubic.__start_plateau(len(self))
		self._posable = Qubic.__start_posable(len(self))
		self._pose = []
		self._fini = False

	@property
	def pose(self):
		return self._pose

	@property
	def posable(self):
		return self._posable


def to_1d(pos, pos_max) -> int:
	return int(numpy.ravel_multi_index(pos, pos_max))


def to_3d(ind, pos_max):
	return numpy.unravel_index(ind, pos_max)
