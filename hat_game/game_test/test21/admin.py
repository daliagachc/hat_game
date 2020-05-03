# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2


# %%
from hat_game.util.util import Game


# %%
player_team_dic = {
    'diego':'a',
    'sara':'b'
}

# %%
g = Game(
    game_name='test21', 
    password='PASS', 
    timer_secs = 5,
    number_of_words = 2,
    number_of_rounds = 4,
    admin_mode = True,
    root_game_folder='../',
    player_team_dic = player_team_dic,
    drop_db_if_exist=True,
)


# %%
g.all_show_words()

# %%
g.all_set_center_banner()

# %%
g.db.add_update_config_val('timer_on','0','int')

# %%
g.db.add_update_config_val('current_player','sara','str')
g.db.add_update_config_val('current_round','3','int')
g.db.add_update_config_val('timer_secs','30','int')
g.activate_current_player()
# g.db.add_update_config_val('timer_on','0','int')
# g.db.add_update_config_val('number_of_words','10','int')

# %%

# %%
g.db.get_config_dic()

# %%
g.all_set_center_banner()

# %%
g.db._close_conn()

# %%
g.db._connect()

# %%
