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

    def process(self, mod_command):

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("SK_MoveSelPolyBG", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("SK_MoveSelPolyBG", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SK_MoveSelPolyBG", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory("SK_MoveSelPolyBG", MoveSelPolyBG): ServerTagInfo}
