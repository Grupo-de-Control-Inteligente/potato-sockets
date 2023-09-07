#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import re
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
from textblob import TextBlob
import signal
#from potatolcm import estado_gen
#from potatolcm import habla_usuario_t
#from potatolcm import habla_potato_t

# Create templates
user_template = "USER >"
mood_template  = "MOOD > {0}"
bot_template  = "BOT  > {0}"

# Define user's variables
mood = "normal"
user_input = []
user_name = "desconocido"
user_city = "desconocido"
user_country = "desconocido"
global user_data
user_data = []

#msg_potato = habla_potato_t()


def signal_handler(signum, frame):
    raise Exception("Timeout")

# Define current date and time
def current_date_time():
    now = datetime.datetime.now()
    day = '{:01d}'.format(now.day)
    day_name = now.strftime("%A").capitalize()
    print(day_name)
    day_name = get_day_es(day_name)
    month = '{:02d}'.format(now.month)
    month_name = now.strftime("%B").capitalize()
    year = '{:02d}'.format(now.year)
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    second = '{:02d}'.format(now.second)
    return day, day_name, month, month_name, year, hour, minute, second

def get_day_es(day_name):
    if day_name == "Monday": day_name = 'lunes'
    elif day_name == "Tuesday": day_name = 'martes'
    elif day_name == "Wednesday": day_name = 'miercoles'
    elif day_name == "Thursday": day_name = 'jueves'
    elif day_name == "Friday": day_name = 'viernes'
    elif day_name == "Saturday": day_name = 'sabado'
    else: day_name = "domingo"
    return day_name

def get_season():
    day = datetime.date.today().timetuple().tm_yday # get the current day of the year
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else
    if day in spring: season = 'primavera'
    elif day in summer: season = 'verano'
    elif day in fall: season = 'otono'
    else: season = 'invierno'
    return season

def set_response(variable,value):
    if variable == "user_name":
        global user_name
        user_name = value
    elif variable == "user_city":
        global user_city
        user_city = value
    elif variable == "user_country":
        global user_country
        user_country = value

def get_response(variable):
    if variable == "day":
        value, _, _, _, _, _, _, _ = current_date_time()
    elif variable == "day_name":
        _, value, _, _, _, _, _, _ = current_date_time()
    elif variable == "month":
        _, _, value, _, _, _, _, _ = current_date_time()
    elif variable == "month_name":
        _, _, _, value, _, _, _, _ = current_date_time()
    elif variable == "season":
        value = get_season()
    elif variable == "year":
        _, _, _, _, value, _, _, _ = current_date_time()
    elif variable == "hour":
        _, _, _, _, _, value, _, _ = current_date_time()
    elif variable == "minute":
        _, _, _, _, _, _, value, _ = current_date_time()
    elif variable == "second":
        _, _, _, _, _, _, _, value = current_date_time()
    elif variable == "user_name":
        value = user_name.capitalize()
    elif variable == "user_city":
        value = user_city.capitalize()
    elif variable == "user_country":
        value = user_country.capitalize()
    elif variable == "bot_mood":
        value = mood
    return value

