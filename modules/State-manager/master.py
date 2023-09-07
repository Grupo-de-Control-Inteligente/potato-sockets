import sys
import os
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(package_path)
from sockets.sockets import sockets
import json
json_path= os.path.join(package_path, 'modules/State-manager/potato_state_manager.json')



ip_master = "127.0.0.1" 

# Colocamos el ID de todos los Slaves
ip_face = "127.0.0.2"
ip_emotional_model = "127.0.0.3"
ip_dialog_manager = "127.0.0.4"
ip_knowledge_base = "127.0.0.5"
ip_speech_analizer = "127.0.0.6"
ip_arduino = "127.0.0.7"

class master():

	def __init__ (self, ip_master):
		self.list_ip_destinations = []
		self.state_manager = []
		self.master = sockets(ip_master)
		self.master.bind()
		self.run_master()

	def run_master (self):
		try:
			while True:

				# Recibimos los mensajes de los Slaves
				msg_received = self.master.receive()
				
				ip_origin = msg_received["ip_origin"]
				ip_destination = msg_received["ip_destination"]
				id_message = msg_received["id_message"]
				message = msg_received["message"]
				type_msg = msg_received["type_msg"]

				# Analizamos el destinatario del mensaje
				if ip_origin == ip_face:
					if id_message == "send audio":
						# Si la Tablet envía los datos y es un audio van al Speech Analizer
						self.list_ip_destinations.append(ip_speech_analizer)
						n_msg = 1
						message = self.master.receive()
					else:
						# Si la Tablet envía los datos y es un texto van al Modulo de Aprendizaje y al Gestor de Diálogo
						if id_message == "send text":
							self.list_ip_destinations.append(ip_knowledge_base)
							self.list_ip_destinations.append(ip_dialog_manager)
							n_msg = 2
						else:
							print("Mensaje no válido")
							self.list_ip_destinations.append(-1)
							n_msg = 0
				else:
					if ip_origin == ip_speech_analizer:
						if id_message == "send user emotion":
							# Si el Speech Analizer envía los datos y es una Emoción van al Gestor de Diálogo
							self.list_ip_destinations.append(ip_dialog_manager)
							n_msg = 1
						else:
							print("Mensaje no válido")
							self.list_ip_destinations.append(-1)
							n_msg = 0
					else:
						if ip_origin == ip_knowledge_base:
							print("Mensaje no válido")
							self.list_ip_destinations.append(-1)
							n_msg = 0
						else:
							if ip_origin == ip_dialog_manager:
								if id_message == "send answer":
									# Si el Gestor de Diálogo envía los datos y es la frase de respuesta de POTATO van a la Tablet
									self.list_ip_destinations.append(ip_face)
									n_msg = 1
								else:
									if id_message == "send interest":
										# Si el Gestor de Diálogo envía los datos y es el Interés van al Modelo Emocional
										self.list_ip_destinations.append(ip_emotional_model)
										n_msg = 1
									else:
										print("Mensaje no válido")
										self.list_ip_destinations.append(-1)
										n_msg = 0
							else:
								if ip_origin == ip_emotional_model:
									if id_message == "send POTATO emotion":
										# Si el Modelo Emocional envía los datos y es la emoción van al Gestor de Diálogo y a la cara
										self.list_ip_destinations.append(ip_dialog_manager)
										self.list_ip_destinations.append(ip_face)
										n_msg = 2
									else:
										if id_message == "send heartbeat":
											# Si el Modelo Emocional envía los datos y es la velocidad del latido va al Arduino
											self.list_ip_destinations.append(ip_arduino)
											n_msg = 1
										else:
											if id_message == "send tail speed":
												# Si el Modelo Emocional envía los datos y es la velocidad de la cola va al Arduino
												self.list_ip_destinations.append(ip_arduino)
												n_msg = 1
											else:
												print("Mensaje no válido")
												self.list_ip_destinations.append(-1)
												n_msg = 0
								else:
									if ip_origin == ip_arduino:
										if id_message == "send caress":
											self.list_ip_destinations.append(ip_emotional_model)
											n_msg = 1
										else:
											if id_message == "send light":
												self.list_ip_destinations.append(ip_emotional_model)
												n_msg = 1
											else:
													print("Mensaje no válido")
													self.list_ip_destinations.append(-1)
													n_msg = 0
									else:
										print("IP de Origen no válida")
										self.list_ip_destinations.append(-1)		
										n_msg = 0

				# Comprobamos que el destino sea válido
				if self.list_ip_destinations[0] != -1:
					# Se programa el mensaje que el Master envirará al correspondiente Slave

					for i in range (n_msg):
						potato_state_manager = {
							"ip_origin": ip_master,
							"ip_destination": self.list_ip_destinations[n_msg - (i+1)],
							"id_message": id_message,
							"message": message,
							"type_msg": type_msg
						}
						
						#response_msg = json.dumps(potato_state_manager)
						#print("Sent message: " + str(potato_state_manager))
						if(self.list_ip_destinations[n_msg-(i+1)] == potato_state_manager["ip_destination"]):
							self.master.send(potato_state_manager)
							# Guardar el state manager en un archivo json
							self.state_manager.append(potato_state_manager)
							with open(json_path, 'w') as archivo_json:
								json.dump(self.state_manager, archivo_json, indent=4)

							print("\n")
						del self.list_ip_destinations[n_msg-(i+1)]
				else:
					print("IP de destino no válido:", self.list_ip_destinations[0])
					del self.list_ip_destinations[0]

		finally:
			self.master.close()

master1 = master(ip_master)


			