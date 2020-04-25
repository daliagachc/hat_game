# project name: hat_game
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# %%

from typing import List, Dict
Team,Gui,DB, Player = None,None,None,None

class Player(object):
    pass

class Team(object):
    players: List[Player]
    name: str

class Gui(object):
    name:str
    pass



class Game(object):
    team: Dict[str,Team]
    gui: Gui
    name: str
    password: str
    database: DB






g = Game()
g.gui.
