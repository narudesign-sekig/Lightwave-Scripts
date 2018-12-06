#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
marshall_dynavalues???
"""

import lwsdk

__lwver__ = "11"


class DynaValue(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(DynaValue, self).__init__()
        self.foregroundLayers = ''
        self.backgroundLayers = ''

    # add foreground layer
    def addForegroundLayer(self, layer):
        self.foregroundLayers += ' ' + str(layer)

    # add background layer
    def addBackgroundLayer(self, layer):
        self.backgroundLayers += ' ' + str(layer)

    # select foreground layers
    def selectForegroundLayers(self, mod_command):
        py_dyna_values = lwsdk.marshall_dynavalues(self.foregroundLayers)
        cmd = mod_command.lookup(mod_command.data, "SETALAYER")
        mod_command.execute(mod_command.data, cmd,
                            py_dyna_values, lwsdk.OPSEL_USER)

    # select background layers
    def selectBackgroundLayers(self, mod_command):
        py_dyna_values = lwsdk.marshall_dynavalues(self.backgroundLayers)
        cmd = mod_command.lookup(mod_command.data, "SETBLAYER")
        mod_command.execute(mod_command.data, cmd,
                            py_dyna_values, lwsdk.OPSEL_USER)

    def process(self, mod_command):
        self.addForegroundLayer(1)
        self.addForegroundLayer(2)
        self.addForegroundLayer(6)

        self.addBackgroundLayer(3)
        self.addBackgroundLayer(10)

        self.selectForegroundLayers(mod_command)
        self.selectBackgroundLayers(mod_command)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("Dyna Values", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("Dyna Values", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/Dyna Values", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "LW_Dynavalues", DynaValue): ServerTagInfo}
