import sys
import select
import os
import base64

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(package_path)
from sockets.sockets import sockets


# Direcciones IP necesarias
ip_face = "127.0.0.2"
ip_master = "127.0.0.1"

path = os.path.abspath(__file__)

class face():
	face = sockets(ip_face)
	face.bind()
	face.connect(ip_master)
	i=0
	seq = 0
	try:    
		while True:
		# Esperar a recibir datos o entrada del usuario
			# Lista de sockets para lectura (incluye el socket del servidor)
			ready_sockets, _, _ = select.select([sys.stdin, face.fileno()], [], [])

			for sock in ready_sockets:
				if sock == face.fileno():
					# Recibir mensaje del cliente
					msg_received = face.receive()
					ip_origin = msg_received["ip_origin"]
					ip_destination = msg_received["ip_destination"]
					id_message = msg_received["id_message"]
					message = msg_received["message"]
					type_msg = msg_received["type_msg"]
					if id_message == "send answer":
						if(msg_received["seq"] - seq >10):
							print("Mensaje recibido: %s, de la IP: %s, con ID: %s %s" % (message, ip_origin, id_message,msg_received["seq"]))
							seq = msg_received["seq"]
					

				elif sock == sys.stdin:
					# Leer entrada del usuario
					user_input = input()


					
					# Enviar mensaje al cliente
					phrase_data = {
					"ip_origin": ip_face,
					"ip_destination": ip_master,
					"id_message": "send text",
					"message": user_input,
					"type_msg": str(type(user_input))
					}
					#response_msg = json.dumps(response_data)
					face.send(phrase_data)
					# print("Sent message: " + user_input)
					print("\n")

	finally:
		face.close()

