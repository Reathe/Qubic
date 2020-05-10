import sys

sys.path.append('src')

from threading import Thread

from ursina import *
from controls import EmptyController
from model.qubic import Qubic
from networking.server import QubicServer, cmd, ServerRequestHandler
from ui.qubic.vue_qubic import VueQubic

if __name__ == "__main__":
	# HOST, PORT = "localhost", 9999
	window.title = 'server'
	window.windowed_size = (500, 400)
	server_view = Ursina()
	q = Qubic()
	vueQub = VueQubic(q, EmptyController())

	HOST, PORT = "", 9999
	Thread(target=server_view.run)
	server = QubicServer((HOST, PORT), ServerRequestHandler)

	server_thread = Thread(target=server.serve_forever)
	server_thread.start()

	Thread(target=cmd, args=(server, vueQub)).start()
	server_view.run()
