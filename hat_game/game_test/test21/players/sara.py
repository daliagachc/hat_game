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
g = Game(game_name='test21', password='PASS', player_name='sara',root_game_folder='../../')
g.gui.create_layout()


# %%
g.gui.timer_button.stop = True

# %%
st =pprint.pformat(g.db.get_config_df()['value'])

# %%
g.gui.center_button.description='''
z \n
sd
sd'''

# %%
st

# %%
