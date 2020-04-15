import unittest

from model.curseur import Curseur
from model.qubic import Qubic


class TestQubic(unittest.TestCase):
	def test_poser(self):
		pass

	def test_tour(self):
		pass

	def test_annule_pose(self):
		pass

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


if __name__ == '__main__':
	unittest.main()
