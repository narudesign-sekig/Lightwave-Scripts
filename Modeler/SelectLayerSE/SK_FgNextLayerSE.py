#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
SK_FgNextLayerSE

(Foreground) Select next layer, Skip empty layer
"""

import lwsdk

__author__      = "Makoto Sekiguchi"
__date__        = "Dec 12 2018"
__copyright__   = "Copyright (C) 2018 naru design"
__version__     = "0.90"
__maintainer__  = "Makoto Sekiguchi"
__status__      = "Develop"
__lwver__       = "11"


class FgNextLayerSE(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(FgNextLayerSE, self).__init__()

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

    def process(self, mod_command):

        state_query = lwsdk.LWStateQueryFuncs()

        selected_fg_layers_str_list = state_query.layerList(lwsdk.OPLYR_FG, None).split()

        if len(selected_fg_layers_str_list) > 1:
            self.show_error_dialog('Invalid layer selection', 'Select only one fg layer.')
            return lwsdk.AFUNC_OK

        data_layers_str = state_query.layerList(lwsdk.OPLYR_NONEMPTY, None).split()
        data_layers = [int(n) for n in data_layers_str]
        data_layers.sort()

        selected_fg_layer = int(selected_fg_layers_str_list[0])

        selected_bg_layers_str = state_query.layerList(lwsdk.OPLYR_BG, None)
        selected_bg_layers_str_list = selected_bg_layers_str.split()
        selected_bg_layers_int_list = [int(n) for n in selected_bg_layers_str_list]

        for data_layer in data_layers:
            if selected_fg_layer < data_layer and not data_layer in selected_bg_layers_int_list:
                self.set_layers(mod_command, "SETALAYER", str(data_layer))
                self.set_layers(mod_command, "SETBLAYER", selected_bg_layers_str)
                return lwsdk.AFUNC_OK

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("FG_NextLayerSE", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("FG_NextLayerSE", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/FG_NextLayerSE", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory("SK_FG_NextLayerSE", FgNextLayerSE): ServerTagInfo}
