from abc import ABC
from typing import List

from qubic_observer import QubicObserver


class QubicSubject(ABC):
	__observers: List[QubicObserver]

	def __new__(cls):
		if cls is QubicSubject:
			raise TypeError('Abstract class cannot be instantiatied')
		return object.__new__(cls)

	def __init__(self):
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
