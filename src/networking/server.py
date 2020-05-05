import json
from abc import ABC, abstractmethod
from socketserver import TCPServer, BaseRequestHandler  # , ThreadingMixIn
# from threading import Thread
from typing import Any, Tuple, Optional, Dict

from networking.rooms import Rooms


# TODO: integrer une ui activable en console
# TODO : peut-être passer en multi-threaded, je sais pas si c'est utile pour l'instant
class QubicServer(TCPServer):
	rooms: Rooms

	def __init__(self, server_address: Tuple[str, int], ServerRequestHandlerClass):
		super().__init__(server_address, ServerRequestHandlerClass)
		self.rooms = Rooms()


class ServerRequestHandler(BaseRequestHandler):
	server: QubicServer

	def __init__(self, request: Any, client_address: Any, server: QubicServer):
		self.qubic_handler = QubicRequestHandler.init_cor(server)
		super().__init__(request, client_address, server)

	def handle(self):
		# self.request is the TCP socket connected to the client
		# host, port = self.client_address
		data = self.request.recv(1024).decode().strip()
		request = json.loads(data)
		result = self.qubic_handler.handle_request(request)
		# TODO: enlever print
		print(request)
		print(result)
		data = json.dumps(result)
		self.request.sendall(data.encode())


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
		return handler

	def handle_request(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		"""
		if it can, handles the request
		Args:
			data: the request

		Returns:
			the result of the request, None if the request cannot be handled
		"""
		result = self.next._handle_request(data)
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


if __name__ == "__main__":
	HOST, PORT = "localhost", 9999

	with QubicServer((HOST, PORT), ServerRequestHandler) as server:
		server.serve_forever()
