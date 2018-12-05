#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Select layer sample
"""

import lwsdk

__lwver__ = "11"


class selectLayer(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(selectLayer, self).__init__()

    def process(self, mod):
        mod.evaluate(mod.data, 'setlayer "1 2 4"')
        mod.evaluate(mod.data, 'SETBLAYER "10"')

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("Select Layer By Name", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("Select Layer", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/Python", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "LW_SelectLayer", selectLayer): ServerTagInfo}
