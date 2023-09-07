from googletrans import Translator
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline, set_seed
import pathlib
import os

# Obtener la ruta absoluta del archivo actual
path = os.path.abspath(__file__)

#"happiness" / "sadness" / "no_emotion"
class GPT2Emotional:
    def __init__(self):
        self.txt_out=""
        self.generator="None"
        self.translator="None"

    def set_gen(self):
        #Descargo el pretrained model de la ruta correspondiente
        MODEL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(path)))), 'models/gpt2_emotional/gpt2-large_shuffled')
        TOKENIZER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(path)))), 'models/gpt2_emotional/tokenizer_gpt2-large')
  
        model = AutoModelForCausalLM.from_pretrained(MODEL)
        tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
        self.generator = pipeline('text-generation', model = model, tokenizer = tokenizer)
        self.translator = Translator()
        #hapiness/sadness/no_emotion
    
    def do_gen(self,user_in, user_mood='no emotion', potato_mood='no emotion'):  
        a=self.generator("<bos><"+user_mood+">"+user_in+"<"+potato_mood+">"+"<sep>", max_length=50, num_return_sequences=1)
        txt=a[0]['generated_text']
        idx=txt.rfind(">")
        txt=txt[idx+1:]
        trans = self.translator.translate(txt, dest='es')
        self.txt_out=trans.text
    