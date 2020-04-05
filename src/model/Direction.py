from operator import add
from typing import Tuple

GAUCHE = (-1, 0, 0)
DROITE = (1, 0, 0)
HAUT = (0, 1, 0)
BAS = (0, -1, 0)
DEVANT = (0, 0, 1)
DERRIERE = (0, 0, -1)


def add_dir(*p: Tuple[int, int, int]) -> Tuple[int, int, int]:
	res = (0, 0, 0)
	for direction in p:
		res = map(add, res, direction)
	return tuple(res)


def mult_dir(n: int, p: Tuple[int, int, int]) -> Tuple[int, int, int]:
	x, y, z = map(lambda a: a * n, p)
	return x, y, z