class RuleBasedModel(object):

    def __init__(self, pairs_es, pairs_en, reflections_es={}, reflections_en={}):
        self._pairs_es = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs_es]
        self._pairs_en = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs_en]
        self._reflections_es = reflections_es
        self._reflections_en = reflections_en
        self._regex_es = self._compile_reflections_es()
        self._regex_en = self._compile_reflections_en()
    
    def _compile_reflections_es(self):
        sorted_refl_es = sorted(self._reflections_es.keys(), key=len, reverse=True)
        return re.compile(r"\b({0})\b".format("|".join(map(re.escape, sorted_refl_es))), re.IGNORECASE)
    def _compile_reflections_en(self):
        sorted_refl_en = sorted(self._reflections_en.keys(), key=len, reverse=True)
        return re.compile(r"\b({0})\b".format("|".join(map(re.escape, sorted_refl_en))), re.IGNORECASE)

    def _language(self, message):
        global language
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(1)
        try: language = TextBlob(message).detect_language()
        except: language = "es"
        finally:
            signal.alarm(0)
            if language == "en": pairs = self._pairs_en
            else: pairs = self._pairs_es
            return pairs

    def _conditional(self,response_list):
        conditional_resp,regular_resp = [],[]
        for response in response_list:
            if response.startswith('*'):
                pos_ini = response.find("<")
                pos_end = response.find(">")
                pos_cond = pos_end + 2
                pos_assign = response.find("=>")
                variable = self._setter_getter(response[pos_ini : pos_end + 1]).lower()
                value = response[pos_cond + 3 : pos_assign - 1]
                if response[pos_cond : pos_cond + 2] == "!=":
                    if variable != value:
                        conditional_resp.append(response[pos_assign + 3:])
                elif response[pos_cond : pos_cond + 2] == "==":
                    if variable == value:
                        conditional_resp.append(response[pos_assign + 3:])
            else:
                regular_resp.append(response)
        # pick a random response
        if conditional_resp:
            resp = random.choice(conditional_resp)
        else:
            resp = random.choice(regular_resp)
        return resp

    def _chatbot_mood(self,response):
        global mood
        if   mood == "normal"    : bot_mood = "\033[0;32;m:) \033[0;30;m" # green
        elif mood == "sad"       : bot_mood = "\033[0;34;m:( \033[0;30;m" # blue
        elif mood == "alegrecal" : bot_mood = "\033[0;35;m;) \033[0;30;m" # purple
        elif mood == "alegre"    : bot_mood = "\033[0;33;m:p \033[0;30;m" # yellow
        elif mood == "miedo"     : bot_mood = "\033[0;37;m:s \033[0;30;m" # gray
        elif mood == "angry"     : bot_mood = "\033[0;31;mx( \033[0;30;m" # red
        else                     : bot_mood = ""
        response = (bot_mood + response)
        return response

    def _wildcards(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute_reflections(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find('%')
        return response

    def _substitute_reflections(self, message):
        if language is "en":
            reflections = self._regex_en.sub(lambda mo: self._reflections_en[mo.string[mo.start(): mo.end()]], message.lower())
        else:
            reflections = self._regex_es.sub(lambda mo: self._reflections_es[mo.string[mo.start(): mo.end()]], message.lower())
        return reflections

    def _setter_getter(self, response):
        pos_ini = response.find("<")
        pos_end = response.find(">")
        while pos_ini >= 0:
            action = response[pos_ini + 1 : pos_ini + 4]
            if action == "set":
                pos_assign = response.find("=")
                variable = response[pos_ini + 5 : pos_assign]
                value = response[pos_assign + 1: pos_end]
                set_response(variable, value) # set the variable in the value
                response = (response[:pos_ini] + "" + response[pos_end + 2:])
            elif action == "get":
                variable = response[pos_ini + 5 : pos_end]
                value = get_response(variable) # pick the variable
                response = (response[:pos_ini] + "{}" + response[pos_end + 1 :]).format(value)
            pos_ini = response.find("<")
            pos_end = response.find(">")
        return response

    def _respond(self, message):
        pairs = self._language(message) # detect language
        for (pattern, response) in pairs: # check each pattern
            match = pattern.match(message)
            if match: # did the pattern match?
                resp = self._conditional(response)   # conditional response
                # resp = self._chatbot_mood(resp)      # chatbot emoji moode 
                resp = self._wildcards(resp, match)  # process wildcards
                resp = self._setter_getter(resp)     # set and get external class variables such as names, cities, time, ...

                # fix munged punctuation at the end
                if resp[-2:] == '..': resp = resp[:-2] + '.'
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                if resp[-2:] == '.?': resp = resp[:-2] + '?'
                return resp
