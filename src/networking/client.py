import json
import socket
from typing import Dict, Any, List

from networking.rooms import Room


class Client:
	HOST, PORT = "localhost", 9999

	def __init__(self, name, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name = None
		self.id = None
		self.room_id = None

		self._register(name)

	def send(self, data: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Sends data to server

		Args:
			data: the data to be sent

		Returns:
			the received data
		"""
		data = json.dumps(data)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			# Create a socket (SOCK_STREAM means a TCP socket)
			# Connect to server and send request
			sock.connect((self.HOST, self.PORT))
			sock.sendall(bytes(data + "\n", "utf-8"))
			# Receive request from the server and shut down
			received = json.loads(sock.recv(1024).decode())
			print("Sent:     {}".format(data))
			print("Received: {}".format(received))
			return received

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
			print(ex)
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
			print(ex)
			print(result)

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
			return result['room_id']
		except Exception as ex:
			print(ex)
			print(result)

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
			print(ex)
			print(result)

	def room_id_list(self) -> List[str]:
		request = {
			'type': 'room_id_list',
			'player_id': self.id,
		}
		result = self.send(request)
		try:
			return result['room_id_list']
		except Exception as ex:
			print(ex)
			print(result)

	def room_list(self) -> List[Room]:
		request = {
			'type': 'room_list',
			'player_id': self.id,
		}
		result = self.send(request)
		try:
			return result['room_list']
		except Exception as ex:
			print(ex)
			print(result)

	def get_room(self, room_id: str) -> Room:
		request = {
			'type': 'room_get_by_id',
			'player_id': self.id,
			'room_id': room_id,
		}
		result = self.send(request)
		try:
			return result['room']
		except Exception as ex:
			print(ex)
			print(result)
