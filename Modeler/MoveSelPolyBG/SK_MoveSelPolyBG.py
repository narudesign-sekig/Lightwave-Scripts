#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
SK_MoveSelPolyBG

Move the selected polygon to the background layer
"""

import lwsdk

__author__      = "Makoto Sekiguchi"
__date__        = "Dec 15 2018"
__copyright__   = "Copyright (C) 2018 naru design"
__version__     = "0.90"
__maintainer__  = "Makoto Sekiguchi"
__status__      = "Develop"
__lwver__       = "11"


class MoveSelPolyBG(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(MoveSelPolyBG, self).__init__()

    """
    show erro dialog
    args:
        msg1 : 1st line
        msg2 : 2nd line
    """
    def show_error_dialog(self, msg1, msg2):
        message_funcs = lwsdk.LWMessageFuncs()
        message_funcs.error(msg1, msg2)

    """
    select layer
    args:
        cs          : "SETALAYER" or "SETBLAYER"
        layers      : target (str)
    """
    def set_layers(self, mod, cs, layers):
        cs_options = lwsdk.marshall_dynavalues(layers)
        cs_setlayer = mod.lookup(mod.data, cs)
        mod.execute(mod.data, cs_setlayer, cs_options, lwsdk.OPSEL_USER)

    """
    swap select layer
    """
    def swap_layers(self, mod, fg_layers, bg_layers):
        self.set_layers(mod, 'SETALAYER', fg_layers)
        self.set_layers(mod, 'SETBLAYER', bg_layers)

    def process(self, mod):
        state_query = lwsdk.LWStateQueryFuncs()

        selected_fg_layers_str = state_query.layerList(lwsdk.OPLYR_FG, None)
        selected_bg_layers_str = state_query.layerList(lwsdk.OPLYR_BG, None)
        selected_bg_layers_str_list = selected_bg_layers_str.split()

        if len(selected_bg_layers_str_list) != 1:
            self.show_error_dialog('Invalid layer selection', 'Select only one bg layer')

        mod.execute(mod.data, mod.lookup(mod.data, 'CUT'), None, lwsdk.OPSEL_USER)
        self.swap_layers(mod, selected_bg_layers_str, selected_fg_layers_str)
        mod.execute(mod.data, mod.lookup(mod.data, 'PASTE'), None, lwsdk.OPSEL_USER)
        self.swap_layers(mod, selected_fg_layers_str, selected_bg_layers_str)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("SK_MoveSelPolyBG", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("SK_MoveSelPolyBG", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SK_MoveSelPolyBG", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory("SK_MoveSelPolyBG", MoveSelPolyBG): ServerTagInfo}
