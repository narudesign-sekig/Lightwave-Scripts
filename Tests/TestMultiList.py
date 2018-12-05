#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Test multilist control
display title
"""

import lwsdk

__author__ = "Makoto Sekiguchi"
__date__ = "Dec 4 2018"
__copyright__ = "Copyright (C) 2012 naru design"
__version__ = "0.0"
__maintainer__ = "Makoto Sekiguchi"
__status__ = "Test"
__lwver__ = "11"

RESOURCE = '\04(k:"%s" c:LWPy)'

multi_text = [["first", "1"], ["second", "2"], ["third", "333"]]
multi_title = ["Name", "Value"]


class testMultiListControl(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(testMultiListControl, self).__init__()

    def nameCallback(self, control, user_data, row, column):
        if row < 0:
            return RESOURCE % multi_title[column]

        return RESOURCE % multi_text[row][column]

    def countCallback(self, control, user_data):
        return len(multi_text)

    def columnCallback(self, control, user_data, column):
        if column >= len(multi_text[0]):
            return 0
        return 100

    def process(self, mod_command):
        ui = lwsdk.LWPanels()
        panel = ui.create(RESOURCE % 'Test Multilist Control')

        c1 = panel.multilist_ctl(RESOURCE % 'Multilist', 200, 10,
                                 self.nameCallback, self.countCallback, self.columnCallback)

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
