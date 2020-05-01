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
    admin_mode = True,
    root_game_folder='../',
    player_team_dic = player_team_dic,
#     drop_db_if_exist=True,
)


# %%
g.generate_all_players_nb()

# %%
