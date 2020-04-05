from abc import abstractmethod, ABC


class Pion(ABC):
	@abstractmethod
	def __eq__(self, other):
		"""
		Deux pions sont les mêmes si ils sont du même type
		"""
		pass
