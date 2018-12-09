#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Dump layer name list
layer containing the mesh
"""

import lwsdk

__lwver__ = "11"


class HistoryData():
    def __init__(self):
        self.string = ''
        self.select_contains = False
        self.select_others = False


class DumpLayerNameCM(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(DumpLayerNameCM, self).__init__()

    def selectLayers(self, data):
        obj_funcs = lwsdk.LWObjectFuncs()
        state_query = lwsdk.LWStateQueryFuncs()

        obj_name = state_query.object()
        layer_list = state_query.layerList(lwsdk.OPLYR_NONEMPTY, obj_name)

        # there is no mesh !
        if layer_list == '':
            message_funcs = lwsdk.LWMessageFuncs()
            message_funcs.error('No mesh data', '')
            return lwsdk.AFUNC_OK

        current_obj = obj_funcs.focusObject()
        layers = layer_list.split(' ')

        foreground_layers = []
        background_layers = []

        for layer in layers:
            layer_int = int(layer) - 1

            # layer name is (unnamed), display None
            layer_name = obj_funcs.layerName(current_obj, layer_int)

            if layer_name == None:
                layer_name = ''

            if data.select_contains == (False if layer_name.find(data.string) < 0 else True):
                foreground_layers.append(layer)
            else:
                background_layers.append(layer)

            print('foreground_layers')
            print(foreground_layers)
            print('background_layers')
            print(background_layers)

    def process(self, mod_command):
        data = HistoryData
        data.string = "aaa"
        data.select_contains = True
        data.select_others = False

        self.selectLayers(data)
        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("LW_DumpLayerNameCM", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("LW_DumpLayerNameCM", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/LW_DumpLayerNameCM", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "LW_DumpLayerNameCM", DumpLayerNameCM): ServerTagInfo}
