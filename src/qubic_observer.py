from abc import ABC, abstractmethod
from typing import List


class QubicObserver(ABC):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@abstractmethod
	def notify(self, qubic):
		raise NotImplementedError


class QubicSubject(ABC):
	__observers: List[QubicObserver]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__observers = []

	@property
	def observers(self) -> List[QubicObserver]:
		return self.__observers

	def add_observers(self, *observers: QubicObserver):
		for observer in observers:
			self.observers.append(observer)

	def remove_observers(self, *observers: QubicObserver):
		for observer in observers:
			self.observers.remove(observer)

	def notify_observers(self):
		for observer in self.observers:
			observer.notify(self)
