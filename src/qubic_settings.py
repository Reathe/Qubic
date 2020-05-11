from abc import ABC, abstractmethod

import jsonpickle


class Settings(ABC):
	def __init__(self, file_name, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.file_name = file_name

	@abstractmethod
	def default(self):
		pass

	def save(self):
		print(f"Saving {self.file_name}...")
		try:
			with open(self.file_name + '.json', 'w') as file:
				file.write(jsonpickle.encode(self))
		except:
			print("Failed to save")
			raise IOError

	def load(self):
		print(f"Loading {self.file_name}...")
		try:
			with open(self.file_name + '.json', 'r') as file:
				self.__dict__ = jsonpickle.decode(file.read()).__dict__
		except:
			print("Failed")
			raise IOError
