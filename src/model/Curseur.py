from operator import add
from typing import Tuple


class Curseur:
	"""
	Un Curseur qui situe une position
	"""

	def __init__(self, pos_max: Tuple[int, int, int] = (1, 1, 1), pos: Tuple[int, int, int] = (0, 0, 0)):
		"""
		Args:
			pos: (x, y, z)
			pos_max: (x_max, y_max, z_max)
		"""
		if not all(map(lambda v: v > 0, pos_max)):
			raise ValueError("La pos_max {} du curseur n'est pas valide".format(pos_max))

		self._pos_max = pos_max
		self.pos = pos

	@property
	def pos(self) -> Tuple[int, int, int]:
		"""
		La position (x,y,z) du curseur
		"""
		return self._pos

	@pos.setter
	def pos(self, pos: Tuple[int, int, int]) -> None:
		"""
		set self.pos si la position est valide
		Args:
			pos: La nouvelle pos
		"""
		if not self.valid_pos(pos):
			raise ValueError("Position {} non valide".format(pos))
		self._pos = pos

	@property
	def pos_max(self) -> Tuple[int, int, int]:
		"""
		La position max (non comprise) (x,y,z) du curseur
		"""
		return self._pos_max

	def __add__(self, pos: Tuple[int, int, int]) -> 'Curseur':
		x, y, z = tuple(map(add, self.pos, pos))
		return Curseur((x, y, z), self.pos_max)

	def __iadd__(self, vect: Tuple[int, int, int]) -> 'Curseur':
		"""
		Déplace le curseur, la nouvelle pos devient pos+vect, élément par élément

		Args:
		 vect:
		"""
		p = (_, _, _) = tuple(map(add, self.pos, vect))
		self.pos = p
		return self

	def valid_pos(self, pos: Tuple[int, int, int]) -> bool:
		"""
		Une position est valide si 0 <= pos < pos_max, élément par élément

		Args:
			pos: La position à tester
		Returns: si la position est valide
		"""
		return all(max_val > val >= 0 for val, max_val in zip(pos, self.pos_max))

	def move(self, vect: Tuple[int, int, int]) -> 'Curseur':
		"""
		Déplace le curseur, la nouvelle pos devient pos+vect, élément par élément
		Args:
		 vect: le vect
		"""
		return self.__iadd__(vect)

	def __str__(self):
		return 'Curseur[pos: {}, pos_max: {}]'.format(self.pos, self.pos_max)
