from abc import ABC, abstractmethod
from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn, StreamRequestHandler
from threading import Thread, Lock
from typing import Any, Tuple, Optional, Dict

import jsonpickle
from ursina import *

from controls import EmptyController
from model.qubic import Qubic
from networking.rooms import Rooms
# TODO : peut-être passer en multi-threaded, 1 thread/client je sais pas si c'est utile pour l'instant
from ui.qubic.vue_qubic import VueQubic


class QubicServer(TCPServer, ThreadingMixIn):
	rooms: Rooms

	def __init__(self, server_address: Tuple[str, int], ServerRequestHandlerClass):
		super().__init__(server_address, ServerRequestHandlerClass)
		self.rooms = Rooms()
		self.lock = Lock()


class ServerRequestHandler(StreamRequestHandler):
	server: QubicServer

	def __init__(self, request: Any, client_address: Any, server: QubicServer):
		self.qubic_handler = QubicRequestHandler.init_cor(server)
		super().__init__(request, client_address, server)

	def handle(self):
		# self.request is the TCP socket connected to the client
		# host, port = self.client_address
		try:
			data = self.rfile.readline().strip()
			request = jsonpickle.decode(data)
			result = self.qubic_handler.handle_request(request)
			data = jsonpickle.encode(result)
			encoded = data.encode()
			self.wfile.write(encoded)
		except Exception as e:
			print(f'Exception in handle:{e}')


class QubicRequestHandler(ABC):
	next: 'QubicRequestHandler'
	server: QubicServer

	def __init__(self, server: QubicServer, next=None, *args, **kwargs):
		"""
		Args:
			server: the server
			next: next called handlers in the chain
		"""
		super().__init__(*args, **kwargs)
		self.server = server
		self.next = next

	@classmethod
	def init_cor(cls, server: QubicServer) -> 'QubicRequestHandler':
		handler = RegisterHandler(server, next=None)
		handler = CreateHandler(server, next=handler)
		handler = JoinHandler(server, next=handler)
		handler = LeaveHandler(server, next=handler)
		handler = RoomIDListHandler(server, next=handler)
		handler = RoomListHandler(server, next=handler)
		handler = GetRoomByIDHandler(server, next=handler)
		handler = QubicPlaceHandler(server, next=handler)
		handler = GetQubicHandler(server, next=handler)
		return handler

	def handle_request(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		"""
		if it can, handles the request
		Args:
			data: the request

		Returns:
			the result of the request, None if the request cannot be handled
		"""

		try:
			self.server.lock.acquire()
			result = self._handle_request(data)
		except Exception as e:
			print(f'Exception in handle_request:{e}')
			result = None
		finally:
			self.server.lock.release()

		if result:
			return result
		elif self.next:
			return self.next.handle_request(data)

	@abstractmethod
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		pass


class RegisterHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		"""
		handles a request
		Args:
			request: the request

		Returns:

		"""
		if request['type'] == 'register':
			p = self.server.rooms.register(request['player_name'])
			return {
				"type": "on_register",
				"player_id": p.id,
				"player_name": p.name
			}


class CreateHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'create':
			room_id = self.server.rooms.create(request['room_name'])
			return {
				"type": "on_create",
				"room_id": room_id,
				"room_name": self.server.rooms[room_id].name
			}


class JoinHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'join':
			if 'room_id' not in request:
				request['room_id'] = None
			pid, rid, spec = request['player_id'], request["room_id"], request["spectator"]
			room_id = self.server.rooms.join(pid, rid, spec)
			return {
				"type": "on_join",
				"room_id": room_id,
			}


class LeaveHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'leave':
			pid, rid = request['player_id'], request["room_id"]

			self.server.rooms.leave(pid, rid)
			return {
				"type": "on_leave",
				"success": True
			}


class RoomIDListHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict) -> Optional[Dict[str, Any]]:
		if request['type'] == 'room_id_list':
			rooms_id = self.server.rooms.rooms_id
			return {
				'type': 'on_room_id_list',
				'room_id_list': rooms_id
			}


class RoomListHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'room_list':
			rooms = self.server.rooms.rooms
			return {
				'type': 'on_room_list',
				'room_list': rooms
			}


class GetRoomByIDHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'room_get_by_id':
			room = self.server.rooms[request['room_id']]
			return {
				'type': 'on_room_get_by_id',
				'room': room
			}


class GetQubicHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'get_qubic':
			pid, rid = request['player_id'], request['room_id']
			room = self.server.rooms[rid]
			if room.is_in_room(pid) or pid in room.spectators:
				return {
					'type': 'on_get_qubic',
					'qubic': room.qubic
				}


class QubicPlaceHandler(QubicRequestHandler):
	def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		if request['type'] == 'qubic_place':
			pid, rid = request['player_id'], request['room_id']
			room = self.server.rooms[rid]
			if room.is_player_turn(pid):
				pos = request['pos']
				room.qubic.poser(pos)
				return {
					'type': 'on_qubic_place',
					'qubic': room.qubic
				}


def cmd(server: QubicServer, vue: VueQubic):
	def print_help():
		print("--------------------------------------")
		print("list : list rooms")
		print("room #room_id : print room information")
		print("user #user_id : print user information")
		print("quit : quit server")
		print("--------------------------------------")

	print_help()
	while True:
		cmd = input("cmd :")
		if cmd == "list":
			server.lock.acquire()
			print(f"Rooms ({len(server.rooms.rooms)}):")
			for room in server.rooms.rooms:
				print(f"{room}")
			server.lock.release()
		elif cmd == "list -p":
			server.lock.acquire()
			print(f"Players ({len(server.rooms.players)}):")
			for player in server.rooms.players.values():
				print(f"{player}")
			server.lock.release()
		elif cmd.startswith("room "):
			try:
				id = cmd[5:]
				room = server.rooms[id]
				print(room)
				try:
					print(room.qubic.plateau)
					vue.notify(room.qubic)
				except Exception as e:
					print(e)
			except:
				print("Error while getting room informations")
		elif cmd.startswith("player "):
			try:
				player = server.rooms.players[cmd[7:]]
				print(player)
			except:
				print("Error while getting user informations")
		elif cmd == 'clear':
			server.rooms.remove_empty()
		elif cmd == "help":
			print_help()
		elif cmd == "quit":
			print("Shutting down  server...")
			server.shutdown()
			server.server_close()

		else:
			print('unknown command')
