import socket
from typing import Dict, Any, List

import jsonpickle

from model.qubic import Qubic
from networking.rooms import Room


class Client:
	HOST, PORT = "5.48.154.196", 9999
	# HOST, PORT = "localhost", 9999

	def __init__(self, name, id=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = None
		self.room_id = None
		self.id = id
		if self.id is None:
			print(f'No id, could be found, registering as new player')
			self._register(name)

	def send(self, data: Dict[str, Any], size=48000) -> Dict[str, Any]:
		"""
		Sends data to server

		Args:
			data: the data to be sent
			size: max size of the received data in bytes
			pickle: pickled object
		Returns:
			the received data
		"""
		data = jsonpickle.encode(data)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			# Create a socket (SOCK_STREAM means a TCP socket)
			# Connect to server and send request
			sock.connect((self.HOST, self.PORT))
			sock.sendall(bytes(data + "\n", "utf-8"))
			# Receive request from the server and shut down
			received = sock.recv(size).decode()

			answer = jsonpickle.decode(received)
			# print("Sent:     {}".format(data))
			# print("Received: {}".format(received))
			return answer

	def _register(self, player_name: str):
		"""
		registers the player in the server and sets the id and name attributes

		Args:
			player_name: the players name
		"""
		request = {
			'type': 'register',
			'player_name': player_name
		}
		result = self.send(request)
		try:
			self.id = result['player_id']
			self.name = result['player_name']
		except Exception as ex:
			print(f'Client could not register:{ex}')
			print(result)

	def create(self, room_name: str) -> str:
		"""
		creates a room

		Args:
			room_name: the name

		Returns:
			the rooms id
		"""
		request = {
			'type': 'create',
			'room_name': room_name
		}
		result = self.send(request)
		try:
			return result['room_id']
		except Exception as ex:
			print(f'Could not create {ex}')

	def join(self, room_id: str, spectator: bool):
		"""
		joins the room

		Args:
			room_id: the room to be joined
			spectator: if you're joining as a spectator

		Returns: the id of the room
		"""
		request = {
			'type': 'join',
			'player_id': self.id,
			'room_id': room_id,
			'spectator': spectator
		}
		result = self.send(request)
		try:
			self.room_id = result['room_id']
		except Exception as ex:
			print(f'Could not join {ex}')

	def leave(self) -> bool:
		if not self.room_id:
			return False

		request = {
			'type': 'leave',
			'player_id': self.id,
			'room_id': self.room_id
		}
		result = self.send(request)
		try:
			return result['success']
		except Exception as ex:
			print(f'Could not leave {ex}')

	def room_id_list(self) -> List[str]:
		request = {
			'type': 'room_id_list',
			'player_id': self.id,
		}
		result = self.send(request)
		try:
			return result['room_id_list']
		except Exception as ex:
			print(f'Could not get room id list {ex}')

	def room_list(self) -> List[Room]:
		request = {
			'type': 'room_list',
			'player_id': self.id,
		}
		result = self.send(request)
		try:
			return result['room_list']
		except Exception as ex:
			print(f'Could not get room list {ex}')

	def get_room(self) -> Room:
		request = {
			'type': 'room_get_by_id',
			'player_id': self.id,
			'room_id': self.room_id
		}
		result = self.send(request)
		try:
			return result['room']
		except Exception as ex:
			print(f'Could not get room {ex}')

	def get_qubic(self) -> Qubic:
		"""
		Has to be called when in a room

		Returns:
			the Qubic
		"""
		request = {
			'type': 'get_qubic',
			'player_id': self.id,
			'room_id': self.room_id
		}
		result = self.send(request)
		try:
			return result['qubic']
		except Exception as ex:
			print(f'Could not get qubic {ex}')

	def qubic_place(self, pos):
		request = {
			'type': 'qubic_place',
			'player_id': self.id,
			'room_id': self.room_id,
			'pos': pos
		}
		result = self.send(request)
		try:
			return result['qubic']
		except Exception as ex:
			print(f'Could not place piece in qubic {ex}')
