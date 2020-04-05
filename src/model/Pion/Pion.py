from abc import ABC, ABCMeta


class Pion(ABC):
	__metaclass__ = ABCMeta

	def __new__(cls):
		if cls is Pion:
			raise TypeError('Abstract class cannot be instantiatied')

		return object.__new__(cls)

	def __eq__(self, other):
		"""
		Deux pions sont les mêmes si ils sont du même type et non None
		"""
		return other is not None and self.repr() == other.repr()

	def __repr__(self):
		return type(self).__name__

	@classmethod
	def repr(cls):
		return cls.__name__
