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

	def test_get_set_item(self):
		c = Curseur(pos_max=(4, 4, 4))
		with self.assertRaises(ValueError):
			c['y'] = 5
		self.assertTrue(c["y"] == 0)
		self.assertTrue(c["z"] == 0)
		c['y'] = 2
		self.assertTrue((0, 2, 0) == c.pos)

	def test_iterator(self):
		test_curs = Curseur(pos_max=(4, 4, 4)), Curseur(pos=(0, 3, 1), pos_max=(4, 4, 4))
		for c in test_curs:
			ind = 0
			for i in c:
				with self.subTest("test: {}\n{}[{}] == {}\n".format(c, c.pos, ind, i)):
					self.assertTrue(i == c.pos[ind])
				ind += 1


if __name__ == '__main__':
	unittest.main()
