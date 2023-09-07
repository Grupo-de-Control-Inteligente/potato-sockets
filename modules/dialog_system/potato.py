import os
import sys

# Agregar la ruta de la carpeta raíz del proyecto al path de Python
path = sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print (path)
from dialog_manager.dialog_manager import DialogManager

DS = DialogManager()

def Potato_chat():
    DS.converse()

def demo():
    Potato_chat()
    
if __name__ == "__main__":
    demo()