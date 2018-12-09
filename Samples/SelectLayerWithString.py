#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Select layer sample

Select layers with names includes "abc" as the foreground,
and select other layers as the background.
"""

import lwsdk

from lwsdk.pris.modeler import init, lyrsetfg, lyrsetbg

__lwver__ = "11"


class HistoryData():
    def __init__(self):
        self.string = ''
        self.select_contains = False
        self.select_others = False


class SelectLayerWithString(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(SelectLayerWithString, self).__init__()

        self.history = []

    def select_layers(self, mod_command, history):
        init(mod_command)
        objFuncs = lwsdk.LWObjectFuncs()
        currentObject = objFuncs.focusObject()
        numberOfLayers = objFuncs.maxLayers(currentObject)

        foregroundLayers = []
        backgroundLayers = []

        for i in range(numberOfLayers):
            name = objFuncs.layerName(currentObject, i)
            if name != None:
                if name.find(history.string) != -1:
                    foregroundLayers.append(str(i + 1))
                else:
                    backgroundLayers.append(str(i + 1))
            else:
                backgroundLayers.append(str(i + 1))

        lyrsetfg(' '.join(foregroundLayers))
        lyrsetbg(' '.join(backgroundLayers))

    def process(self, mod_command):
        history = HistoryData()
        history.string = "___"
        history.select_contains = False
        history.select_others = False

        self.select_layers(mod_command, history)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("Select Layer With String", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("Select Layer With String", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SelectLayerWithString",
     lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "LW_SelectLayerWithString", SelectLayerWithString): ServerTagInfo}
