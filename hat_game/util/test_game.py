# project name: hat_game
# created by diego aliaga daliaga_at_chacaltaya.edu.bo
from unittest import TestCase
import hat_game.util.util as util
import hat_game.util.logger as log
import os

log.ger.debug('start test')


def create_basic_game():
    g = util.Game(
        game_name='test',
        password='pass',
        admin_mode=True,
        drop_db_if_exist=True
    )
    # g.add_team('test_team')
    return g

def remove_test_db():
    import shutil
    shutil.rmtree(
        '/Users/diego/hat_game/hat_game/game_test/test')



class TestGame(TestCase):
    def setUp(self) -> None:
        self.g = create_basic_game()

    def test_create_team(self):
        self.assertIsInstance(self.g, util.Game)

    def test_add_team(self):
        self.g.add_team('a')
        self.assertIn('a', self.g.db.get_teams_df().values)

    def test_add_dup_team_fails(self):
        self.g.add_team('test_team')
        self.assertRaises(
            NameError,
            self.g.add_team, 'test_team'
        )

    def tearDown(self) -> None:
        remove_test_db()


    # def test_print_teams(self):
    #     print(self.g.teams)


def create_test_game_db():
    g = create_basic_game()
    db = util.DB(g)
    db.create_db_folder()
    return g, db


class TestDB(TestCase):
    def setUp(self) -> None:
        self.g, self.db = create_test_game_db()

        pass

    def test_close_before_def(self):
        # g = create_basic_game()
        # db = util.DB(g)
        g,db = self.g, self.db
        db._close_conn()
        self.assertTrue(True)

    def test_conn(self):
        # g, db = create_test_game_db()
        g,db = self.g, self.db
        db._connect()
        self.assertTrue(True)

    def test_conn_decorator(self):
        # g, db = create_test_game_db()
        g,db = self.g, self.db
        log.ger.debug('conn created: %s', db.check_conn_created())
        self.assertTrue(True)


    def test_get_tb_list(self):
        # g, db = create_test_game_db()
        g,db = self.g, self.db
        table_list = db.get_table_list()
        print(table_list)
        # self.assertListEqual([], table_list)

    def test_create_player_team_table(self):
        # self.db.create_teams_tb()
        self.db.add_team('A')
        self.db.add_team('B')
        df = self.db.get_teams_df()
        print(df)
        # self.db.create_player_team_tb()
        self.db.add_player('diego','A')
        self.db.add_player('yara','A')
        self.db.add_player('sara','B')
        self.db.add_player('ingrid','B')
        df = self.db.get_player_team_df()
        print(df)
        # self.db.create_words_tb()
        self.db.add_word('bla','diego')
        self.db.add_word('blo','diego')
        self.db.add_word('ble','yara')
        self.db.add_word('bli','yara')
        self.db.add_word('bao','sara')
        self.db.add_word('beo','sara')
        self.db.add_word('boo','ingrid')
        self.db.add_word('buo','ingrid')
        df = self.db.get_words_df()
        print(df)

        # self.db.create_rounds_tb()
        df = self.db.get_rounds_df()
        print(df)
        self.assertTrue(True)

    def tearDown(self) -> None:
        remove_test_db()
