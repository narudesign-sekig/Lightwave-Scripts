#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Select layers by string
"""

import lwsdk
from lwsdk.pris import recall, store

__author__      = "Makoto Sekiguchi"
__date__        = "Dec 5 2018"
__copyright__   = "Copyright (C) 2018 naru design"
__version__     = "1.03"
__maintainer__  = "Makoto Sekiguchi"
__status__      = "Release"
__lwver__       = "11"

list_history_title = ["String", "FG Layer", "Select others BG"]

class HistoryData():
    def __init__(self):
        self.string = ''
        self.select_contains = 0
        self.select_others = 0

class NoForegroundLayer(Exception):
    def __str__(self):
        return "No Foreground Layer"

class SelectLayersByString(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(SelectLayersByString, self).__init__()

        self.text_string = None
        self.hchoice_contains = None
        self.bool_others = None
        self.list_history = None
        self.button_remove = None
        self.bool_sort_history = None

        self.history = []
        self.selection = []
        self.sort_history = True
        self.last_string = None
        self.last_select_contains = 0
        self.last_others = 0

    # list_history name callback
    def nameCallback(self, control, user_data, row, column):
        if row < 0:
            return list_history_title[column]

        if column == 0:
            return self.history[row].string
        elif column == 1:
            return 'Contains' if self.history[row].select_contains else 'Not contains'
        else:
            return 'On' if self.history[row].select_others else 'Off'

    # list_history count callback
    def countCallback(self, control, user_data):
        if self.history == None:
            return 0

        return len(self.history)

    # list_history column callback
    def columnCallback(self, control, user_data, column):
        if column >= len(list_history_title):
            return 0
        return 150

    # list_history select callback
    def selectCallback(self, control, user_data, row, selecting):
        if row < 0:
            for i in range(len(self.selection)):
                self.selection[i] = False
        else:
            if selecting == 1:
                self.selection[row] = True
                self.text_string.set_str(self.history[row].string)
                self.hchoice_contains.set_int(not self.history[row].select_contains)
                self.bool_others.set_int(self.history[row].select_others)
            else:
                self.selection[row] = False

        self.refresh_button_remove()

    # toggle remove button enable/disable
    def refresh_button_remove(self):
        if self.selection.count(True) > 0:
            self.button_remove.enable()
        else:
            self.button_remove.ghost()

    # read history
    def read_history(self):
        self.history = recall("history", [])
        self.selection = [False] * len(self.history)
        self.sort_history = recall("sort_history", True)
        self.last_string = recall("last_string", "")
        self.last_select_contains = recall("last_select_contains", 0)
        self.last_others = recall("last_others", 0)

    # write history
    def write_history(self):
        store("history", self.history)
        store("sort_history", self.sort_history)
        store("last_string", self.last_string)
        store("last_select_contains", self.last_select_contains)
        store("last_others", self.last_others)

    # check duplicate history
    def search_history(self, history):
        if self.history != None:
            for index, data in enumerate(self.history):
                if data.string == history.string and data.select_contains == history.select_contains \
                        and data.select_others == history.select_others:
                    return index
        return - 1

    # remove history
    def remove_history(self, control, user_data):
        len_selection = len(self.selection)

        for i in range(len_selection):
            if self.selection[i]:
                self.history.pop(i - len_selection)

        while self.selection.count(True) > 0:
            self.selection.remove(True)

        self.list_history.redraw()
        self.list_history.set_addr_int([-1])
        self.refresh_button_remove()
        self.write_history()

    # move history record forward
    def move_history_record_forward(self, index):
        tmp = self.history.pop(index)
        self.history.insert(0, tmp)

    # add history
    def add_history(self, history):
        index = self.search_history(history)

        if index < 0 and len(history.string) > 0:
            self.history.insert(0, history)

        if index > 0 and self.sort_history:
            self.move_history_record_forward(index)

    # select layers
    def select_layers(self, mod, data):
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

            if data.select_contains == (0 if layer_name.find(data.string) < 0 else 1):
                foreground_layers.append(layer)
            else:
                background_layers.append(layer)

        if len(foreground_layers) == 0:
            raise NoForegroundLayer()

        if len(foreground_layers) > 0:
            cs_options = lwsdk.marshall_dynavalues(' '.join(foreground_layers))
            cs_setlayer = mod.lookup(mod.data, "SETALAYER")
            mod.execute(mod.data, cs_setlayer, cs_options, lwsdk.OPSEL_USER)

        if len(background_layers) > 0 and data.select_others:
            cs_options = lwsdk.marshall_dynavalues(' '.join(background_layers))
            cs_setlayer = mod.lookup(mod.data, "setblayer")
            mod.execute(mod.data, cs_setlayer, cs_options, lwsdk.OPSEL_USER)

    # set default values
    def set_default_values(self):
        if len(self.history) > 0:
            self.text_string.set_str(self.last_string)
            self.hchoice_contains.set_int(not self.last_select_contains)
            self.bool_others.set_int(self.last_others)
            self.bool_sort_history.set_int(self.sort_history)


    def process(self, mod_command):
        self.read_history()

        ui = lwsdk.LWPanels()
        panel = ui.create('Select layers by string ' + __version__ + ' - ' + __copyright__)

        self.text_string = panel.str_ctl("String", 50)
        self.hchoice_contains = panel.hchoice_ctl("Select FG Layer", ('Contains string', 'Not contains string'))
        self.bool_others = panel.bool_ctl("Select others as BG Layer")
        self.bool_sort_history = panel.bool_ctl("Move the last condition up if they match")
        self.list_history = panel.multilist_ctl('History', 450, 10, self.nameCallback, self.countCallback, self.columnCallback)
        self.button_remove = panel.button_ctl("Remove")
        self.button_remove.ghost()

        self.list_history.set_select(self.selectCallback)
        self.button_remove.set_event(self.remove_history)

        self.set_default_values()

        if panel.open(lwsdk.PANF_BLOCKING | lwsdk.PANF_CANCEL) == 0:
            ui.destroy(panel)

            return lwsdk.AFUNC_OK

        history = HistoryData()
        history.string = self.text_string.get_str()
        history.select_contains = not self.hchoice_contains.get_int()
        history.select_others = self.bool_others.get_int()

        self.last_string = history.string
        self.last_select_contains = history.select_contains
        self.last_others = history.select_others
        self.sort_history = self.bool_sort_history.get_int()

        self.add_history(history)
        self.write_history()

        try:
            self.select_layers(mod_command, history)

        except NoForegroundLayer:
            message_funcs = lwsdk.LWMessageFuncs()
            message_funcs.error('No foreground layer', '')

        finally:
            return lwsdk.AFUNC_OK

        ui.destroy(panel)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("SK_SelectLayersByString", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("SK_SelectLayersByString", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SK_SelectLayersByString", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory("SK_SelectLayersByString", SelectLayersByString): ServerTagInfo}
