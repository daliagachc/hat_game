# project name: hat_game
# created by diego aliaga daliaga_at_chacaltaya.edu.bo


import logging as log
import sys

log = log
ger = log.getLogger('hat_game')
handler = log.StreamHandler()
formatter = log.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
ger.addHandler(handler)

# ger_out = log.getLogger('hat_game')
# handler = log.StreamHandler(sys.stdout)
# formatter = log.Formatter(
#     '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# ger_out.addHandler(handler)
