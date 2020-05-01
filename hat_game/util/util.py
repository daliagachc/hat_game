# project name: hat_game
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
# %%
import numpy as np
import functools
from typing import List, Dict
import os
import sqlite3
# Team,Gui,DB, Player = None,None,None,None
import hat_game.util.logger as log
import pandas as pd
import hat_game.util.timer as timer
import jupyter_client
import json
import jupytext
import os
import nbformat.notebooknode as nb
from ipywidgets import AppLayout, Button, Layout

# %%

log.ger.setLevel(log.log.DEBUG)
log.ger.debug('import hat game util')

import hat_game.util.templates as tmp

# noinspection PyProtectedMember
TEMPLATE_PATH = tmp.__path__._path[0]


class Player(object):
    name: str

    def get_player_name(self):
        pass


class Team(object):
    players: List[Player]
    name: str


def create_expanded_button(description, button_style):
    return Button(description=description, button_style=button_style,
                  layout=Layout(height='auto', width='auto'))


class Gui(object):
    layout: AppLayout
    game = None

    def __init__(self, *, game):
        self.game: Game = game
        # from IPython import kernel

        pass

    def create_layout(self):
        # timer.display_timer(5)
        header_button = create_expanded_button('Header', 'success')
        left_button = create_expanded_button('Left', 'info')
        center_button = create_expanded_button('Center', 'warning')
        right_button = create_expanded_button('Right', 'info')
        footer_button = create_expanded_button('Footer', 'success')

        layout = AppLayout(
            # header=header_button,
            header=timer.get_timer_button(
                self.game.timer_secs
            ),
            left_sidebar=None,
            center=center_button,
            right_sidebar=None,
            footer=footer_button
        )
        self.layout = layout
        return layout


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
    tb_kernels = 'kernels'

    def __init__(self, game):
        game: Game
        self.game = game
        self.db_path = os.path.join(game.DB_FOLDER,
                                    game.game_name + '.sqlite')

    def add_players(self, player_team_dic:Dict[str,str]):
        for p,t in player_team_dic.items():
            self.add_player(player=p,team=t)
    def add_teams(self, player_team_dic:Dict[str,str]):
        teams = np.unique(
            list(player_team_dic.values())
        )
        for team in teams:
            self.add_team(team=team)


    def create_db_folder(self):
        os.makedirs(self.game.DB_FOLDER, exist_ok=True)

    def check_db_exists(self) -> bool:
        return os.path.isfile(self.db_path)

    def remove_db(self):
        if self.check_db_exists():
            os.remove(self.db_path)

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

        sql = [s1, s2]

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
    def create_kernels_tb(self):
        s1 = f'''
                create table {self.tb_kernels}
        (
            player varchar
                constraint kernels_pk
                    primary key,
            control_port INTEGER,
            hb_port INTEGER,
            iopub_port INTEGER,
            ip TEXT,
            kernel_name TEXT,
            key TEXT,
            shell_port INTEGER,
            signature_scheme TEXT,
            stdin_port INTEGER,
            transport TEXT
        )
        '''

        sql = [s1]

        for s in sql:
            self.conn.execute(s)

    @conn_decorator
    def add_kernel(self):
        _d = self.game.kernel_dic
        sql0 = f'''
        delete from {self.tb_kernels} 
        where player='{self.game.player_name}'
        '''

        sql1 = f'''
        insert into {self.tb_kernels}
        (
        player,
        control_port,
        hb_port,
        iopub_port,
        ip,
        kernel_name,
        key,
        shell_port,
        signature_scheme,
        stdin_port,
        transport
        )
        values
        (
        '{self.game.player_name}',
        {_d["control_port"]},
        {_d["hb_port"]},
        {_d["iopub_port"]},
        '{_d["ip"]}',
        '{_d["kernel_name"]}',
        '{_d["key"]}',
        {_d["shell_port"]},
        '{_d["signature_scheme"]}',
        {_d["stdin_port"]},
        '{_d["transport"]}'
        )
        '''
        # print(sql1)
        for sql in [sql0, sql1]:
            self.conn.execute(sql)

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
        return self.get_tb_df(self.tb_words, index_col='word_id')

    def get_rounds_df(self):
        return self.get_tb_df(self.tb_rounds, index_col='move')

    def get_kernels_df(self):
        df = self.get_tb_df(self.tb_kernels, index_col='player')

        def _get_kernel(r):
            kernel_dic = json.loads(r.to_json())
            km = jupyter_client.AsyncKernelClient()
            km.load_connection_info(kernel_dic)
            return km

        df['kernel'] = df.apply(_get_kernel, axis=1)
        return df[['kernel']]

    def execute_command_in_all_kernels(self, cmd: str):
        df = self.get_kernels_df()
        for l, row in df.iterrows():
            km = row['kernel']
            km: jupyter_client.asynchronous.client.AsyncKernelClient
            km.execute(cmd, silent=True)

    def execute_command_in_specific_kernels(self, cmd: str,
                                            players: List[str] = None):
        if players is None:
            players = []

        df = self.get_kernels_df().loc[players]
        for l, row in df.iterrows():
            km = row['kernel']
            km: jupyter_client.asynchronous.client.AsyncKernelClient
            km.execute(cmd, silent=True)

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
    def add_team(self, team:str):
        sql = f'''
        insert into {self.tb_teams} 
        (team)
        values ('{team}')
        '''
        log.ger.debug(sql)
        self.conn.execute(sql)


