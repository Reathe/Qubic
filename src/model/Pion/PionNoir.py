from src.model.Pion.Pion import Pion


class PionNoir(Pion):
	def __eq__(self, other):
		return isinstance(other, PionNoir)
