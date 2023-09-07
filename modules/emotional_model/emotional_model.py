# -*- coding: utf-8 -*-
"""
Emotional model- Generate emotion using a Fuzzy model
"""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from threading import Timer
import time

##COMUNICACIONES
import sys
import os
import threading

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(package_path)
from sockets.sockets import sockets


###VARIABLES DE ENTRADA SIMULADAS###
luz=900
caricia=2
interes_frase=50
glucosa=75

###CONSTANTES INICIALES SIMULADAS###
bateria=100
const_animica=10 #,100
const_alerta=20
const_interes=10

### CLASE QUE CONTIENE TODO EL CONTROLADOR BORROSO###
# para cada controlador se define una funcion set_, que se ejecuta al principio para definir el controlador
#y una funcion do_, que se ejecuta en bucle durante la duración del control

class Fuzzy():
	def __init__(self):
		self.it=0
		self.Habla_Interes= None
		self.Luz_Alerta = None
		self.Alerta_Latido = None
		self.Caricia_Animica = None
		self.Animica_ColaVel = None
		self.Alerta_Animica = None
		self.pre_AlIn = const_alerta #para el retardo
		self.pre_AnIn = const_animica #para el retardo
		self.pre_InIn = const_interes #para el retardo
		self.an_in_col = [[const_animica],[const_interes],[0]]
		self.al_an_eg = [[const_alerta],[const_animica],[50]]#para plotear alerta-animica-estado
		self.alerta_ret = [[const_alerta],[const_alerta]]
		self.animica_ret = [[const_animica],[const_animica]]
		self.interes_ret = [[const_interes],[const_interes]]

		self.caricia = 2
		self.interes_frase = 50
		self.luz = 900
		self.glucosa = 75
		######CLIENT#####
		self.mood = "happiness"
	def set_Habla_Interes(self):
		# New Antecedent/Consequent 
		Habla = ctrl.Antecedent(np.arange(0, 101, 1), 'Habla')
		InteresIn = ctrl.Antecedent(np.arange(0, 101, 1), 'InteresIn')
		Interes = ctrl.Consequent(np.arange(0, 101, 1), 'Interes')
		
		#INTERES AUX
		InteresIn['MINDIFERENCIA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0,0, 25])
		InteresIn['INDIFERENCIA'] = fuzz.trimf(np.arange(0, 101, 1), [0, 25, 50])
		InteresIn['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		InteresIn['INTERES'] = fuzz.trimf(np.arange(0, 101, 1), [50, 75, 100])
		InteresIn['MINTERES'] = fuzz.trapmf(np.arange(0, 101, 1), [75, 100, 100, 100])
		
		#INTERES
		Interes['MINDIFERENCIA'] = fuzz.trapmf(np.arange(0, 101, 1),[0, 0,0, 25])
		Interes['INDIFERENCIA'] = fuzz.trimf(np.arange(0, 101, 1), [0, 25, 50])
		Interes['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		Interes['INTERES'] = fuzz.trimf(np.arange(0, 101, 1), [50, 75, 100])
		Interes['MINTERES'] = fuzz.trapmf(np.arange(0, 101, 1), [75, 100, 100, 100])
		
		#HABLA
		Habla['IRRELEVANTE'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 20, 50])
		Habla['RELEVANTE'] = fuzz.trimf(np.arange(0, 101, 1), [20, 50, 80])
		Habla['MRELEVANTE'] = fuzz.trapmf(np.arange(0, 101, 1), [50, 80, 100, 100])
		
		#REGLAS
		
		rule1 = ctrl.Rule(Habla['IRRELEVANTE'] & InteresIn['MINDIFERENCIA'] , Interes['MINDIFERENCIA'])
		rule2 = ctrl.Rule(Habla['IRRELEVANTE'] & InteresIn['INDIFERENCIA'] , Interes['MINDIFERENCIA'])
		rule3 = ctrl.Rule(Habla['IRRELEVANTE'] & InteresIn['NORMAL'] , Interes['INDIFERENCIA'])
		rule4 = ctrl.Rule(Habla['IRRELEVANTE'] & InteresIn['INTERES'] , Interes['INDIFERENCIA'])
		rule5 = ctrl.Rule(Habla['IRRELEVANTE'] & InteresIn['MINTERES'] , Interes['NORMAL'])
		
		rule6 = ctrl.Rule(Habla['RELEVANTE'] & InteresIn['MINDIFERENCIA'] , Interes['INDIFERENCIA'])
		rule7 = ctrl.Rule(Habla['RELEVANTE'] & InteresIn['INDIFERENCIA'] , Interes['NORMAL'])
		rule8 = ctrl.Rule(Habla['RELEVANTE'] & InteresIn['NORMAL'] , Interes['INTERES'])
		rule9 = ctrl.Rule(Habla['RELEVANTE'] & InteresIn['INTERES'] , Interes['MINTERES'])
		rule10 = ctrl.Rule(Habla['RELEVANTE'] & InteresIn['MINTERES'] , Interes['MINTERES'])
		
		rule11 = ctrl.Rule(Habla['MRELEVANTE'] & InteresIn['MINDIFERENCIA'] , Interes['INTERES'])
		rule12 = ctrl.Rule(Habla['MRELEVANTE'] & InteresIn['INDIFERENCIA'] , Interes['INTERES'])
		rule13 = ctrl.Rule(Habla['MRELEVANTE'] & InteresIn['NORMAL'] , Interes['MINTERES'])
		rule14 = ctrl.Rule(Habla['MRELEVANTE'] & InteresIn['INTERES'] , Interes['MINTERES'])
		rule15 = ctrl.Rule(Habla['MRELEVANTE'] & InteresIn['MINTERES'] , Interes['MINTERES'])
		
		
		
		#CONTROLADOR LUZ-ALERTA
		Habla_Interes_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15])
		
		Habla_Interes = ctrl.ControlSystemSimulation(Habla_Interes_ctrl)
		Habla_Interes.input['InteresIn'] = const_interes
		Habla_Interes.input['Habla'] = self.interes_frase
		Habla_Interes.compute()
		self.Habla_Interes = Habla_Interes
	def do_Habla_Interes(self):
		if self.Habla_Interes == None:
			self.set_Habla_Interes()
		Habla_Interes=self.Habla_Interes
		Habla_Interes.input['Habla'] = self.interes_frase                    #leer por sockets
		Habla_Interes.input['InteresIn'] = self.Habla_Interes.output['Interes']
		
		##RETARDO##
		ret_InIn = (self.pre_InIn*const_interes+Habla_Interes.output['Interes'])/(const_interes+1)
		self.pre_InIn=ret_InIn
		self.interes_ret[0].append(Habla_Interes.output['Interes'])
		self.interes_ret[1].append(ret_InIn)
		
		# Crunch the numbers
		Habla_Interes.compute()
		#print ("Interes {}".format(Habla_Interes.output['Interes']))
		#Luz_Alerta.input['Luz'].view(sim=Luz_Alerta)
		self.Habla_Interes = Habla_Interes
		
	def set_Luz_Alerta(self):
		Luz = ctrl.Antecedent(np.arange(0, 1024, 1), 'Luz')
		Glucosa = ctrl.Antecedent(np.arange(0, 241, 1), 'Glucosa')
		AlertaIn = ctrl.Antecedent(np.arange(0, 101, 1), 'AlertaIn')
		Alerta = ctrl.Consequent(np.arange(0, 101, 1), 'Alerta')
		
		#LUZ
		Luz['MOSCURO'] = fuzz.trapmf(np.arange(0, 1024, 1), [0, 0, 100, 200])
		Luz['OSCURO'] = fuzz.trimf(np.arange(0, 1024, 1), [100, 200, 400])
		Luz['NORMAL'] = fuzz.trimf(np.arange(0, 1024, 1), [200, 400, 700])
		Luz['CLARO'] = fuzz.trimf(np.arange(0, 1024, 1), [400, 700, 900])
		Luz['MCLARO'] = fuzz.trapmf(np.arange(0, 1024, 1), [700, 900, 1023, 1023])
		
		#BATERIA
		Glucosa['MBAJA'] = fuzz.trapmf(np.arange(0, 241, 1), [0, 0, 40, 70])
		Glucosa['BAJA'] = fuzz.trimf(np.arange(0, 241, 1), [40, 70, 100])
		Glucosa['MEDIA'] = fuzz.trapmf(np.arange(0, 241, 1), [70, 100, 120, 180])
		Glucosa['ALTA'] = fuzz.trapmf(np.arange(0, 241, 1), [120, 180, 240, 240])
		#ALERTA AUX
		AlertaIn['CALMA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 25, 50])
		AlertaIn['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		AlertaIn['MIEDO'] = fuzz.trapmf(np.arange(0, 101, 1), [50, 75, 100, 100])
		
		#ALERTA 
		Alerta['CALMA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 25, 50])
		Alerta['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		Alerta['MIEDO'] = fuzz.trapmf(np.arange(0, 101, 1), [50, 75, 100, 100])
		
		#REGLAS
		#batería alta
		rule1 = ctrl.Rule(Glucosa['ALTA'] & Luz['MOSCURO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule2 = ctrl.Rule(Glucosa['ALTA'] & Luz['MOSCURO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule3 = ctrl.Rule(Glucosa['ALTA'] & Luz['MOSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule4 = ctrl.Rule(Glucosa['ALTA'] & Luz['OSCURO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule5 = ctrl.Rule(Glucosa['ALTA'] & Luz['OSCURO'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule6 = ctrl.Rule(Glucosa['ALTA'] & Luz['OSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule7 = ctrl.Rule(Glucosa['ALTA'] & Luz['NORMAL'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule8 = ctrl.Rule(Glucosa['ALTA'] & Luz['NORMAL'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule9 = ctrl.Rule(Glucosa['ALTA'] & Luz['NORMAL'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		rule10 = ctrl.Rule(Glucosa['ALTA'] & Luz['CLARO'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule11 = ctrl.Rule(Glucosa['ALTA'] & Luz['CLARO'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule12 = ctrl.Rule(Glucosa['ALTA'] & Luz['CLARO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		rule13 = ctrl.Rule(Glucosa['ALTA'] & Luz['MCLARO'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule14 = ctrl.Rule(Glucosa['ALTA'] & Luz['MCLARO'] & AlertaIn['NORMAL'], Alerta['CALMA'])
		rule15 = ctrl.Rule(Glucosa['ALTA'] & Luz['MCLARO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		#glucosa media
		rule16 = ctrl.Rule(Glucosa['MEDIA'] & Luz['MOSCURO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule17 = ctrl.Rule(Glucosa['MEDIA'] & Luz['MOSCURO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule18 = ctrl.Rule(Glucosa['MEDIA'] & Luz['MOSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule19 = ctrl.Rule(Glucosa['MEDIA'] & Luz['OSCURO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule20 = ctrl.Rule(Glucosa['MEDIA'] & Luz['OSCURO'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule21 = ctrl.Rule(Glucosa['MEDIA'] & Luz['OSCURO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		rule22 = ctrl.Rule(Glucosa['MEDIA'] & Luz['NORMAL'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule23 = ctrl.Rule(Glucosa['MEDIA'] & Luz['NORMAL'] & AlertaIn['NORMAL'], Alerta['CALMA'])
		rule24 = ctrl.Rule(Glucosa['MEDIA'] & Luz['NORMAL'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		rule25 = ctrl.Rule(Glucosa['MEDIA'] & Luz['CLARO'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule26 = ctrl.Rule(Glucosa['MEDIA'] & Luz['CLARO'] & AlertaIn['NORMAL'], Alerta['CALMA'])
		rule27 = ctrl.Rule(Glucosa['MEDIA'] & Luz['CLARO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		rule28 = ctrl.Rule(Glucosa['MEDIA'] & Luz['MCLARO'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule29 = ctrl.Rule(Glucosa['MEDIA'] & Luz['MCLARO'] & AlertaIn['NORMAL'], Alerta['CALMA'])
		rule30 = ctrl.Rule(Glucosa['MEDIA'] & Luz['MCLARO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		#glucosa BAJA
		rule31 = ctrl.Rule(Glucosa['BAJA'] & Luz['MOSCURO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule32 = ctrl.Rule(Glucosa['BAJA'] & Luz['MOSCURO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule33 = ctrl.Rule(Glucosa['BAJA'] & Luz['MOSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule34 = ctrl.Rule(Glucosa['BAJA'] & Luz['OSCURO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule35 = ctrl.Rule(Glucosa['BAJA'] & Luz['OSCURO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule36 = ctrl.Rule(Glucosa['BAJA'] & Luz['OSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule37 = ctrl.Rule(Glucosa['BAJA'] & Luz['NORMAL'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule38 = ctrl.Rule(Glucosa['BAJA'] & Luz['NORMAL'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule39 = ctrl.Rule(Glucosa['BAJA'] & Luz['NORMAL'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule40 = ctrl.Rule(Glucosa['BAJA'] & Luz['CLARO'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule41 = ctrl.Rule(Glucosa['BAJA'] & Luz['CLARO'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule42 = ctrl.Rule(Glucosa['BAJA'] & Luz['CLARO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		rule43 = ctrl.Rule(Glucosa['BAJA'] & Luz['MCLARO'] & AlertaIn['CALMA'], Alerta['CALMA'])
		rule44 = ctrl.Rule(Glucosa['BAJA'] & Luz['MCLARO'] & AlertaIn['NORMAL'], Alerta['CALMA'])
		rule45 = ctrl.Rule(Glucosa['BAJA'] & Luz['MCLARO'] & AlertaIn['MIEDO'], Alerta['NORMAL'])
		#glucosa Muy BAJA
		rule46 = ctrl.Rule(Glucosa['MBAJA'] & Luz['MOSCURO'] & AlertaIn['CALMA'], Alerta['MIEDO'])
		rule47 = ctrl.Rule(Glucosa['MBAJA'] & Luz['MOSCURO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule48 = ctrl.Rule(Glucosa['MBAJA'] & Luz['MOSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule49 = ctrl.Rule(Glucosa['MBAJA'] & Luz['OSCURO'] & AlertaIn['CALMA'], Alerta['MIEDO'])
		rule50 = ctrl.Rule(Glucosa['MBAJA'] & Luz['OSCURO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule51 = ctrl.Rule(Glucosa['MBAJA'] & Luz['OSCURO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule52 = ctrl.Rule(Glucosa['MBAJA'] & Luz['NORMAL'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule53 = ctrl.Rule(Glucosa['MBAJA'] & Luz['NORMAL'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule54 = ctrl.Rule(Glucosa['MBAJA'] & Luz['NORMAL'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule55 = ctrl.Rule(Glucosa['MBAJA'] & Luz['CLARO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule56 = ctrl.Rule(Glucosa['MBAJA'] & Luz['CLARO'] & AlertaIn['NORMAL'], Alerta['MIEDO'])
		rule57 = ctrl.Rule(Glucosa['MBAJA'] & Luz['CLARO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		rule58 = ctrl.Rule(Glucosa['MBAJA'] & Luz['MCLARO'] & AlertaIn['CALMA'], Alerta['NORMAL'])
		rule59 = ctrl.Rule(Glucosa['MBAJA'] & Luz['MCLARO'] & AlertaIn['NORMAL'], Alerta['NORMAL'])
		rule60 = ctrl.Rule(Glucosa['MBAJA'] & Luz['MCLARO'] & AlertaIn['MIEDO'], Alerta['MIEDO'])
		#CONTROLADOR LUZ-ALERTA
		Luz_Alerta_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15
										 , rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30
										 , rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45, rule46
										 , rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60])
		
		Luz_Alerta = ctrl.ControlSystemSimulation(Luz_Alerta_ctrl)
		Luz_Alerta.input['Glucosa'] = 20
		Luz_Alerta.input['Luz'] = 120
		Luz_Alerta.input['AlertaIn'] = 49.999
		
		# Crunch the numbers
		Luz_Alerta.compute()
		#print (Luz_Alerta.output['Alerta'])
		self.Luz_Alerta=Luz_Alerta
		return 1
	
	def do_Luz_Alerta(self):
		if self.Luz_Alerta == None:
			self.set_Luz_Alerta()
		Luz_Alerta=self.Luz_Alerta
		Luz_Alerta.input['Glucosa'] = self.glucosa #leer del lmc
		Luz_Alerta.input['Luz'] = self.luz #leer del lmc
		Luz_Alerta.input['AlertaIn'] = Luz_Alerta.output['Alerta']
		
		##RETARDO##
		ret_AlIn = (self.pre_AlIn*const_alerta+Luz_Alerta.output['Alerta'])/(const_alerta+1)
		Luz_Alerta.input['AlertaIn'] = ret_AlIn
		self.pre_AlIn=ret_AlIn
		self.alerta_ret[0].append(Luz_Alerta.output['Alerta'])
		self.alerta_ret[1].append(ret_AlIn)
		
		# Crunch the numbers
		Luz_Alerta.compute()
		#print ("Alerta {}".format(Luz_Alerta.output['Alerta']))
		#Luz_Alerta.input['Luz'].view(sim=Luz_Alerta)
		self.Luz_Alerta = Luz_Alerta

	def set_Alerta_Latido(self):
		# AlertaIn es la entrada : AlertaIn = ctrl.Antecedent(np.arange(0, 101, 1), 'AlertaIn')
		AlertaIn = ctrl.Antecedent(np.arange(0, 101, 1), 'AlertaIn')
		vLatido = ctrl.Consequent(np.arange(30, 301, 1), 'vLatido')
		
		#ALERTA AUX
		AlertaIn['CALMA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 25, 50])
		AlertaIn['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		AlertaIn['MIEDO'] = fuzz.trapmf(np.arange(0, 101, 1), [50, 75, 100, 100])
		
		#LATIDO salida
		vLatido['CALMA'] = fuzz.trapmf(np.arange(30, 301, 1), [30, 30, 50, 80])
		vLatido['NORMAL'] = fuzz.trimf(np.arange(30, 301, 1), [50, 80, 120])
		vLatido['MIEDO'] = fuzz.trapmf(np.arange(30, 301, 1), [80, 120, 300, 300])
		
		#REGLAS
		rule1 = ctrl.Rule(AlertaIn['CALMA'], vLatido['CALMA'])
		rule2 = ctrl.Rule(AlertaIn['NORMAL'], vLatido['NORMAL'])
		rule3 = ctrl.Rule(AlertaIn['MIEDO'], vLatido['MIEDO'])
		
		#CONTROLADOR ALERTA-LATIDO
		Alerta_Latido_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
		
		Alerta_Latido = ctrl.ControlSystemSimulation(Alerta_Latido_ctrl)
		Alerta_Latido.input['AlertaIn'] = self.Luz_Alerta.output['Alerta'] #toma como entrada la salida de alerta latido
		
		# Crunch the numbers
		Alerta_Latido.compute()
		#vLatido.view(sim=Alerta_Latido)
		self.Alerta_Latido=Alerta_Latido
		
	def do_Alerta_Latido(self):
		if self.Alerta_Latido == None:
			self.set_Alerta_Latido()
		self.Alerta_Latido.input['AlertaIn'] = self.pre_AlIn
		self.Alerta_Latido.compute()
		#print ("Vlatido {}".format(self.Alerta_Latido.output['vLatido']))
	
	def set_Caricia_Animica(self):
		Caricia = ctrl.Antecedent(np.arange(0, 7, 1), 'Caricia')
		Bateria = ctrl.Antecedent(np.arange(0, 101, 1), 'Bateria')
		AnimicaIn = ctrl.Antecedent(np.arange(0, 121, 1), 'AnimicaIn')
		Animica = ctrl.Consequent(np.arange(0, 121, 1), 'Animica')
		
		#BATERIA
		Bateria['BAJA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 20, 50])
		Bateria['MEDIA'] = fuzz.trimf(np.arange(0, 101, 1), [20, 50, 80])
		Bateria['ALTA'] = fuzz.trapmf(np.arange(0, 101, 1), [50, 80, 100, 100])
		
		#CARICIA multiplicar por 2 la entrada
		Caricia['NADA'] = fuzz.trapmf(np.arange(0, 7, 1), [4,5,6,6])
		Caricia['POCO'] = fuzz.trapmf(np.arange(0, 7, 1), [0,1,5, 6])
		Caricia['MUCHO'] = fuzz.trapmf(np.arange(0, 7, 1), [0, 0,1,2])
		
		#AnimicaIn AUX
		AnimicaIn['MTRISTE'] = fuzz.trapmf(np.arange(0, 121, 1), [0, 0, 15, 30])
		AnimicaIn['TRISTE'] = fuzz.trimf(np.arange(0, 121, 1), [15, 30, 45])
		AnimicaIn['NORMAL'] = fuzz.trimf(np.arange(0, 121, 1), [30, 45, 80])
		AnimicaIn['ALEGRE'] = fuzz.trimf(np.arange(0, 121, 1), [60, 80, 100])
		AnimicaIn['MALEGRE'] = fuzz.trapmf(np.arange(0, 121, 1), [80, 100, 120, 120])
		
		#ALERTA 
		Animica['MTRISTE'] = fuzz.trapmf(np.arange(0, 121, 1), [0, 0, 15, 30])
		Animica['TRISTE'] = fuzz.trimf(np.arange(0, 121, 1), [15, 30, 45])
		Animica['NORMAL'] = fuzz.trimf(np.arange(0, 121, 1), [30, 45, 80])
		Animica['ALEGRE'] = fuzz.trimf(np.arange(0, 121, 1), [60, 80, 100])
		Animica['MALEGRE'] = fuzz.trapmf(np.arange(0, 121, 1), [80, 100, 120, 120])
		
		#REGLAS
		#batería alta
		rule1 = ctrl.Rule(Bateria['ALTA'] & Caricia['NADA'] & AnimicaIn['MTRISTE'], Animica['MTRISTE'])
		rule2 = ctrl.Rule(Bateria['ALTA'] & Caricia['NADA'] & AnimicaIn['TRISTE'], Animica['TRISTE'])
		rule3 = ctrl.Rule(Bateria['ALTA'] & Caricia['NADA']& AnimicaIn['NORMAL'], Animica['NORMAL'])
		rule4 = ctrl.Rule(Bateria['ALTA'] & Caricia['NADA'] & AnimicaIn['ALEGRE'], Animica['ALEGRE'])
		rule5 = ctrl.Rule(Bateria['ALTA'] & Caricia['NADA'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		rule6 = ctrl.Rule(Bateria['ALTA'] & Caricia['POCO'] & AnimicaIn['MTRISTE'], Animica['TRISTE'])
		rule7 = ctrl.Rule(Bateria['ALTA'] & Caricia['POCO'] & AnimicaIn['TRISTE'], Animica['NORMAL'])
		rule8 = ctrl.Rule(Bateria['ALTA'] & Caricia['POCO']& AnimicaIn['NORMAL'], Animica['NORMAL'])
		rule9 = ctrl.Rule(Bateria['ALTA'] & Caricia['POCO'] & AnimicaIn['ALEGRE'], Animica['MALEGRE'])
		rule10 = ctrl.Rule(Bateria['ALTA'] & Caricia['POCO'] & AnimicaIn['MALEGRE'], Animica['MALEGRE'])
		rule11 = ctrl.Rule(Bateria['ALTA'] & Caricia['MUCHO'] & AnimicaIn['MTRISTE'], Animica['TRISTE'])
		rule12 = ctrl.Rule(Bateria['ALTA'] & Caricia['MUCHO'] & AnimicaIn['TRISTE'], Animica['NORMAL'])
		rule13 = ctrl.Rule(Bateria['ALTA'] & Caricia['MUCHO']& AnimicaIn['NORMAL'], Animica['ALEGRE'])
		rule14 = ctrl.Rule(Bateria['ALTA'] & Caricia['MUCHO'] & AnimicaIn['ALEGRE'], Animica['ALEGRE'])
		rule15 = ctrl.Rule(Bateria['ALTA'] & Caricia['MUCHO'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		
		#bateria media
		rule16 = ctrl.Rule(Bateria['MEDIA'] & Caricia['NADA'] & AnimicaIn['MTRISTE'], Animica['MTRISTE'])
		rule17 = ctrl.Rule(Bateria['MEDIA'] & Caricia['NADA'] & AnimicaIn['TRISTE'], Animica['TRISTE'])
		rule18 = ctrl.Rule(Bateria['MEDIA'] & Caricia['NADA']& AnimicaIn['NORMAL'], Animica['NORMAL'])
		rule19 = ctrl.Rule(Bateria['MEDIA'] & Caricia['NADA'] & AnimicaIn['ALEGRE'], Animica['ALEGRE'])
		rule20 = ctrl.Rule(Bateria['MEDIA'] & Caricia['NADA'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		rule21 = ctrl.Rule(Bateria['MEDIA'] & Caricia['POCO'] & AnimicaIn['MTRISTE'], Animica['TRISTE'])
		rule22 = ctrl.Rule(Bateria['MEDIA'] & Caricia['POCO'] & AnimicaIn['TRISTE'], Animica['NORMAL'])
		rule23 = ctrl.Rule(Bateria['MEDIA'] & Caricia['POCO']& AnimicaIn['NORMAL'], Animica['ALEGRE'])
		rule24 = ctrl.Rule(Bateria['MEDIA'] & Caricia['POCO'] & AnimicaIn['ALEGRE'], Animica['MALEGRE'])
		rule25 = ctrl.Rule(Bateria['MEDIA'] & Caricia['POCO'] & AnimicaIn['MALEGRE'], Animica['MALEGRE'])
		rule26 = ctrl.Rule(Bateria['MEDIA'] & Caricia['MUCHO'] & AnimicaIn['MTRISTE'], Animica['TRISTE'])
		rule27 = ctrl.Rule(Bateria['MEDIA'] & Caricia['MUCHO'] & AnimicaIn['TRISTE'], Animica['NORMAL'])
		rule28 = ctrl.Rule(Bateria['MEDIA'] & Caricia['MUCHO']& AnimicaIn['NORMAL'], Animica['ALEGRE'])
		rule29 = ctrl.Rule(Bateria['MEDIA'] & Caricia['MUCHO'] & AnimicaIn['ALEGRE'], Animica['ALEGRE'])
		rule30 = ctrl.Rule(Bateria['MEDIA'] & Caricia['MUCHO'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		#bateria baja
		rule31 = ctrl.Rule(Bateria['BAJA'] & Caricia['NADA'] & AnimicaIn['MTRISTE'], Animica['MTRISTE'])
		rule32 = ctrl.Rule(Bateria['BAJA'] & Caricia['NADA'] & AnimicaIn['TRISTE'], Animica['TRISTE'])
		rule33 = ctrl.Rule(Bateria['BAJA'] & Caricia['NADA']& AnimicaIn['NORMAL'], Animica['TRISTE'])
		rule34 = ctrl.Rule(Bateria['BAJA'] & Caricia['NADA'] & AnimicaIn['ALEGRE'], Animica['NORMAL'])
		rule35 = ctrl.Rule(Bateria['BAJA'] & Caricia['NADA'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		rule36 = ctrl.Rule(Bateria['BAJA'] & Caricia['POCO'] & AnimicaIn['MTRISTE'], Animica['TRISTE'])
		rule37 = ctrl.Rule(Bateria['BAJA'] & Caricia['POCO'] & AnimicaIn['TRISTE'], Animica['NORMAL'])
		rule38 = ctrl.Rule(Bateria['BAJA'] & Caricia['POCO']& AnimicaIn['NORMAL'], Animica['NORMAL'])
		rule39 = ctrl.Rule(Bateria['BAJA'] & Caricia['POCO'] & AnimicaIn['ALEGRE'], Animica['ALEGRE'])
		rule40 = ctrl.Rule(Bateria['BAJA'] & Caricia['POCO'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		rule41 = ctrl.Rule(Bateria['BAJA'] & Caricia['MUCHO'] & AnimicaIn['MTRISTE'], Animica['TRISTE'])
		rule42 = ctrl.Rule(Bateria['BAJA'] & Caricia['MUCHO'] & AnimicaIn['TRISTE'], Animica['NORMAL'])
		rule43 = ctrl.Rule(Bateria['BAJA'] & Caricia['MUCHO']& AnimicaIn['NORMAL'], Animica['NORMAL'])
		rule44 = ctrl.Rule(Bateria['BAJA'] & Caricia['MUCHO'] & AnimicaIn['ALEGRE'], Animica['ALEGRE'])
		rule45 = ctrl.Rule(Bateria['BAJA'] & Caricia['MUCHO'] & AnimicaIn['MALEGRE'], Animica['ALEGRE'])
		#CONTROLADOR CARICIA-ANIMICA
		Caricia_Animica_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15
										 , rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30
										 , rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45])
		
		Caricia_Animica = ctrl.ControlSystemSimulation(Caricia_Animica_ctrl)
		Caricia_Animica.input['Bateria'] = bateria #meter valores base
		Caricia_Animica.input['Caricia'] = 2*self.caricia #meter valores base
		Caricia_Animica.input['AnimicaIn'] = const_animica #meter valores base
		
		# Crunch the numbers
		Caricia_Animica.compute()
		#Animica.view(sim=Caricia_Animica)
		self.Caricia_Animica = Caricia_Animica
		
	def do_Caricia_Animica(self):
		if self.Caricia_Animica == None:
			self.set_Caricia_Animica()
		Caricia_Animica=self.Caricia_Animica
		Caricia_Animica.input['Bateria'] = bateria #leer del lmc
		Caricia_Animica.input['Caricia'] = 2*self.caricia #leer del lmc
		##RETARDO##
		ret_AnIn = (self.pre_AnIn*const_animica + Caricia_Animica.output['Animica'])/(const_animica+1)
		Caricia_Animica.input['AnimicaIn'] = ret_AnIn
		#print(self.pre_AnIn)
		self.pre_AnIn = ret_AnIn
		if self.pre_AnIn <= 40:
			self.mood="sadness"
		elif self.pre_AnIn > 40 and self.pre_AnIn <= 70:
			self.mood="no emotion"   
		elif self.pre_AnIn >70:
			self.mood="happiness" 
		self.animica_ret[0].append(Caricia_Animica.output['Animica']) 
		self.animica_ret[1].append(ret_AnIn) 
		#print (self.mood)
			# Crunch the numbers
		Caricia_Animica.compute()
		#print ("Animica{}".format(Caricia_Animica.output['Animica']))
			#Luz_Alerta.input['Luz'].view(sim=Luz_Alerta)
		self.Caricia_Animica=Caricia_Animica
				
	def set_Animica_ColaVel(self):
		# New Antecedent/Consequent 
		
		AnimicaIn = ctrl.Antecedent(np.arange(0, 121, 1), 'AnimicaIn')
		ColaVel = ctrl.Consequent(np.arange(0, 121, 1), 'ColaVel')
		InteresIn = ctrl.Antecedent(np.arange(0, 101, 1), 'InteresIn')
		
		#COLAVEL salida
		ColaVel['MLENTO'] = fuzz.trapmf(np.arange(0, 121, 1), [0, 0, 2, 8])
		ColaVel['LENTO'] = fuzz.trimf(np.arange(0, 121, 1), [2, 8, 14])
		ColaVel['NORMAL'] = fuzz.trimf(np.arange(0, 121, 1), [8, 14, 20])
		ColaVel['RAPIDO'] = fuzz.trimf(np.arange(0, 121, 1), [14, 20, 60])
		ColaVel['MRAPIDO'] = fuzz.trapmf(np.arange(0, 121, 1), [20, 60, 120,120])
		
		#AnimicaIn ENTRADA
		AnimicaIn['MTRISTE'] = fuzz.trapmf(np.arange(0, 121, 1), [0, 0, 15, 30])
		AnimicaIn['TRISTE'] = fuzz.trimf(np.arange(0, 121, 1), [15, 30, 45])
		AnimicaIn['NORMAL'] = fuzz.trimf(np.arange(0, 121, 1), [30, 45, 80])
		AnimicaIn['ALEGRE'] = fuzz.trimf(np.arange(0, 121, 1), [60, 80, 100])
		AnimicaIn['MALEGRE'] = fuzz.trapmf(np.arange(0, 121, 1), [80, 100, 120, 120])
		
		#INTERESIN ENTRADA
		InteresIn['MINDIFERENCIA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0,0, 25])
		InteresIn['INDIFERENCIA'] = fuzz.trimf(np.arange(0, 101, 1), [0, 25, 50])
		InteresIn['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		InteresIn['INTERES'] = fuzz.trimf(np.arange(0, 101, 1), [50, 75, 100])
		InteresIn['MINTERES'] = fuzz.trapmf(np.arange(0, 101, 1), [75, 100, 100, 100])
		
		#REGLAS
		rule1 = ctrl.Rule(AnimicaIn['MTRISTE'] & InteresIn['MINDIFERENCIA'], ColaVel['MLENTO'])
		rule2 = ctrl.Rule(AnimicaIn['TRISTE'] & InteresIn['MINDIFERENCIA'], ColaVel['MLENTO'])
		rule3 = ctrl.Rule(AnimicaIn['NORMAL'] & InteresIn['MINDIFERENCIA'], ColaVel['LENTO'])
		rule4 = ctrl.Rule(AnimicaIn['ALEGRE'] & InteresIn['MINDIFERENCIA'], ColaVel['NORMAL'])
		rule5 = ctrl.Rule(AnimicaIn['MALEGRE'] & InteresIn['MINDIFERENCIA'], ColaVel['MRAPIDO'])
		
		rule6 = ctrl.Rule(AnimicaIn['MTRISTE'] & InteresIn['INDIFERENCIA'], ColaVel['MLENTO'])
		rule7 = ctrl.Rule(AnimicaIn['TRISTE'] & InteresIn['INDIFERENCIA'], ColaVel['LENTO'])
		rule8 = ctrl.Rule(AnimicaIn['NORMAL'] & InteresIn['INDIFERENCIA'], ColaVel['LENTO'])
		rule9 = ctrl.Rule(AnimicaIn['ALEGRE'] & InteresIn['INDIFERENCIA'], ColaVel['NORMAL'])
		rule10 = ctrl.Rule(AnimicaIn['MALEGRE'] & InteresIn['INDIFERENCIA'], ColaVel['RAPIDO'])
		
		rule11 = ctrl.Rule(AnimicaIn['MTRISTE'] & InteresIn['NORMAL'], ColaVel['MLENTO'])
		rule12 = ctrl.Rule(AnimicaIn['TRISTE'] & InteresIn['NORMAL'], ColaVel['LENTO'])
		rule13 = ctrl.Rule(AnimicaIn['NORMAL'] & InteresIn['NORMAL'], ColaVel['NORMAL'])
		rule14 = ctrl.Rule(AnimicaIn['ALEGRE'] & InteresIn['NORMAL'], ColaVel['RAPIDO'])
		rule15 = ctrl.Rule(AnimicaIn['MALEGRE'] & InteresIn['NORMAL'], ColaVel['MRAPIDO'])
		
		rule16 = ctrl.Rule(AnimicaIn['MTRISTE'] & InteresIn['INTERES'], ColaVel['LENTO'])
		rule17 = ctrl.Rule(AnimicaIn['TRISTE'] & InteresIn['INTERES'], ColaVel['LENTO'])
		rule18 = ctrl.Rule(AnimicaIn['NORMAL'] & InteresIn['INTERES'], ColaVel['RAPIDO'])
		rule19 = ctrl.Rule(AnimicaIn['ALEGRE'] & InteresIn['INTERES'], ColaVel['RAPIDO'])
		rule20 = ctrl.Rule(AnimicaIn['MALEGRE'] & InteresIn['INTERES'], ColaVel['MRAPIDO'])
		
		rule21 = ctrl.Rule(AnimicaIn['MTRISTE'] & InteresIn['MINTERES'], ColaVel['MLENTO'])
		rule22 = ctrl.Rule(AnimicaIn['TRISTE'] & InteresIn['MINTERES'], ColaVel['NORMAL'])
		rule23 = ctrl.Rule(AnimicaIn['NORMAL'] & InteresIn['MINTERES'], ColaVel['RAPIDO'])
		rule24 = ctrl.Rule(AnimicaIn['ALEGRE'] & InteresIn['MINTERES'], ColaVel['MRAPIDO'])
		rule25 = ctrl.Rule(AnimicaIn['MALEGRE'] & InteresIn['MINTERES'], ColaVel['MRAPIDO'])
		#CONTROLADOR ANIMICA-COLAVEL
		Animica_ColaVel_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15
										 , rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25])
		
		Animica_ColaVel = ctrl.ControlSystemSimulation(Animica_ColaVel_ctrl)

		Animica_ColaVel.input['AnimicaIn'] = self.Caricia_Animica.output['Animica']
		Animica_ColaVel.input['InteresIn'] = self.Habla_Interes.output['Interes']
		
		# Crunch the numbers
		Animica_ColaVel.compute()
		#ColaVel.view(sim=Animica_ColaVel)
		self.Animica_ColaVel=Animica_ColaVel
		
	def do_Animica_ColaVel(self):
		if self.Animica_ColaVel == None:
			self.set_Animica_ColaVel()
		self.Animica_ColaVel.input['AnimicaIn'] = self.pre_AnIn
		self.Animica_ColaVel.input['InteresIn'] = self.pre_InIn #ponia AnimicaIn
		self.Animica_ColaVel.compute()
		self.an_in_col[0].append(self.pre_AnIn)
		self.an_in_col[1].append(self.pre_InIn)
		self.an_in_col[2].append(self.Animica_ColaVel.output['ColaVel'])
		#print ("ColaVel {}".format(self.Animica_ColaVel.output['ColaVel'])) 
	
	def set_Alerta_Animica(self):
		# New Antecedent/Consequent 
		EstadoGen = ctrl.Consequent(np.arange(0, 101, 1), 'EstadoGen')
		AnimicaIn = ctrl.Antecedent(np.arange(0, 121, 1), 'AnimicaIn')
		AlertaIn = ctrl.Antecedent(np.arange(0, 101, 1), 'AlertaIn')
		
		#ALERTA AUX
		AlertaIn['CALMA'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 25, 50])
		AlertaIn['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [25, 50, 75])
		AlertaIn['MIEDO'] = fuzz.trapmf(np.arange(0, 101, 1), [50, 75, 100, 100])
		
		#AnimicaIn AUX
		AnimicaIn['MTRISTE'] = fuzz.trapmf(np.arange(0, 121, 1), [0, 0, 15, 30])
		AnimicaIn['TRISTE'] = fuzz.trimf(np.arange(0, 121, 1), [15, 30, 45])
		AnimicaIn['NORMAL'] = fuzz.trimf(np.arange(0, 121, 1), [30, 45, 80])
		AnimicaIn['ALEGRE'] = fuzz.trimf(np.arange(0, 121, 1), [60, 80, 100])
		AnimicaIn['MALEGRE'] = fuzz.trapmf(np.arange(0, 121, 1), [80, 100, 120, 120])
		
		#ESTADOGEN
		EstadoGen['MIEDO'] = fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 20, 40])#Cambio 0,0,10,20
		EstadoGen['NORMAL'] = fuzz.trimf(np.arange(0, 101, 1), [20, 40, 60])
		EstadoGen['ALEGRE'] = fuzz.trimf(np.arange(0, 101, 1), [40, 60, 80])
		EstadoGen['ALEGRECAL'] = fuzz.trapmf(np.arange(0, 101, 1), [60, 80, 100, 100])
		
		#REGLAS
		rule1 = ctrl.Rule(AlertaIn['CALMA'] & AnimicaIn['MTRISTE'], EstadoGen['NORMAL'])
		rule2 = ctrl.Rule(AlertaIn['CALMA'] & AnimicaIn['TRISTE'], EstadoGen['NORMAL'])
		rule3 = ctrl.Rule(AlertaIn['CALMA'] & AnimicaIn['NORMAL'], EstadoGen['NORMAL'])
		rule4 = ctrl.Rule(AlertaIn['CALMA'] & AnimicaIn['ALEGRE'], EstadoGen['ALEGRE'])
		rule5 = ctrl.Rule(AlertaIn['CALMA'] & AnimicaIn['MALEGRE'], EstadoGen['ALEGRECAL'])
		rule6 = ctrl.Rule(AlertaIn['NORMAL'] & AnimicaIn['MTRISTE'], EstadoGen['NORMAL'])
		rule7 = ctrl.Rule(AlertaIn['NORMAL'] & AnimicaIn['TRISTE'], EstadoGen['NORMAL'])
		rule8 = ctrl.Rule(AlertaIn['NORMAL'] & AnimicaIn['NORMAL'], EstadoGen['NORMAL'])
		rule9 = ctrl.Rule(AlertaIn['NORMAL'] & AnimicaIn['ALEGRE'], EstadoGen['NORMAL'])
		rule10 = ctrl.Rule(AlertaIn['NORMAL'] & AnimicaIn['MALEGRE'], EstadoGen['ALEGRE'])
		rule11 = ctrl.Rule(AlertaIn['MIEDO'] & AnimicaIn['MTRISTE'], EstadoGen['MIEDO'])
		rule12 = ctrl.Rule(AlertaIn['MIEDO'] & AnimicaIn['TRISTE'], EstadoGen['MIEDO'])
		rule13 = ctrl.Rule(AlertaIn['MIEDO'] & AnimicaIn['NORMAL'], EstadoGen['MIEDO'])
		rule14 = ctrl.Rule(AlertaIn['MIEDO'] & AnimicaIn['ALEGRE'], EstadoGen['MIEDO'])
		rule15 = ctrl.Rule(AlertaIn['MIEDO'] & AnimicaIn['MALEGRE'], EstadoGen['NORMAL'])
		#CONTROLADOR ALERTA-ANIMICA
		Alerta_Animica_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15
										 ])
		
		Alerta_Animica = ctrl.ControlSystemSimulation(Alerta_Animica_ctrl)
		Alerta_Animica.input['AnimicaIn'] = self.Caricia_Animica.output['Animica']
		Alerta_Animica.input['AlertaIn'] = self.Luz_Alerta.output['Alerta']
		
		# Crunch the numbers
		Alerta_Animica.compute()
		#EstadoGen.view(sim=Alerta_Animica)
		self.Alerta_Animica=Alerta_Animica
		
	def do_Alerta_Animica(self):
		if self.Alerta_Animica == None:
			self.set_Alerta_Animica()
		self.Alerta_Animica.input['AnimicaIn'] = self.pre_AnIn
		self.Alerta_Animica.input['AlertaIn'] = self.pre_AlIn
		self.Alerta_Animica.compute()
		self.al_an_eg[0].append(self.pre_AlIn)
		self.al_an_eg[1].append(self.pre_AnIn)
		self.al_an_eg[2].append(self.Alerta_Animica.output['EstadoGen'])
		if self.Alerta_Animica.output['EstadoGen']<=30:
			self.mood= "Miedo"
		#print ("Estado Gen :{}".format(self.Alerta_Animica.output['EstadoGen'])) 
	

### FUNCION PARA EJECUTAR EL CONTRO BORROSO COMPLETO ###       

def do_Fuzzy(Fuzzy):      
	Fuzzy.do_Luz_Alerta()
	Fuzzy.do_Habla_Interes()
	Fuzzy.do_Alerta_Latido()
	Fuzzy.do_Caricia_Animica()
	Fuzzy.do_Animica_ColaVel()
	Fuzzy.do_Alerta_Animica()
	return Fuzzy

# def timeout_msg(out):
#     out = out.encode()
#     #print("Error")
#     sent_out = SlaveSock.sendto(out, Master_addr)
#     print("Sent message: " + out.decode('utf-8'))
#     print('sent %s bytes back to %s\n' % (sent_out, Master_addr))


############### COMUNICACIONES ###################

# Direcciones IP necesarias
ip_emotionalmodel = "127.0.0.3"
ip_master = "127.0.0.1"

class emotional_model(): 

	def __init__(self):
		self.potato_mood = "None"
		self.emotional_model = sockets(ip_emotionalmodel)
		self.emotional_model.bind()
		self.emotional_model.connect(ip_master)
		self.Fuzzy1=Fuzzy()

	def continuous_code_execution(self):
		### CODIGO PARA PRUEBAS Y PLOT ### 
		msg_rec="None"    
		i=0
		inicio = time.time()
		
			
		self.Fuzzy1 = do_Fuzzy(self.Fuzzy1)
		self.potato_mood = self.Fuzzy1.mood
		heartbeat_speed = format(self.Fuzzy1.Alerta_Latido.output['vLatido'])
		tail_speed = format(self.Fuzzy1.Animica_ColaVel.output['ColaVel'])

		# Envíamos la emoción de POTATO
		response_data = {
			"ip_origin": ip_emotionalmodel,
			"ip_destination": ip_master,
			"id_message": "send POTATO emotion",
			"message": self.potato_mood,
			"type_msg": str(type(self.potato_mood))
		}

			
		self.emotional_model.send(response_data)
		print("Sent message: " + self.potato_mood)

		response_data = {
			"ip_origin": ip_emotionalmodel,
			"ip_destination": ip_master,
			"id_message": "send heartbeat",
			"message": heartbeat_speed,
			"type_msg": str(type(heartbeat_speed))
		}
		self.emotional_model.send(response_data)
		print("Sent message: " + heartbeat_speed)

		response_data = {
			"ip_origin": ip_emotionalmodel,
			"ip_destination": ip_master,
			"id_message": "send tail speed",
			"message": tail_speed,
			"type_msg": str(type(tail_speed))
		}
				
		self.emotional_model.send(response_data)
		print("Sent message: " + tail_speed)

				
		
	def handle_msg(self):
		# Recibimos el interés del Dialog Manager
		data = self.emotional_model.receive()
		if(data["id_message"] != "send POTATO emotion"):
			id_message = data["id_message"]
			message = data["message"]


			if id_message == "send interest":
				self.Fuzzy1.interes_frase = message  
				print("Received message: " + str(self.Fuzzy1.interes_frase))  
			
			elif id_message == "send caress":
				self.Fuzzy1.caricia = message  
				print("Received message: " + str(self.Fuzzy1.caricia))  
			
			elif id_message == "send light":
				self.Fuzzy1.luz = message
				print("Received message: " + str(self.Fuzzy1.luz)) 
			
			elif id_message == "send glucose":
				self.Fuzzy1.glucosa = message
				print("Received message: " +str(self.Fuzzy1.glucosa))
	
	def threads(self):
		while(True):
			self.continuous_code_execution()
			self.handle_msg()

emotions = emotional_model()
emotions.threads()





	# timeout=10
	# while msg_rec != "fin":
	#     try:
	#         t = Timer(timeout, timeout_msg, args=['Se ha agotado el tiempo de espera'])
	#         t.start()
	#         buff, caddr = clientSock.recvfrom(BUFFER_SIZE)
	#         msg_rec = buff.decode()
	#         t.cancel()
	#         print ("\nReceived message: " + msg_rec)
	#         if msg_rec!="fin":
	#                 habla, luz, glucosa = map(int, msg_rec.split(','))
	#                 """print(habla)
	#                 print(luz)
	#                 print(glucosa)"""
	#                 Fuzzy1=do_Fuzzy(Fuzzy1)
	#                 msg_send = Fuzzy1.mood
	#                 print("Sent message: " + msg_send)
	#                 buff = msg_send.encode()
	#                 csent = clientSock.sendto(buff, caddr)
	#                 #Añadir un timeout para que esté mandando datos constantemente
	#                 timeout=0.5
	#         else:
	#             t.cancel()
	#             buff = "fin".encode()
	#             clientSock.sendall(buff)
	#             clientSock.close()
	#             #msg_rec = "fin"
	#             #print("socket eliminado")

	#         #clientSock.close()
	#     except:
	#         print("ERROR: el Servidor no está disponible")
	#         clientSock.close()
	#         sys.exit(1)
		
		
	
	#########PLOTS#############
		
"""Fuzzy1.al_an_eg[0].pop()#comentar si no se quiere plot
	Fuzzy1.al_an_eg[1].pop()#comentar si no se quiere plot
	Fuzzy1.al_an_eg[2].pop()#comentar si no se quiere plot
	Fuzzy1.an_in_col[0].pop()#comentar si no se quiere plot
	Fuzzy1.an_in_col[1].pop()#comentar si no se quiere plot
	Fuzzy1.an_in_col[2].pop()#comentar si no se quiere plot
	plt.plot(Fuzzy1.al_an_eg[0],'r--',Fuzzy1.al_an_eg[1],'bs',Fuzzy1.al_an_eg[2],'g') #comentar si no se quiere plot
	plt.show()#comentar si no se quiere plot
	plt.plot(Fuzzy1.alerta_ret[0],'r--',Fuzzy1.alerta_ret[1],'g') #comentar si no se quiere plot
	plt.show()
	plt.plot(Fuzzy1.animica_ret[0],'r--',Fuzzy1.animica_ret[1],'g') #comentar si no se quiere plot
	plt.show()
	plt.plot(Fuzzy1.interes_ret[0],'r--',Fuzzy1.interes_ret[1],'g') #comentar si no se quiere plot
	plt.show()
	plt.plot(Fuzzy1.an_in_col[0],'r',Fuzzy1.an_in_col[1],'g',Fuzzy1.an_in_col[2],'b') #comentar si no se quiere plot
	plt.show()#comentar si no se quiere plot"""