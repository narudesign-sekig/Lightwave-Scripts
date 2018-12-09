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

    def process(self, mod_command):

        # OK
        cs_options = lwsdk.marshall_dynavalues('1 2 4')

        # OK
        # cs_options = lwsdk.marshall_dynavalues(' '.join(["1", "2", "4"]))

        # NG case
        # cs_options = lwsdk.marshall_dynavalues(["1", "2", "4"])

        # NG case
        # layerList = []
        # layerList.append(str(1))
        # layerList.append(str(2))
        # layerList.append(str(4))
        # cs_options = lwsdk.marshall_dynavalues(layerList)

        # NG case
        # layerList = []
        # layerList.append(1)
        # layerList.append(2)
        # layerList.append(4)
        # cs_options = lwsdk.marshall_dynavalues(layerList)

        cs_setlayer = mod_command.lookup(mod_command.data, "SETALAYER")
        result, dyna_value = mod_command.execute(
            mod_command.data, cs_setlayer, cs_options, lwsdk.OPSEL_USER)

        cs_options = lwsdk.marshall_dynavalues('3 10')
        cs_setlayer = mod_command.lookup(mod_command.data, "setblayer")
        result, dyna_value = mod_command.execute(
            mod_command.data, cs_setlayer, cs_options, lwsdk.OPSEL_USER)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("Select Layer By Name", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("Select Layer", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/Python", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)


]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "LW_SelectLayer", selectLayer): ServerTagInfo}
