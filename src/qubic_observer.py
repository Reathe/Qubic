from abc import ABC, abstractmethod


class QubicObserver(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__()

	@abstractmethod
	def notify(self, qubic):
		raise NotImplementedError
