#!/bin/bash

# # These must all be local, or on relative path.
# HE_MODEL="holdem_conv_24_filter_xCards_xNumDraws_x0_9803_double_row_percent_basline_800k.pickle"
# CNN_MODEL="nlh_events_conv_24_filter_xCards_xCommunity_xContext_0.02_CNN_1_74_Slum_Tartanian7_etc_foldper_700k.pickle"
# CNN_OLD_MODEL="nlh_events_conv_24_filter_xCards_xCommunity_xContext_0.02_CNN_1_73_Tartanian7_restart_foldper_700k.pickle"

# # For some reason, this needs to be executed.
export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
python acpc_player.py --address=$1 --port=$2
# Python NLH player
# TODO: Take localhost & port from the command line

#./example_player holdem.nolimit.2p.reverse_blinds.game $1 $2
