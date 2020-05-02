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
g.execute_command_in_all_kernels(
    'g.gui.show_words()'
)

# %%

# %%
g.execute_command_in_all_kernels(
    'g.gui.start_count_down()'
)

# %%
g.db.add_update_config_val('timer_on','0','int')

# %%
g.db.add_update_config_val('current_player','sara','str')
g.db.add_update_config_val('current_round','1','int')

# %%
g.db.add_update_config_val('timer_on','0','int')

# %%
g.db.get_config_dic()

# %%
import hat_game.util.util as util

# %%
b = util.TimerButton(game=g)

# %%
b

# %%
b.count_down(5)

# %%
b.threaded_count_down(5)

# %%

# %%
