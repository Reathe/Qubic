import json
import socket

if __name__ == '__main__':
	HOST, PORT = "localhost", 9999
	while True:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

			data = input()
			# Create a socket (SOCK_STREAM means a TCP socket)
			# Connect to server and send data
			sock.connect((HOST, PORT))
			sock.sendall(bytes(data + "\n", "utf-8"))
			# Receive data from the server and shut down
			received = json.loads(sock.recv(1024))
			print("Sent:     {}".format(data))
			print("Received: {}".format(received))
