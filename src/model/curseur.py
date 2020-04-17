from typing import Tuple, Union

from src.model.direction_tools import add_dir


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
		super().__init__()
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
		return Curseur(self.pos_max, add_dir(self.pos, pos))

	def __iadd__(self, vect: Tuple[int, int, int]) -> 'Curseur':
		"""
		Déplace le curseur, la nouvelle pos devient pos+vect, élément par élément

		Args:
		 vect:
		"""
		self.pos = add_dir(self.pos, vect)
		return self

	def __getitem__(self, key: Union[str, int], in_pos_max: bool = False):
		nuple = self.pos_max if in_pos_max else self.pos
		real_key = {'x': 0, 'y': 1, 'z': 2, 0: 0, 1: 1, 2: 2}
		return nuple[real_key[key]]

	def __setitem__(self, key, value):
		real_key = {'x': 0, 'y': 1, 'z': 2, 0: 0, 1: 1, 2: 2}
		res = list(self.pos)
		res[real_key[key]] = value
		self.pos = tuple(res)

	def __iter__(self):
		self.__it = 0
		return self

	def __next__(self):
		x = self.__it
		if x < 3:
			self.__it += 1
			return self.pos[x]
		else:
			raise StopIteration

	def valid_pos(self, pos: Union[Tuple[int, int, int], 'Curseur']) -> bool:
		"""
		Une position est valide si 0 <= pos < pos_max, élément par élément

		Args:
			pos: La position à tester
		Returns: si la position est valide
		"""
		pos = pos[0], pos[1], pos[2]
		return all(max_val > val >= 0 for val, max_val in zip(pos, self.pos_max))

	def move(self, vect: Tuple[int, int, int]) -> 'Curseur':
		"""
		Déplace le curseur, la nouvelle pos devient pos+vect, élément par élément

		Args:
		 vect: le vect
		"""
		return self.__iadd__(vect)

	def __repr__(self):
		return 'Curseur[pos: {}, pos_max: {}]'.format(self.pos, self.pos_max)
