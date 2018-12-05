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


class SelectLayerWithString(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(SelectLayerWithString, self).__init__()

        self.target = "abc"

    def process(self, mod):
        init(mod)
        objFuncs = lwsdk.LWObjectFuncs()
        currentObject = objFuncs.focusObject()
        numberOfLayers = objFuncs.maxLayers(currentObject)

        foregroundLayers = []
        backgroundLayers = []

        for i in range(numberOfLayers):
            name = objFuncs.layerName(currentObject, i)
            if name != None:
                if name.find(self.target) != -1:
                    foregroundLayers.append(str(i + 1))
                else:
                    backgroundLayers.append(str(i + 1))
            else:
                backgroundLayers.append(str(i + 1))

        lyrsetfg(' '.join(foregroundLayers))
        lyrsetbg(' '.join(backgroundLayers))

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("Select Layer With String", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("Select Layer With String", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SelectLayerWithString",
     lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "LW_SelectLayerWithString", SelectLayerWithString): ServerTagInfo}
