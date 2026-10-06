import ctypes
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

from source.modules.engine import engine
from source.modules.maker.editor import editor

if __name__ == "__main__":
    # splash 

    # editor 
    editor.run()

    # Executa o motor de jogo    
    #engine.run()