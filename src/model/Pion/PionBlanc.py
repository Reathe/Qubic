from src.model.Pion.Pion import Pion


class PionBlanc(Pion):
	def __eq__(self, other):
		return isinstance(other, PionBlanc)
