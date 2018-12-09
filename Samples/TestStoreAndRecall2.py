#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Test store and recall value
"""

import lwsdk
from lwsdk.pris import store, recall

__lwver__ = "11"

class myData:
    def __init__(self):
        self.value1 = 0
        self.value2 = 1
        self.value3 = "string data"

class testStoreAndRecall2(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(testStoreAndRecall2, self).__init__()

    def process(self, generic_access):
        arr = []

        tmpArr = recall("arr")
        if tmpArr != None:
            arr = tmpArr

        print arr
        
        dt = myData()
        arr.append(dt)

        print arr

        store("arr", arr)

        return lwsdk.AFUNC_OK

ServerTagInfo = [
                    ( "Python Test Store And Recall 2", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH ),
                    ( "Store And Recall 2", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH ),
                    ( "Utilities/Python", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH )
                ]

ServerRecord = { lwsdk.CommandSequenceFactory("LW_PyStoreAndRecall", testStoreAndRecall2) : ServerTagInfo }