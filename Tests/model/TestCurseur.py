import unittest

from src.model.Curseur import Curseur


class MyTestCase(unittest.TestCase):
	def test_init(self):
		with self.assertRaises(ValueError):
			Curseur((5, 0, 5))
		with self.assertRaises(ValueError):
			Curseur((5, -5, 5))

		with self.assertRaises(ValueError):
			Curseur((5, 5, 5), (5, 5, 5))
		with self.assertRaises(ValueError):
			Curseur((5, 5, 5), (6, 0, 0))
		with self.assertRaises(ValueError):
			Curseur((5, 5, 5), (1, -1, 1))

	def test_iadd(self):
		c = Curseur(pos_max=(1, 1, 1))
		with self.assertRaises(ValueError):
			c += (0, 1, 0)
		with self.assertRaises(ValueError):
			c += (0, -1, 0)

		c = Curseur(pos_max=(4, 4, 4))
		with self.assertRaises(ValueError):
			c += (1, 3, 5)
		with self.assertRaises(ValueError):
			c += (0, 4, 0)


if __name__ == '__main__':
	unittest.main()
