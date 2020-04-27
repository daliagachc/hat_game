import ipywidgets
import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display

test_df = pd.DataFrame(['Guitar','check','Diego','Sara','bucket','Lost','quarantine'])


class Gui(object):
    points=0
    b_exp= widgets.Button(
        description='I explained it!',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        icon='check'
    )
    b_putback=widgets.Button(
        description='Put back :/',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        icon='check'
    )
    b_nw= widgets.Button(
        description='new word',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        icon='check'
    )
    output1 = widgets.Output()
    output_w = widgets.Output()

    def __init__(self):
        print('Hey! Starting!')
        self.currentWord= None
        self.currentWordWidg=None
        self.current_display_points=None
    def start_game(self):
        self.b_exp.on_click(self.clicked_explained)
        self.b_putback.on_click(self.clicked_putback)
        self.b_nw.on_click(self.clicked_new_word)
        buttons=widgets.HBox([self.b_exp, self.b_putback, self.output1])#, self.b_nw])
        out = widgets.VBox([self.b_nw, self.output_w])
        display(buttons)
        display(out)
        #display(self.b_exp)
        #display(self.b_putback, self.output)
        #display(self.b_nw)

        # display buttons
        return
    def _get_new_word(self,):
        ii= np.random.randint(len(test_df))
        return(test_df.loc[ii,0])

    def display_new_word(self):
        return self.display_word(self._get_new_word())

    def display_word(self, word, description='Word:'):
        w= widgets.HTML(
            value="%s"%word,
            placeholder=description,
            description=description,
        )
        self.currentWordWidg = w
        display(w)
        return w


    def clicked_new_word(self, b):
        if self.currentWordWidg is not None:
            self.currentWordWidg.close()
        with self.output_w:
            w=self.display_new_word()
            self.currentWordWidg= w


    def clicked_explained(self,b):
        #self.currentWordWidg.close()
        self.points = self.points + 1
        if self.current_display_points is not None:
            self.current_display_points.close()
        with self.output1:
            self.current_display_points=self.display_word('Explained! +1, current score:%s'%self.points
                                                          , description='')

        #self.points = self.points+1
        #with self.output1:
        #   print('Explained it ')
    def clicked_putback(self, b):
        self.points = self.points-1
        if self.current_display_points is not None:
            self.current_display_points.close()
        with self.output1:
            self.current_display_points=self.display_word('Put back! -1, current score:%s'%self.points,
                                                          description='')

        #with self.output1:
        #    print('Word put back :/')

class GetWords(object):
    def get_words(self):
        whl = []
        for i in range(4):
            text = widgets.Text(
                value='',
                placeholder='Write word in here',
                description='String:',
                disabled=False
            )
            whl.append(text)
            display(text)
        button = widgets.Button(description="Submit!")
        output = widgets.Output()

        display(button, output)

        def on_button_clicked(b):
            with output:
                for el in whl:
                    print(el.value)
                #print("Button clicked.")

        button.on_click(on_button_clicked)
