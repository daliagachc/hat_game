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
from hat_game.util.util import Game
g = Game(game_name='test', password='pass', player_name='admin',
         drop_db_if_exist=False,
         create_tables=False
         )

# %%
g.database.execute_command_in_all_kernels(
    'g.gui.layout.header.click()')

# %%
g.database.execute_command_in_specific_kernels(
    'a=4',['diego']
    )

# %%
g.database.execute_command_in_specific_kernels(
    'a=2',['sara']
    )

# %%
g.database.get_kernels_df().loc['diego']['kernel']

# %%
