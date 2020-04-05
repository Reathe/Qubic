import unittest

from src.model.Pion.Pion import Pion
from src.model.Pion.PionBlanc import PionBlanc
from src.model.Pion.PionNoir import PionNoir


class TestPions(unittest.TestCase):
	def test_eq(self):
		self.assertEqual(PionNoir(), PionNoir())
		self.assertEqual(PionBlanc(), PionBlanc())
		self.assertNotEqual(PionBlanc(), PionNoir())
		self.assertNotEqual(PionBlanc(), None)
		self.assertNotEqual(PionNoir(), None)
		self.assertEqual(PionNoir(), PionNoir)
		self.assertEqual(PionBlanc(), PionBlanc)
		self.assertNotEqual(PionBlanc(), PionNoir)
		self.assertNotEqual(PionNoir(), PionBlanc)
		self.assertNotEqual(PionBlanc(), Pion)
		self.assertNotEqual(PionNoir(), Pion)

	def test_abstract(self):
		with self.assertRaises(TypeError):
			Pion()


if __name__ == '__main__':
	unittest.main()
