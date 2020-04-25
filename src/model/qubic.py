from typing import Tuple, List, Optional, Union

import itertools

from qubic_subject import QubicSubject
from model.curseur import Curseur
from model.direction_tools import mult_dir, add_dir, BAS
from model.pion import PionBlanc, PionNoir, Pion


class Qubic(QubicSubject):
	"""
	Les blancs commencent toujours... Comme aux échecs :)
	"""
	_plateau: List[List[List[Optional[Pion]]]]
	_posable: List[Tuple[int, int, int]]
	_pose: List[Tuple[int, int, int]]
	_gravite: bool
	_fini: bool

	def __init__(self, taille: int = 4, gravite: bool = True):
		super().__init__()
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
			pos = self.get_pos_with_gravity(pos)
		if self.get_pion(pos) is None:
			pion_tour_blanc = {True: PionBlanc(), False: PionNoir()}
			self._plateau[pos[0]][pos[1]][pos[2]] = pion_tour_blanc.get(self.tour_blanc())
			move = pos
			self._posable.remove(move)
			self._pose.append(move)
			self.win(pos)
			self.notify_observers()

	def get_pos_with_gravity(self, pos: Tuple[int, int, int]) -> Tuple[int, int, int]:
		"""
		Donne la position si le pion tombait jusqu'à ce qu'il rencontre sois le bas du plateau, soit un pion

		Args:
			pos: la position de départ

		Returns: la position tombee
		"""
		pion_sous = self.get_pion(add_dir(pos, BAS))
		while pos[1] > 0 and pion_sous is None:
			pos = add_dir(pos, BAS)
			pion_sous = self.get_pion(add_dir(pos, BAS))
		return pos

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
			self.notify_observers()

	@staticmethod
	def __start_plateau(taille) -> List[List[List[Optional[Pion]]]]:
		return [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]

	@staticmethod
	def __start_posable(taille) -> List[Tuple[int, int, int]]:
		# noinspection PyTypeChecker
		return list(itertools.product((_ for _ in range(taille)), repeat=3))

	def win(self, pos: Union[Tuple[int, int, int], Curseur]) -> bool:
		"""
		Returns if game was won by the piece in this position,
		also updates the corresponding fini variable

		Args:
			pos: the checked position

		Returns: boolean
		"""
		pos = pos[0], pos[1], pos[2]
		if self.get_pion(pos) is None:
			return False

		lst = list(itertools.product([1, 0, -1], repeat=3))[:28//2]
		axe: Tuple[int, int, int]
		for axe in lst:
			if self.__sum(pos, axe) + self.__sum(pos, mult_dir(-1, axe)) - 1 == self.taille:
				self._fini = True
				return self.fini

		return False

	def __sum(self, pos: Tuple[int, int, int], axes: Tuple[int, int, int]) -> int:
		"""
		Args:
			pos: Starting pos
			axes: the movement vector

		Returns:
			the number of consecutive equal pieces starting from pos, and moving by axes each time
		"""
		if axes == (0, 0, 0):
			return 1
		somme = 0
		pion = self.get_pion(pos)
		while self.valid_pos(pos) and self.get_pion(pos) == pion:
			somme += 1
			pos = add_dir(pos, axes)
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
