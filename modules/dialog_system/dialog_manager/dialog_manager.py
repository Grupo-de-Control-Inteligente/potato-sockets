#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nlp.nlp import NLP
from nlp.interest import Interest
from dialog_manager.response_generators.rule_based.rule_based_model import RuleBasedModel
from dialog_manager.response_generators.rule_based.rule_based_model_helper import pairs_es, reflections_es, pairs_en, reflections_en
from threading import Timer
from dialog_manager.response_generators.protocol.protocol import glucose_protocol
from dialog_manager.response_generators.gpt2_emotional.gpt2_emotional import GPT2Emotional

##COMUNICACIONES: SLAVE
import sys
import os
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.append(package_path)
from sockets.sockets import sockets


############### CLIENT ###################
ip_dialogmanager = "127.0.0.4"
ip_master = "127.0.0.1"


generator = GPT2Emotional()
generator.set_gen()
user_template = "USER >"
mood_template  = "MOOD > {0}"
bot_template  = "BOT  > {0}"
user_mood = "happiness" #provisional hasta que el ModeloEmocional esté terminado
potato_mood = "happiness"

class DialogManager:

	def __init__(self):
		self.t = None  # Agrega la variable 't' como atributo de la clase
		self.dialog_manager = sockets(ip_dialogmanager)
		self.dialog_manager.bind()
		self.dialog_manager.connect(ip_master)
	

	def too_quiet(self,quiet):
		print ("quiet")
		response_data = {
			"ip_origin": ip_dialogmanager,
			"ip_destination":ip_master,
			"id_message": "send answer",
			"message": quiet,
			"type_msg": str(type(quiet))
		}
		self.dialog_manager.send(response_data)


	def converse(self, quit = "salirfueraya"):
		global message, potato_mood, user_mood

		####tiempo de respuesta####
		timeout = 30 #segundos que espera a que el usuario hable
		t = Timer(timeout, self.too_quiet, ['Estas muy callado..'])
		t.start()
		print(self.t)
		##############

		while True:
			data = self.dialog_manager.receive()
							# if(data["id_message"] != "send POTATO emotion"):
				#     print ("Received message: " + str(data))

			id_message = data["id_message"]
			message = data["message"]
				
			# Nos llega la frase  
			if id_message == "send text":
				t.cancel()
				timeout = 30
				phrase = NLP(message)
				phrase.correct()
				message_out = phrase.msg_out
				print(user_template, message_out)
				print(f"tipo de frase > {phrase.sentence_t}")

					# Mandamos el interés al Modelo Emocional
				interest_score = Interest(message_out)
				interest_score.score()
				"""w.points()
				msg=str(w.P)"""
				print("Sent message: " + str(interest_score.P))
				response_data = {
					"ip_origin": ip_dialogmanager,
					"ip_destination": ip_master,
					"id_message": "send interest",
					"message":  interest_score.P,
					"type_msg": str(type(interest_score.P))
				}

				self.dialog_manager.send(response_data)

				print(f"interés de la palabra entre 0-100:  > {interest_score.P}")

					# Ponemos un Timer para que, en caso de que el usuario no hable en mucho tiempo, POTATO le conteste
					
					# Mandamos la respuesta a la cara
				if potato_mood == "Miedo":
					p = glucose_protocol()
					p.do_protocol()
				else:
					rules = RuleBasedModel(pairs_es, pairs_en, reflections_es, reflections_en)
					response = rules._respond(message) # Look up for a respond to the message
						
					if response is None:
						generator.do_gen(phrase.msg_out_eng, user_mood, potato_mood)
						response = generator.txt_out
					print(mood_template.format(potato_mood))
					print(bot_template.format(response))
					print("Sent message: " + response)
					print("\n")

					response_data = {
					"ip_origin": ip_dialogmanager,
					"ip_destination":ip_master,
					"id_message": "send answer",
					"message": response,
					"type_msg": str(type(response))
					}
					   
				self.dialog_manager.send(response_data)

				t = Timer(timeout, self.too_quiet, args=['¿Como va todo?'])
				t.start()
			else:
				if id_message == "send POTATO emotion":
					potato_mood = message
				else:
					if id_message == "send User emotion":
						user_mood = message
					else: print("Mensaje no válido")
			
			


#         buff, saddr = clientSock.recvfrom(1024) # buffer size is 1024 bytes
#         user_input = buff.decode('utf-8')
#         t.cancel()
#         while user_input != quit:
#         #while True:
#             if user_input:
#                 while user_input[-1] in "!.":
#                     user_input = user_input[:-1]
#                 print("")
#                 print(user_template, user_input)
#                 n = NLP(user_input)
#                 n.correct()
#                 user_input = n.msg_out
#                 print(user_template, user_input)
#                 print(f"tipo de frase > {n.sentence_t}")
#                 w = Interest(user_input)
#                 w.points()
#                 ####MANDAR INTERÉS A FUZZY####
#                 msg=str(w.P)
#                 buff = msg.encode()
#                 #clientSock.sendall(buff)
#                 ##############################
#                 print(f"interés de la palabra entre 0-100:  > {w.P}")
#                 """ buff, saddr = clientSock.recvfrom(1024) # buffer size is 1024 bytes
#                 msg = buff.decode('utf-8')
#                 print ("Received message: " + msg) """
#                 mood = msg
#                 ##############################
#                 if mood == "Miedo":
#                     p=Protocol()
#                     p.do_protocolo()
#                 else:
#                     dm = RuleBasedModel(pairs_es, pairs_en, reflections_es, reflections_en)
#                     response = dm._respond(user_input) # Look up for a respond to the message
#                     if response is None:
#                         gn.do_gen(n.msg_out_eng)
#                         response=gn.txt_out
#                     print(mood_template.format(mood))
#                     print(bot_template.format(response))
#                     print("Sent message: " + response)
#                     buff = response.encode()
#                     csent = clientSock.sendto(buff, saddr)
#                     print('sent %s bytes back to %s\n' % (csent, saddr))
#             ####tiempo de respuesta####
#             t = Timer(timeout, too_quiet, args=['¿Cómo va todo?'])
#             t.start()
#             buff, saddr = clientSock.recvfrom(1024) # buffer size is 1024 bytes
#             user_input = buff.decode('utf-8')
#             t.cancel()
#             ####tiempo de respuesta####
#             """timeout = 10
#             t = Timer(timeout, print, ['¿Cómo va todo?'])
#             t.start()
#             ########
#             try:
#                 user_input = input()
#                 t.cancel()
#             except:
#                 user_input = input()
#                 t.cancel()"""
			
			
			
#         if user_input == quit:
#             buff = "fin".encode()
#             clientSock.sendall(buff)
#             clientSock.close()

# def too_quiet(quiet):
#     print ("quiet")
#     quiet = quiet.encode()
#     sent_quiet = clientSock.sendto(quiet, saddr)
#     print("Sent message: " + quiet)
#     print('sent %s bytes back to %s\n' % (sent_quiet, saddr))
