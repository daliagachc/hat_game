# project name: hat_game
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# %%
import functools
from typing import List, Dict
import os
import sqlite3
# Team,Gui,DB, Player = None,None,None,None
import hat_game.util.logger as log
import pandas as pd

# %%

log.ger.setLevel(log.log.DEBUG)
log.ger.debug('import hat game util')


class Player(object):
    name: str
    def get_player_name(self):
        pass


class Team(object):
    players: List[Player]
    name: str


class Gui(object):
    name: str
    pass


def conn_decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(self, *args, **kwargs):
        self: DB
        self._connect()
        value = func(self, *args, **kwargs)
        self.conn.commit()
        self._close_conn()
        return value

    return wrapper_decorator


# noinspection SqlResolve
class DB(object):
    db_path: str
    game = None
    conn: sqlite3.Connection = None
    tb_player_team = 'player_team'
    tb_teams = 'teams'
    tb_words = 'words'
    tb_rounds = 'rounds'

    def __init__(self, game):
        game: Game
        self.game = game
        self.db_path = os.path.join(game.DB_FOLDER, game.name)

    def create_db_folder(self):
        os.makedirs(self.game.DB_FOLDER, exist_ok=True)

    def check_db_exists(self) -> bool:
        return os.path.isfile(self.db_path)

    def _connect(self):
        self._close_conn()
        self.conn = sqlite3.connect(self.db_path, timeout=500)

    def _close_conn(self):
        if self.conn is not None:
            self.conn.close()

    @conn_decorator
    def create_player_team_tb(self):
        s1 = f'''
        create table {self.tb_player_team}
        (
            player varchar,
            team varchar
        )'''
        s2 = f'''
            create unique index player_team_player_uindex
                on player_team (player)
            '''

        sql = [s1,s2]

        for s in sql:
            self.conn.execute(s)

    @conn_decorator
    def create_rounds_tb(self):
        s1 = f'''
        create table {self.tb_rounds}
        (
            move    INTEGER not null
                constraint rounds_pk
                    primary key autoincrement,
            round   int,
            team    varchar,
            player  varchar,
            word    varchar,
            word_id int,
            result  varchar
        )'''

        sql = [s1]

        for s in sql:
            self.conn.execute(s)


    @conn_decorator
    def create_teams_tb(self):
        s1 = f'''
        create table {self.tb_teams}
        (team varchar)'''
        s2 = f'''
        create unique index table_name_team_uindex
        on teams (team)'''
        sql = [s1, s2]
        for s in sql:
            self.conn.execute(s)

    @conn_decorator
    def create_words_tb(self):
        s1 = f'''
        create table {self.tb_words}
        (
            word_id INTEGER not null
                constraint table_name_pk
                    primary key autoincrement,
            word    varchar not null,
            player  varchar not null
        )'''
        sql = [s1]
        for s in sql:
            self.conn.execute(s)

    @conn_decorator
    def get_table_list(self):
        sql = """
        select name from sqlite_master where type is 'table'
        """
        df = pd.read_sql(sql, self.conn)
        return list(df.values)

    @conn_decorator
    def check_conn_created(self):
        return os.path.isfile(self.db_path)

    @conn_decorator
    def check_table_exists(self, table) -> bool:
        tables = self.get_table_list()
        return table in tables

    @conn_decorator
    def get_tb_df(self, name, index_col=None):
        df = pd.read_sql(
            f'select * from {name}',
            self.conn,
            index_col=index_col
        )
        return df

    def get_player_team_df(self):
        return self.get_tb_df(self.tb_player_team, index_col='player')

    def get_teams_df(self):
        return self.get_tb_df(self.tb_teams)

    def get_words_df(self):
        return self.get_tb_df(self.tb_words,index_col='word_id')

    def get_rounds_df(self):
        return self.get_tb_df(self.tb_rounds,index_col='move')



    @conn_decorator
    def add_player(self, player, team):
        sql = f'''
        insert into {self.tb_player_team} 
        (player, team)
        values ('{player}','{team}')
        '''
        self.conn.execute(sql)

    @conn_decorator
    def add_word(self, word, player):
        sql = f'''
        insert into {self.tb_words} 
        (word, player)
        values ('{word}','{player}')
        '''
        self.conn.execute(sql)

    @conn_decorator
    def add_team(self, team):
        sql = f'''
        insert into {self.tb_teams} 
        (team)
        values ('{team}')
        '''
        self.conn.execute(sql)



class Game(object):
    teams: Dict[str, Team]
    gui: Gui
    name: str
    password: str
    database: DB
    a = 2
    DB_FOLDER = '/tmp/hate_game_db'
    admin_mode: bool

    def __init__(self, name, password, teams=None, admin_mode=False,
                 db_folder=None
                 ):
        self.name = name
        self.password = password
        if teams is None:
            self.teams = {}
        self.admin_mode = admin_mode
        if db_folder is not None:
            self.DB_FOLDER = db_folder

        pass

    def add_team(self, name, team: Team):
        if name in self.teams.keys():
            raise NameError('name already used')
        else:
            self.teams[name] = team
        pass

# %%

