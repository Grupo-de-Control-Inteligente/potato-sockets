import socket
import sys
import json
import random

PORT = 12345
BUFFER_SIZE = 1024
CNT = 10

class sockets():

	def __init__(self, ip):
		self.socketaddr = (ip, PORT)
		self.valid = 0
		for i in range(1,6):
			if(self.valid == 0):
				try:
					self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					self.valid = 1
					self.seq = random.randint(0,10000)

				except socket.error as err: 
					print("ERROR: Socket creation failed with error %s" %(err))
					self.valid = 0
				
		if(self.valid == 0):
			sys.exit(1)
		#self.audio = 0

	def bind (self):
		self.valid = 0
		for i in range(1,6):
			if(self.valid == 0):
				try:
					self.sock.bind(self.socketaddr)
					print("Bind to %s\n" % repr(self.socketaddr))
					self.valid = 1
				except:
					print("ERROR: Bind to %s refused" % repr(self.socketaddr))
					self.valid = 0
		if(self.valid == 0):
			sys.exit(1)

	def connect(self, ip_serv):
		self.valid = 0
		for i in range(1,6):
			if(self.valid == 0):
				try:
					self.serveraddr = (ip_serv, PORT)
					self.sock.connect(self.serveraddr)
					print("Connected to %s\n" % repr(self.serveraddr))
					self.valid = 1
				except:
					print("ERROR: Connection to %s refused" % repr(self.serveraddr))
					self.valid = 0
		if(self.valid == 0):
			sys.exit(1)
		 
	def receive(self):
		buff, self.receiveaddr = self.sock.recvfrom(BUFFER_SIZE)
		msg = buff.decode('utf-8')
		# print ("Received message: " + msg)
		# print('received %s bytes from %s\n' % (len(buff), self.receiveaddr))
		# if(self.audio == 1):
		# 	self.audio = 0
		# 	data["message"] = msg
		# else: 

		try:
			
			data = json.loads(msg)
			#if(data["ip_origin"] != "127.0.0.1" and data["ip_origin"] != "127.0.0.3"):
			if(data["ip_origin"] != "127.0.0.1" and data["ip_origin"] != self.socketaddr[0]):
				msent = self.sock.sendto(buff, self.receiveaddr)
				# print("\n")
				# print("Confirmación enviada")
				# print("\n")
			
				
			# type_msg = data["type_msg"]
			# if (type_msg == "<class 'bytes'>"):
			# 	self.audio = 1
			
			
		except json.JSONDecodeError:
			print("Invalid JSON message received:", msg)
		return data
				
	

	def send(self, data):
		# type_msg = data["type_msg"]
		# if(type_msg == "<class 'bytes'>" ):
		# 	msg_audio = data["message"]
		# 	data["message"] = 0
		# 	audio = 1
		# else: audio = 0
		data["seq"] = self.seq 
		self.seq = self.seq + CNT
		# print("Sent message" + str(data))
		msg = json.dumps(data)
		ip_destination = data["ip_destination"]
		buff = msg.encode('utf-8')
		self.dest_addr = (ip_destination, PORT)
		msent = self.sock.sendto(buff, self.dest_addr)

		# Confirmación de la recepción del mensaje (sólo en el caso de los slaves para poder probar los módulos por separado)
		if(data["ip_origin"] != "127.0.0.1" ):
			conf, receiveaddr = self.sock.recvfrom(BUFFER_SIZE)
			confirmation = json.loads(conf.decode('utf-8'))
			# print("Confirmación recibida")
			# Bucle para reenviar el mensaje tantas veces como sea necesario
			for i in range(1,5):
				if(confirmation["seq"] != data["seq"]):
					msent = self.sock.sendto(buff, self.dest_addr)
					conf, receiveaddr = self.sock.recvfrom(BUFFER_SIZE)
					confirmation = json.loads(conf.decode('utf-8'))

				
			
			


		# print('sent %s bytes back to %s\n' % (msent, self.dest_addr))
		# if(audio == 1):
		# 	buff = msg_audio.encode('utf-8')
		# 	msent = self.sock.sendto(buff, self.dest_addr)
		
	def close(self):
		self.valid = 0
		for i in range(1,6):
			if (self.valid == 0):
				try:
					print("Closing socket")
					self.valid = 1
					self.sock.close()

				except socket.error as err: 
					print("ERROR: close of Socket failed with error %s" %(err))
					self.valid = 0
				
		if (self.valid == 0):
			sys.exit(1)

	def fileno(self):
		return self.sock.fileno()
	

		
	# def receive_file_size(self, sck: socket.socket):
	# 	# Esta función se asegura de que se reciban los bytes
	# 	# que indican el tamaño del archivo que será enviado,
	# 	# que es codificado por el cliente vía struct.pack(),
	# 	# función la cual genera una secuencia de bytes que
	# 	# representan el tamaño del archivo.
	# 	fmt = "<Q"
	# 	expected_bytes = struct.calcsize(fmt)
	# 	received_bytes = 0
	# 	stream = bytes()
	# 	while received_bytes < expected_bytes:
	# 		chunk = sck.recv(expected_bytes - received_bytes)
	# 		stream += chunk
	# 		received_bytes += len(chunk)
	# 	filesize = struct.unpack(fmt, stream)[0]
	# 	return filesize

	# def receive_file(self, sck: socket.socket, filename):
	# 	# Leer primero del socket la cantidad de 
	# 	# bytes que se recibirán del archivo.
	# 	filesize = self.receive_file_size(sck)
	# 	# Abrir un nuevo archivo en donde guardar
	# 	# los datos recibidos.
	# 	with open(filename, "wb") as f:
	# 		received_bytes = 0
	# 		# Recibir los datos del archivo en bloques de
	# 		# 1024 bytes hasta llegar a la cantidad de
	# 		# bytes total informada por el cliente.
	# 		while received_bytes < filesize:
	# 			chunk = sck.recv(1024)
	# 			if chunk:
	# 				f.write(chunk)
	# 				received_bytes += len(chunk)