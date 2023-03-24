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
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Binding to {}:{}" .format(self.host, self.port))
		self.server.bind((self.host, self.port))
	
	# Helpers
	def stash_connection_data(self, conn_data):
		self.stored_connections.update({conn_data[1]: conn_data[0]})
	
	
	# Main
	def go(self):
		self.server.listen(self.connections)
		while self.run:
			conn, addr = self.server.accept()
			self.stash_connection_data((conn, addr))
			
		
	

