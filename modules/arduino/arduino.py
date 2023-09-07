import sys
import serial

import asyncio

import sys
import os
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(package_path)
from sockets.sockets import sockets

ip_master = "127.0.0.1"
ip_arduino = "127.0.0.7"

port = "/dev/ttyAMA0"
baudrate = 115200

class arduino():

	def __init__(self):
		self.arduino = sockets(ip_arduino)
		self.arduino.bind()
		self.arduino.connect(ip_master)
		self.hw_sensors = serial.Serial(port, baudrate)
		# time.sleep(2)

		self.id_sent_message = "None"
		self.sent_message = "None"

		self.id_received_message = "None"
		self.received_message = "None"

		
	def sockets_send(self):

		response_data = {
		"ip_origin": ip_arduino,
			"ip_destination": ip_master,
			"id_message": self.id_sent_message,
			"message":  self.sent_message,
			"type_msg": str(type(self.sent_message))
			}

		self.arduino.send(response_data)

	def sockets_receive(self):
		received_data = self.arduino.receive()

		self.id_received_message = received_data['id_message']
		self.received_message = received_data['message']

	def process_sensor_data(self, data):
		values = data.strip().split()  # Dividir el mensaje en valores individuales

		# Recorrer los valores en pares (valor, ID del sensor)
		for i in range(0, len(values), 2):
			value = values[i]
			sensor_id = values[i + 1]

			# Asignar los valores a las variables correspondientes según el ID del sensor
			if sensor_id == 'E':
				self.id_sent_message = "send right ear"
				self.sent_message = int(value)
				self.sockets_send()
			elif sensor_id == 'e':
				self.id_sent_message = "send left ear"
				self.sent_message  = int(value)
				self.sockets_send()
			elif sensor_id == 'L':
				self.id_sent_message = "send light"
				self.sent_message  = int(value)
				self.sockets_send()
			elif sensor_id == 'l':
				self.id_sent_message = "send light"
				self.sent_message  = int(value)
				self.sockets_send()
			elif sensor_id == 'C':
				self.id_sent_message = "send caress"
				self.sent_message  = int(value)
				self.sockets_send()
			elif sensor_id == 'c':
				self.id_sent_message = "send caress"
				self.sent_message  = int(value)
				self.sockets_send()
			elif sensor_id == 'P':
				self.id_sent_message = "send buttons"
				self.sent_message  = int(value)
				self.sockets_send()

	def process_emotional_data(self):
		received_actuator_values = {}

		if self.id_received_message == "send heartbeat" :
			received_actuator_values["P"] = self.received_message
		elif self.id_received_message == "send red cheek":
			received_actuator_values["R"] = self.received_message
		elif self.id_received_message == "send green cheek":
			received_actuator_values["G"] = self.received_message
		elif self.id_received_message == "send blue cheek":
			received_actuator_values["B"] = self.received_message
		elif self.id_sent_message == "send tail position":
			received_actuator_values["S"] = self.received_message
		elif self.id_received_message == "send tail speed":
			received_actuator_values["M"] = self.received_message
		
		print(received_actuator_values)

		# Enviamos por arduino
		self.send_actuator_values(received_actuator_values)

	def receive_sensor_values(self):
		# Recibimos por el arduino
		if self.hw_sensors.in_waiting > 0:
			message = self.hw_sensors.readline().decode().strip()

			# Verificar si el mensaje termina con "\r\n"
			if message.endswith("\r\n"):
				message = message[:-2]  # Eliminar "\r\n" del final del mensaje
				
				# Clasificamos lo que nos llega del arduino
				self.process_sensor_data(message)

	def send_actuator_values(self,actuator_values):
		# Construir la cadena de texto con los valores y los IDs de los actuadores
		message = ""
		for actuator_id, actuator_value in actuator_values.items():
			message += str(actuator_value) + actuator_id

		message += "\r"

		self.hw_sensors.write(message.encode())


	async def arduino_read(self):
		self.receive_sensor_values()

	async def arduino_write(self):

		# Recibimos lo que nos llega por sockets
		self.sockets_receive()

		# Clasificamos y enviamos lo que nos llega por sockets
		self.process_emotional_data()
		


	async def run_parallel_methods(self):
		await asyncio.gather(self.arduino_read(), self.arduino_write())

	
arduino1 = arduino()

while(True):
	# Ejecutar los métodos de forma paralela
	asyncio.run(arduino1.run_parallel_methods())
		
