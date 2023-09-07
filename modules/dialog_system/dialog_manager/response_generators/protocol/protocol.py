#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import time
import threading
import os
import signal

class TenSec(threading.Thread):
    def restart(self):
        self.my_timer = time.time() + 10 
    def run(self, *args):
        self.restart()
        while 1:
            time.sleep(0.1)
            if time.time() >= self.my_timer:
                break
        os.kill(os.getpid(), signal.SIGINT)
        
class OneMin(threading.Thread):
    def restart(self):
        self.my_timer = time.time() + 60
    def run(self, *args):
        self.restart()
        while 1:
            time.sleep(0.1)
            if time.time() >= self.my_timer:
                break
        os.kill(os.getpid(), signal.SIGINT)

class glucose_protocol():
    def do_protocol(self):
        print("No te pongas nervioso, estás teniendo una bajada de glucosa ¿Te encuentras bien?")
        r=self.espera(10)
        i=0
        while r is None and i<2:
            r=self.espera(10)
            i=i+1
        if r is None:
            print("Esperando último minuto")
            r=self.espera(60)
        if r is None:
            print("AVISAR A EMERGENCIAS")
        elif r == "Sí" or r=="Si" or r=="si" or r=="sí":
            self.primeraMedida()
        elif r == "No" or r == "no":
            print ("¿Tienes síntomas como mareo, malestar, niebla mental, dolor de cabeza, sudores, debilitamiento, hormigueo o temblores?")
            try:
                res = input('::> ')
            except KeyboardInterrupt:
                res = input('::> ')
            if res=="Sí" or res=="Si" or res=="si" or res=="sí":
                print ("¿Puedes hacerte cargo de la situación?")
                res = input('::> ')
                if res=="Sí" or res=="Si" or res=="si" or res=="sí":
                    self.primeraMedida()
                if res=="No" or res=="no":
                    print ("Toma, por favor, entre 20 y 25 gramos de azúcar lo antes posible, ¿Puedes?")
                    try:
                        res = input('::> ')
                    except KeyboardInterrupt:
                        res = input('::> ')
                    if res == "No" or res=="no":
                        print ("AVISAR A EMERGENCIAS")
            if res=="No":
                self.primeraMedida()
    def espera(self,seg):
        if seg == 10: 
            try:
                t = TenSec()
                t.daemon = True
                t.start()
                x = input('::> ')
                t.restart()
                return x
            except KeyboardInterrupt:
                print("\n¡Por favor, responde!")
                t.join()

        elif seg == 60: 
            try:
                t = OneMin()
                t.daemon = True
                t.start()
                x = input('::> ')
                t.restart()
                return x
            except KeyboardInterrupt:
                print("\n¡Por favor, responde!")
                t.join()


    def primeraMedida(self):
        print("Indícame tu nivel de glucosa, por favor.")
        try:
            res = int(input('::> '))
        except KeyboardInterrupt:
            res = int(input('::> '))
        if res>65 and res<=70:
            print("Toma una fruta, un vaso de leche algún alimento que tenga hidratos de carbono de absorción rápida.")
        if res>45 and res<=65:
            print("Toma entre 10 y 20 gramos de azúcar diluido en agua.")
        if res<=45:
            print("Toma entre 10 y 20 gramos de azúcar diluido en agua. ¿Puedes avisar a un familiar?")
            try:
                res2 = input('::> ')
            except KeyboardInterrupt:
                res2 = input('::> ')
            if res2 == "No" or res2 == "no":
                print("AVISAR A EMERGENCIAS")
                return
        self.segundaMedida(res)
    def segundaMedida(self,res):
        print("Espera cinco minutos y vuelve a indicarme tu nivel de glucosa.")
        try: 
            res2 = int(input('::> '))
        except KeyboardInterrupt:
            res2 = int(input('::> '))
        if res2>=70:
            print("Enhorabuena, ya no hay nada de lo que preocuparse.")
        if res2<70 and res2>res:
            self.segundaMedida(res2) 
        if res2<45:
            print("Procede según la primera medición, por favor.")




