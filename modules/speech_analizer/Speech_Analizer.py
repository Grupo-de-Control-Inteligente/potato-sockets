import sys
import select
import os

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(package_path)
from sockets.sockets import sockets

# Direcciones IP necesarias
ip_speechanalizer = "127.0.0.6"
ip_master = "127.0.0.1"

class speech_analizer():
	speech_analizer = sockets(ip_speechanalizer)
	speech_analizer.bind()
	speech_analizer.connect(ip_master)
	try:    
		while True:
		# Esperar a recibir datos o entrada del usuario
			# Lista de sockets para lectura (incluye el socket del servidor)
			ready_sockets, _, _ = select.select([sys.stdin, speech_analizer.fileno()], [], [])

			for sock in ready_sockets:
				if sock == speech_analizer.fileno():
					# Recibir mensaje del cliente
					msg_received = speech_analizer.receive()
					ip_origin = msg_received["ip_origin"]
					ip_destination = msg_received["ip_destination"]
					id_message = msg_received["id_message"]
					message = msg_received["message"]
					type_msg = msg_received["type_msg"]
					if id_message == "send Answer":
						print("Mensaje recibido: %s, de la IP: %s, con ID: %s" % (message, ip_origin, id_message))
				elif sock == sys.stdin:
					# Leer entrada del usuario
					user_input = input()
					
					# Enviar mensaje al cliente
					phrase_data = {
					"ip_origin": ip_speechanalizer,
					"ip_destination": ip_master,
					"id_message": "send text",
					"message": user_input,
					"type_msg": str(type(user_input))
					}
					#response_msg = json.dumps(response_data)
					speech_analizer.send(phrase_data)
					print("Sent message: " + user_input)

	finally:
		speech_analizer.close()
