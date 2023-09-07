import sys
import select
import os

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(package_path)
from sockets.sockets import sockets

# Direcciones IP necesarias
ip_knowledgebase = "127.0.0.5"
ip_master = "127.0.0.1"

class knowledge_base():
	knowledge_base = sockets(ip_knowledgebase)
	knowledge_base.bind()
	knowledge_base.connect()
	try:    
		while True:
		# Esperar a recibir datos o entrada del usuario
			# Lista de sockets para lectura (incluye el socket del servidor)
			ready_sockets, _, _ = select.select([sys.stdin, knowledge_base.fileno()], [], [])

			for sock in ready_sockets:
				if sock == knowledge_base.fileno():
					# Recibir mensaje del cliente
					msg_received = knowledge_base.receive()
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
					"ip_origin": ip_knowledgebase,
					"ip_destination": ip_master,
					"id_message": "send text",
					"message": user_input,
					"type_msg": str(type(user_input))
					}
					#response_msg = json.dumps(response_data)
					knowledge_base.send(phrase_data)
					print("Sent message: " + user_input)

	finally:
		knowledge_base.close()
