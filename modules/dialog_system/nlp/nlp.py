#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import pickle
import time
import os
import yaml
from torch import package
from googletrans import Translator
import pathlib
path = os.path.abspath(__file__)


class NLP:
    def __init__(self,msg_in):
        
        self.classifier , self.vectorizer = pickle.load(open(os.path.join((os.path.dirname(os.path.dirname(path))), 'models/sentence_type_classifier/utter_type_classifier.pkl'), 'rb'))#pickle.load(open('/Users/laura/Completo_V4/sp_qcorr_model.pkl', 'rb'))
        self.msg_in = msg_in
        self.msg_out = ""
        self.msg_out_eng = ""
        self.sentence_t = ""
        with open (os.path.join((os.path.dirname(os.path.dirname(path))), 'models/puntuation/silero_models.yml'), 'r', encoding="utf8") as yaml_file:
            models = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        model_conf = models.get('te_models').get('latest')
        model_url = model_conf.get('package')
        model_dir = os.path.join((os.path.dirname(os.path.dirname(path))), 'models/sentence_type_classifier/')
        #if not os.path.exists(model_dir):
            #os.makedirs(model_dir)
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, os.path.basename(model_url))
        imp = package.PackageImporter(model_path)
        self.model = imp.load_pickle("te_model", "model")
        self.translator = Translator()
    
    def apply_te(self,text, lan='en'):
        return self.model.enhance_text(text, lan)

    def do_punctuation(self):
        #de es a eng
        i = self.msg_in
        trans = self.translator.translate(i, dest='en')
        trans_t = trans.text.replace('?', '')
        #puntuación inglés
        input_text = trans_t
        output_text = self.apply_te(input_text, lan='en')
        #de eng a es
        self.msg_out_eng = output_text
        trans = self.translator.translate(output_text, dest='es')
        self.msg_out = trans.text 
    
    def sentence_type(self):
        self.sentence_t = self.classifier.predict(self.vectorizer.transform([self.msg_out]))[0]
    
    def correct(self):
        self.do_punctuation()
        self.sentence_type()