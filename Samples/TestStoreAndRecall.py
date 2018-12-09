#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Test store and recall value
"""

import lwsdk
from lwsdk.pris import store, recall

__lwver__ = "11"

class testStoreAndRecall(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(testStoreAndRecall, self).__init__()

    def process(self, generic_access):
        store('a', 111)
        v = recall('b', 123)

        print "value = " + str(v)

        store("str", "string")
        v = recall("str", "none")

        print "value = " + v

        list = [5,3,1,0]
        store("array", list)
        print list

        recallList = []
        recallList = recall("array")

        print recallList

        recallList = recall("array2")

        print recallList

        return lwsdk.AFUNC_OK

ServerTagInfo = [
                    ( "Python Test Store And Recall", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH ),
                    ( "Store And Recall", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH ),
                    ( "Utilities/Python", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH )
                ]

ServerRecord = { lwsdk.CommandSequenceFactory("LW_PyStoreAndRecall", testStoreAndRecall) : ServerTagInfo }