#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Test multilist control
restore values from list
"""

import lwsdk

__author__ = "Makoto Sekiguchi"
__date__ = "Dec 5 2018"
__copyright__ = "Copyright (C) 2012 naru design"
__version__ = "0.0"
__maintainer__ = "Makoto Sekiguchi"
__status__ = "Test"
__lwver__ = "11"

RESOURCE = '\04(k:"%s" c:LWPy)'

multi_text = [
    ["first", True, False],
    ["second", True, False],
    ["third", True, True],
    ["four", False, False]
]
multi_title = ["String", "contains string (FG)", "others (BG)"]


class testMultiListControl(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(testMultiListControl, self).__init__()
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None

    def nameCallback(self, control, user_data, row, column):
        if row < 0:
            return RESOURCE % multi_title[column]

        return RESOURCE % multi_text[row][column]

    def countCallback(self, control, user_data):
        return len(multi_text)

    def columnCallback(self, control, user_data, column):
        if column >= len(multi_text[0]):
            return 0
        return 150

    def selectCallback(self, control, user_data, row, selecting):
        print str(row)
        print selecting

        if row < 0:
            return

        if selecting == 1:
            self.c2.set_str(multi_text[row][0])
            self.c3.set_int(1 if multi_text[row][1] else 0)
            self.c4.set_int(1 if multi_text[row][2] else 0)

    def process(self, mod_command):
        ui = lwsdk.LWPanels()
        panel = ui.create(RESOURCE %
                          'Select layers with string - Copyright(C)2012 naru design')

        self.c2 = panel.str_ctl(RESOURCE % "String", 50)
        self.c3 = panel.bool_ctl(RESOURCE % "contains string (FG)")
        self.c4 = panel.bool_ctl(RESOURCE % "others (BG)")
        self.c1 = panel.multilist_ctl(RESOURCE % 'History', 450, 10,
                                      self.nameCallback, self.countCallback, self.columnCallback)

        self.c1.set_select(self.selectCallback)

        if panel.open(lwsdk.PANF_BLOCKING | lwsdk.PANF_CANCEL) == 0:
            ui.destroy(panel)
            return lwsdk.AFUNC_OK

        ui.destroy(panel)

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("SK_MultilistControl", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("SK_MultilistControl", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SK_MultilistControl", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "SK_MultilistControl", testMultiListControl): ServerTagInfo}
