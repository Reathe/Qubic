import itertools
from typing import List, Optional, Tuple, Union

from model.curseur import Curseur
from model.direction_tools import add_dir, BAS, mult_dir
from model.pion import Pion, PionBlanc, PionNoir
from qubic_observer import QubicSubject


class Qubic(QubicSubject):
	"""
	Les blancs commencent toujours... Comme aux échecs :)
	"""
	_plateau: List[List[List[Optional[Pion]]]]
	_posable: List[Tuple[int, int, int]]
	_pose: List[Tuple[int, int, int]]
	_gravite: bool
	_fini: Optional[Pion]

	def __init__(self, taille: int = 4, gravite: bool = True):
		super().__init__()
		self._taille = taille
		self._plateau = Qubic.__start_plateau(taille)
		self._posable = Qubic.__start_posable(taille, gravite)
		self._last_posable = None
		self._pose = []
		self._fini = None
		self._gravite = gravite

	@property
	def plateau(self) -> List[List[List[Optional[Pion]]]]:
		return self._plateau

	@property
	def fini(self) -> bool:
		return self._fini is not None

	@property
	def winner(self) -> Optional[Pion]:
		return self._fini

	@property
	def taille(self) -> int:
		return self._taille

	def __len__(self):
		return self.taille

	def valid_pos(self, pos: Union[Tuple[int, int, int], Curseur]) -> bool:
		"""
		Args:
			pos:

		Returns:
		Vrai si la position n'est pas hors du jeu
		"""
		for p in pos:
			if not 0 <= p < self.taille:
				return False
		return True

	def get_pion(self, pos: Union[Tuple[int, int, int], Curseur]) -> Optional[Pion]:
		"""
		Retourne le pion à la position pos

		Args:
			pos: La position

		Returns:
			Le pion
		"""
		return self._plateau[pos[0]][pos[1]][pos[2]]

	def poser(self, pos: Union[Tuple[int, int, int], Curseur], pion: Pion = None, notify=True):
		"""
		Pose un pion à la position pos dans le plateau si il n'y a rien
		Le type de pion posé est celui dont c'est le tour
		Si la gravité est activée, le pion va tomber jusqu'à ce qu'il tombe sur quelque chose

		Args:
			pos: La position
			pion: Le pion à poser
			notify: notify observers at the end
		"""
		if self.fini:
			return
		pos = pos[0], pos[1], pos[2]
		if self._gravite:
			pos = self.get_pos_with_gravity(pos)
		if self.get_pion(pos) is None:
			if pion is None:
				pion_tour_blanc = {True: PionBlanc(), False: PionNoir()}
				pion = pion_tour_blanc.get(self.tour_blanc())
			self._plateau[pos[0]][pos[1]][pos[2]] = pion
			self._posable.remove(pos)
			if self._gravite and pos[1] < len(self) - 1:
				next_possible = pos[0], pos[1] + 1, pos[2]
				self._posable.append(next_possible)
			self._pose.append(pos)
			self.win(pos)
			if notify:
				self.notify_observers()
				if self.fini:
					print(f"{self.winner.__name__} win")
			# TODO: temp

	def get_pos_with_gravity(self, pos: Tuple[int, int, int]) -> Tuple[int, int, int]:
		"""
		Donne la position si le pion tombait d'en haut jusqu'à ce qu'il rencontre sois le bas du plateau, soit un pion

		Args:
			pos: la position de départ

		Returns: la position tombee
		"""
		pos = pos[0], self.taille - 1, pos[2]
		pion_sous = self.get_pion(add_dir(pos, BAS))
		while pos[1] > 0 and pion_sous is None:
			pos = add_dir(pos, BAS)
			pion_sous = self.get_pion(add_dir(pos, BAS))
		return pos

	def tour_blanc(self) -> bool:
		"""
		Returns: Vrai si c'est aux blancs de jouer, faux sinon
		"""
		return (len(self._pose) % 2 == 0) and not self.fini

	def tour_noir(self) -> bool:
		"""
		Returns: Vrai si c'est aux noirs de jouer, faux sinon
		"""
		return not self.fini and not self.tour_blanc()

	def annule_coup(self, notify=False):
		"""
		Annule le dernier coup joué si il y en a un
		"""
		if self._pose:
			last = self._pose.pop()
			self._posable.append(last)
			if self._gravite and last[1] < len(self) - 1:
				next_possible = last[0], last[1] + 1, last[2]
				self._posable.remove(next_possible)
			self.plateau[last[0]][last[1]][last[2]] = None
			self._fini = None
			if notify:
				self.notify_observers()

	@staticmethod
	def __start_plateau(taille) -> List[List[List[Optional[Pion]]]]:
		return [[[None for _ in range(taille)] for _ in range(taille)] for _ in range(taille)]

	@staticmethod
	def __start_posable(taille, gravite) -> List[Tuple[int, int, int]]:
		if gravite:
			posable_list = []
			for x in range(taille):
				for z in range(taille):
					posable_list.append((x, 0, z))
			return posable_list
		else:
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

		lst = list(itertools.product([1, 0, -1], repeat=3))[:28 // 2]
		axe: Tuple[int, int, int]
		for axe in lst:
			if self.__sum(pos, axe) + self.__sum(pos, mult_dir(-1, axe)) - 1 == self.taille:
				self._fini = PionNoir if len(self.pose) % 2 == 0 else PionBlanc
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
		self._posable = Qubic.__start_posable(len(self), self._gravite)
		self._pose = []
		self._fini = None
		self.notify_observers()

	@property
	def pose(self):
		return self._pose

	@property
	def posable(self):
		if self.fini:
			return []
		else:
			return self._posable
