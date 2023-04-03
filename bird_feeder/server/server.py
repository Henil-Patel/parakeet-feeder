import socket
import logging
import threading
import queue

HOST = "127.0.0.1"
PORT = 65432

class CommandHandler():
	def __init__(self, connection, address, message_queue: queue.Queue):
		self.connection = connection
		self.address = address 
		self.rx = None
		self.msg = message_queue
		self.size = self.msg.qsize()
		self.main()
	
	def main(self):
		print("Started listener thread for address : {}" .format(self.address))
		while True:
			try:
				self.listen()
			except BrokenPipeError as e:
				print("Listener connection broken. Exiting...")
				break
			self.respond()

				
	def listen(self):
		try:
			self.connection.sendall(b"\n[127.0.0.1]:")
			self.rx = self.connection.recv(1024)
			print("[{}] Got message: {}" .format(self.address[0], self.rx))
			self.msg.put_nowait({"id" : self.connection, "data": self.rx})
		except BrokenPipeError as e:
			raise e
		

	def respond(self):
		if abs(self.msg.qsize() - self.size) == 0:
			print("No new message")
		else:
			msg = self.msg.get()
			print(msg)
 
	
class Server():
	def __init__(self, host, port, connections):
		self.stored_connections = dict()
		self.run = True
		self.connections = connections
		self.host = host
		self.port = port
		self.msgq = queue.Queue()
	
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
		p = threading.Thread(target = Processor, args = (self.msgq,))
		p.start()
		while self.run:
			if len(self.stored_connections) < self.connections:
				# These are client connection data
				conn, addr = self.server_socket.accept()
				conn.sendall(b"Welcome to parakeet feeder!\n")
				print("Got connection from {}".format(addr))
				# Create connection thread
				t = threading.Thread(target = CommandHandler, args = (conn, addr, self.msgq))
				self.stash_connection_data((conn, addr, t, False))
				
			else:
				print("All connections are currently being used")
				break

class Processor():
	def __init__(self, q: queue.Queue):
		self.q = q
		self.size = self.q.qsize()
		self.on_rx()

	def on_rx(self):
		while True:
			if abs(self.q.qsize() - self.size) == 0:
				continue
			else:
				msg: dict = self.q.get()
				self.q.put({"id": msg.get("id"), "data": "processed"})

			
			
		
if __name__ == "__main__":
	connections = 5
	server = Server(HOST, PORT, connections)
	server.go()
	

