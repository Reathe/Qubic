import unittest

from model.curseur import Curseur
from model.pion import PionBlanc
from model.qubic import Qubic


class TestQubic(unittest.TestCase):
	def test_poser(self):
		pass

	def test_tour(self):
		pass

	def test_annule_pose(self):
		q = Qubic(gravite=False)

		for x, z in zip(range(len(q)), range(len(q))[:0:-1]):
			q.poser((x, 0, z))
			q.poser((x, 1, z))

		self.assertFalse(q.fini)

		q.poser((len(q) - 1, 0, 0))
		self.assertTrue(q.fini)
		q.annule_coup()
		self.assertTrue(q.get_pion((len(q) - 1, 0, 0)) is None)
		self.assertFalse(q.fini)

	def test_valid_pos(self):
		q = Qubic()
		c = Curseur((4, 4, 4))
		for x in range(len(q)):
			for y in range(len(q)):
				for z in range(len(q)):
					self.assertTrue(q.valid_pos((x, y, z)))
		self.assertFalse(q.valid_pos((-5, 1, 1)))
		self.assertFalse(q.valid_pos((1, 4, 1)))

	def test_reset(self):
		pass

	def test_victoire(self):
		q = Qubic(gravite=False)

		for x in range(len(q)):
			q.poser((x, x, x))
			self.assertFalse(q.fini, "at pos {}".format(x))

		q.reset()
		for x, z in zip(range(len(q)), range(len(q))[:0:-1]):
			q.poser((x, 0, z))
			q.poser((x, 1, z))
		self.assertFalse(q.fini)
		q.poser((len(q) - 1, 0, 0))
		self.assertTrue(q.fini)

		q.reset()
		for x in range(len(q)):
			q.plateau[x][x][x] = PionBlanc()
		self.assertTrue(q.win((len(q) - 1,) * 3))

		q.reset()
		for x in range(len(q)):
			q.plateau[x][len(q) - 1 - x][x] = PionBlanc()
		self.assertTrue(q.win((len(q) - 1, 0, len(q) - 1)))

		q.reset()
		for x in list(range(len(q))):
			q.plateau[x][x][len(q) - 1 - x] = PionBlanc()
		self.assertTrue((len(q), len(q), 0))

		q.reset()
		for x in list(range(len(q))):
			q.plateau[x][len(q) - 1 - x][len(q) - 1 - x] = PionBlanc()
		self.assertTrue((len(q), len(q), 0))


if __name__ == '__main__':
	unittest.main()
