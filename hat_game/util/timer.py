# project name: hat_game
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

import ipywidgets
from IPython.display import display
import time
import threading

def count_down(button:ipywidgets.Button,
               secs:int):
    button.disabled = True
    original_desc = button.description
    s = secs

    button.description = f'{s}'

    while s > 0:
        time.sleep(1)
        s -= 1
        button.description = f'{s}'

    button.description = original_desc
    button.disabled = False




def display_timer(secs):
    button = ipywidgets.Button(description="Start Timer", button_style='info')
    def _fun(b):
        count_down(b,secs)

    def _thread(b):
        _th = threading.Thread(target=_fun,args=(b,))
        _th.start()

    button.on_click(_thread)
    display(button)
    return button
