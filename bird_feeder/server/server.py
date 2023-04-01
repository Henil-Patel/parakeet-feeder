import socket
import logging
import threading

HOST = "127.0.0.1"
PORT = 65432

class CommandHandler():
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address 
		self.main()
	
	def main(self):
		self.listen()
		self.process()
		self.respond()

	def listen(self):
		print("Started listener thread for address : {}" .format(self.address))
		while True:
			try:
				self.connection.sendall(b"\n[127.0.0.1]:")
			except BrokenPipeError as e:
				print("Connection broken!")
				break
			data = self.connection.recv(1024)
			print("[{}]Processing data: {}" .format(self.address[0], data))
class Server():
	def __init__(self, host, port, connections):
		self.stored_connections = dict()
		self.run = True
		self.connections = connections
		self.host = host
		self.port = port
	
		print("Initializing socket object")
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print("Binding to {}:{}" .format(self.host, self.port))
		self.server_socket.bind((self.host, self.port))
	
	# Helpers
	def stash_connection_data(self, conn_data):
		connection = conn_data[0]
		address = conn_data[1]
		connection_thread = conn_data[2]
		status = conn_data[3]
		print("Starting new connection")
		connection_thread.start()
		status = True
		self.stored_connections.update({address: {connection: [connection_thread, status]}})
		# TODO: Write this to a DB
		
	# Main
	def go(self):
		self.server_socket.listen(self.connections)
		
		while self.run:
			if len(self.stored_connections) < self.connections:
				# These are client connection data
				conn, addr = self.server_socket.accept()
				conn.sendall(b"Welcome to parakeet feeder!\n")
				print("Got connection from {}".format(addr))
				# Create connection thread
				t = threading.Thread(target = CommandHandler, args = (conn, addr))
				self.stash_connection_data((conn, addr, t, False))
				
			else:
				print("All connections are currently being used")
				break
			
			
		
if __name__ == "__main__":
	connections = 5
	server = Server(HOST, PORT, connections)
	server.go()
	

