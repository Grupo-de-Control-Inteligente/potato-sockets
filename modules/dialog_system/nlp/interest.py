#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import re

class Interest:
    def __init__(self,sentence):
    
        self.sentence = sentence
        self.words = []
        self.range20=["viajar","lugares","avión"]
        self.range50=["animales"]
        self.range70=["cucarachas","enjambre"]
        self.range100=["diabetes","glucosa","dolor","pinchazo","mareo"]
        self.P=0
    def word_extraction(self): 
        self.sentence = self.sentence.lower()
        ignore = ["me", "es", "si","sí","yo","la","el","los"]    
        words = re.sub("[^\w]", " ",  self.sentence).split()    
        cleaned_text = [w.lower() for w in words if w not in ignore]    
        return cleaned_text
    def tokenize(self):               
        word = self.word_extraction()        
        self.words.extend(word)            
        self.words = sorted(list(set(self.words))) 
    def score(self):
        self.tokenize()
        for word in self.words:
            score=0
            if word in self.range20: 
                score = 20
            elif word in self.range50: 
                score = 50
            elif word in self.range70: 
                score = 70
            elif word in self.range100: 
                score = 100
            if score > self.P:
                self.P = score

        return score