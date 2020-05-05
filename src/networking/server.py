import json
from socketserver import ThreadingMixIn, TCPServer, BaseRequestHandler
from typing import Any, Tuple


class QubicServer(ThreadingMixIn, TCPServer):
	def __init__(self, server_address: Tuple[str, int], QubicRequestHandlerClass):
		super().__init__(server_address, QubicRequestHandlerClass)
		self.history = {}


class QubicRequestHandler(BaseRequestHandler):
	def __init__(self, request: Any, client_address: Any, server: QubicServer):
		super().__init__(request, client_address, server)

	def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).decode().strip()

		self.request.sendall(json.dumps(self.server.history).encode())

	def parse(self):
		pass


if __name__ == "__main__":
	HOST, PORT = "localhost", 9999

	with QubicServer((HOST, PORT), QubicRequestHandler) as server:
		server.serve_forever()