class Game(object):
    gui: Gui
    game_name: str
    password: str
    database: DB
    a = 2
    GAME_FOLDER: str
    DB_FOLDER: str
    PLAYERS_FOLDER: str
    admin_mode: bool
    player_name: str
    kernel_dic: dict
    drop_db_if_exist: bool
    timer_secs = 5
    create_tables: bool
    player_team_dic: Dict[str,str]

    def __init__(self, game_name,
                 password=None,
                 player_name=None,
                 player_team_dic=None,
                 admin_mode=False,
                 # db_folder=None,
                 drop_db_if_exist=False,
                 create_tables=True,
                 root_game_folder=None,
                 ran_from_cli=False
                 ):

        self.run_from_cli = ran_from_cli
        self.game_name = game_name
        self.password = password
        if player_team_dic is None:
            player_team_dic = {}
        self.player_team_dic = player_team_dic
        self.admin_mode = admin_mode
        self.drop_db_if_exist = drop_db_if_exist
        self.create_tables = create_tables

        if root_game_folder is None:
            import hat_game
            app_path = hat_game.__path__[0]
            self.GAME_FOLDER = os.path.join(
                app_path, 'game_test', game_name)
        else:
            self.GAME_FOLDER = os.path.join(
                root_game_folder, self.game_name)

        os.makedirs(self.GAME_FOLDER, exist_ok=True)

        self.DB_FOLDER = os.path.join(self.GAME_FOLDER, 'db_folder')
        self.PLAYERS_FOLDER = os.path.join(self.GAME_FOLDER, 'players')

        self.player_name = player_name

        if self.run_from_cli is False:
            self.database = DB(game=self)
            self.gui = Gui(game=self)
        else:
            self.generate_admin_nb()

        if self.admin_mode:
            self.do_admin_stuff()

        else:
            try:
                self.get_add_kernel_dic()
            except RuntimeError:
                log.ger.warning('cant find kernel')

        pass

    @staticmethod
    def copy_nb_from_template(path_source,
                              name_source,
                              path_target,
                              name_target,
                              dic_replace: dict,
                              ):
        path_in = os.path.join(path_source, name_source)
        path_out = os.path.join(path_target, name_target)
        nb_in = jupytext.read(path_in)
        st_in = json.dumps(nb_in)
        # %%
        st_out: str = st_in
        for l, v in dic_replace.items():
            st_out = st_out.replace(l, v)

        new_out = json.loads(st_out)
        new_out = nb.from_dict(new_out)
        # %%
        jupytext.write(new_out, path_out)

    def remove_game(self):
        # os.rmdir(self.GAME_FOLDER)
        pass

    def generate_admin_nb(self):
        self.copy_nb_from_template(
            path_source=TEMPLATE_PATH,
            name_source='admin_template.ipynb',
            path_target=self.GAME_FOLDER,
            name_target='admin.ipynb',
            dic_replace={'GAME_NAME':self.game_name}
        )

    def generate_player_nb(self,player_name:str):
        self.copy_nb_from_template(
            path_source=TEMPLATE_PATH,
            name_source='player_template.ipynb',
            path_target=self.GAME_FOLDER,
            name_target=f'{player_name}.ipynb',
            dic_replace={
                'GAME_NAME':self.game_name,
                'PLAYER':player_name
            }
        )
    def do_admin_stuff(self):
        # os.makedirs(self.GAME_FOLDER, exist_ok=True)
        os.makedirs(self.DB_FOLDER, exist_ok=True)
        os.makedirs(self.PLAYERS_FOLDER, exist_ok=True)

        if self.run_from_cli is False:
            if self.drop_db_if_exist:
                self.database.remove_db()
            if self.create_tables:
                self.database.create_db_folder()
                self.database.create_kernels_tb()
                self.database.create_rounds_tb()
                self.database.create_words_tb()
                self.database.create_player_team_tb()
                self.database.create_teams_tb()

                self.database.add_teams(self.player_team_dic)
                self.database.add_players(self.player_team_dic)

    def get_add_kernel_dic(self):
        from ipykernel.connect import get_connection_info
        self.kernel_dic = get_connection_info(unpack=True)
        self.kernel_dic['key'] = self.kernel_dic['key'].decode()
        self.database.add_kernel()

    def add_team(self, team_name):
        teams = self.database.get_teams_df().values
        if team_name in teams:
            raise NameError('name already used')
        else:
            self.database.add_team(team=team_name)
        pass

# %%
if __name__ == '__main__':
    import sys

    Game(
        game_name=sys.argv[2],
        ran_from_cli=True,
        admin_mode=True,
        root_game_folder= sys.argv[1]
    )
