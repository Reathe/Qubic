from abc import ABC, abstractmethod


class QubicObserver(ABC):
	def __new__(cls):
		if cls is QubicObserver:
			raise TypeError('Abstract class cannot be instantiatied')
		return object.__new__(cls)

	def __init__(self):
		pass

	@abstractmethod
	def notify(self, qubic):
		raise NotImplementedError
