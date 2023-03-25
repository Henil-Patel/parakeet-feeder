import socket
import logging
import threading

HOST = ""
PORT = 65432
class Server():
	def __init__(self, host=None, port=None, connections):
		self.stored_connections = dict()
		self.run = True
		self.connections = connections
		if host is not None and port is not None:
			self.host = host
			self.port = port
		else:
			self.host = HOST
			self.port = PORT
	
		print("Initializing socket object")
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Binding to {}:{}" .format(self.host, self.port))
		self.server_socket.bind((self.host, self.port))
	
	# Helpers
	def stash_connection_data(self, conn_data):
		connection = conn_data[0]
		address = conn_data[1]
		connection_thread = conn_data[2]
		self.stored_connections.update({address: {connection: connection_thread}})
		# Write this to a DB
	
	def listener(self, connection, address):
		return
		
	# Main
	def go(self):
		self.server_socket.listen(self.connections)
		self.server_socket.blocking(False)
		while self.run:
			if len(self.stored_connections) < self.connections:
				
				# These are client connection data
				conn, addr = self.server_socket.accept()
				conn.sendall(b"Welcome to parakeet feeder!")
				
				# Create connection thread
				t = threading.Thread(target = self.listener(), args = (conn, addr))
				self.stash_connection_data((conn, addr, t))
				
				
				
			else:
				print("All connections are currently being used")
			
			
		
if __name__() == "__main__":
	connections = 5
	obj1 = Server(connections)
	obj1.go()
	

