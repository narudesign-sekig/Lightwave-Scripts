#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
store and recall history list

- remove button
- remove history
"""

import lwsdk
from lwsdk.pris import recall, store

__lwver__ = "11"

RESOURCE = '\04(k:"%s" c:LWPy)'

list_title = ["String", "contains string (FG)", "others (BG)"]


class historyData():
    def __init__(self):
        self.string = ''
        self.isContain = False
        self.selectOthers = False


class historyList(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(historyList, self).__init__()
        self.listHistory = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.removeButton = None
        self.history = []
        self.selection = []

    def nameCallback(self, control, user_data, row, column):
        if row < 0:
            return RESOURCE % list_title[column]

        if column == 0:
            return self.history[row].string

        if column == 1:
            return 'True' if self.history[row].isContain else 'False'

        return 'True' if self.history[row].selectOthers else 'False'

    def countCallback(self, control, user_data):
        if self.history == None:
            return 0

        return len(self.history)

    def columnCallback(self, control, user_data, column):
        if column >= len(list_title):
            return 0
        return 150

    # select list item callback

    def selectCallback(self, control, user_data, row, selecting):
        print "row = " + str(row) + ", selecting = " + str(selecting)
        if row < 0:
            for i in range(len(self.selection)):
                self.selection[i] = False
        else:
            if selecting == 1:
                self.selection[row] = True
                self.c2.set_str(self.history[row].string)
                self.c3.set_int(1 if self.history[row].isContain else 0)
                self.c4.set_int(1 if self.history[row].selectOthers else 0)
            else:
                self.selection[row] = False

        print self.selection
        print self.selection.count(True)

        self.refreshRemoveButton()

    # remove button callback

    def clickRemoveCallback(self, control, user_data):
        print "clicked!"

        nofSelection = len(self.selection)
        for i in range(nofSelection):
            if self.selection[i]:
                self.history.pop(i - nofSelection)

        while self.selection.count(True) > 0:
            self.selection.remove(True)

        print self.history
        print self.selection

        self.listHistory.redraw()
        self.listHistory.set_addr_int([-1])

    # check duplicate history

    def searchHistory(self, history):
        if self.history == None:
            return -1

        for index, data in enumerate(self.history):
            if data.string == history.string:
                if data.isContain == history.isContain:
                    if data.selectOthers == history.selectOthers:
                        return index
        return -1

    # move history record forward

    def moveHistoryRecordForward(self, index):
        if index == 0:  # no need move
            return

        tmp = self.history.pop(index)
        self.history.insert(0, tmp)

    # toggle remove button enable/disable

    def refreshRemoveButton(self):
        if self.selection.count(True) > 0:
            self.removeButton.enable()
        else:
            self.removeButton.ghost()

    def process(self, mod_command):
        self.history = recall("history", [])
        self.selection = [False] * len(self.history)
        print self.selection

        ui = lwsdk.LWPanels()
        panel = ui.create(RESOURCE % 'historyList')

        self.c2 = panel.str_ctl(RESOURCE % "String", 50)
        self.c3 = panel.bool_ctl(RESOURCE % "contains string (FG)")
        self.c4 = panel.bool_ctl(RESOURCE % "others (BG)")
        self.listHistory = panel.multilist_ctl(RESOURCE % 'History', 450, 10,
                                               self.nameCallback, self.countCallback, self.columnCallback)
        self.removeButton = panel.button_ctl(RESOURCE % "Remove")
        self.removeButton.ghost()

        self.listHistory.set_select(self.selectCallback)
        self.removeButton.set_event(self.clickRemoveCallback)

        if panel.open(lwsdk.PANF_BLOCKING | lwsdk.PANF_CANCEL) == 0:
            ui.destroy(panel)
            return lwsdk.AFUNC_OK

        tmp_history = historyData()
        tmp_history.string = self.c2.get_str()
        tmp_history.isContain = False if self.c3.get_int() < 1 else True
        tmp_history.selectOthers = False if self.c4.get_int() < 1 else True

        index = self.searchHistory(tmp_history)

        if index < 0:
            if len(tmp_history.string) > 0:
                self.history.insert(0, tmp_history)
                store("history", self.history)
        else:
            self.moveHistoryRecordForward(index)
            store("history", self.history)

        ui.destroy(panel)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("historyList", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("historyList", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/historyList", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)


]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "historyList", historyList): ServerTagInfo}
