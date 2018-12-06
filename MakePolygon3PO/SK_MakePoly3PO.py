#! /usr/bin/env python
# -*- Mode: Python -*-
# -*- coding: ascii -*-

"""
Make 4 points polygon form selected 3 poitns.
"""

import lwsdk
from lwsdk.pris.modeler import selmode, pointcount, editbegin, init, editend, pointinfo, getpoints, addpoint, addpolygon, selpoint, exit

__author__ = "Makoto Sekiguchi"
__date__ = "Dec 4 2018"
__copyright__ = "Copyright (C) 2012 naru design"
__version__ = "1.1"
__maintainer__ = "Makoto Sekiguchi"
__status__ = "Released"
__lwver__ = "11"


class makePoly3PO(lwsdk.ICommandSequence):
    def __init__(self, context):
        super(makePoly3PO, self).__init__()

    # calculate vector of the point to be add
    def calculatePoint4(self, p1, p2, p3):
        p4 = p1 + p3 - p2
        return p4

    def process(self, mod_command):
        init(mod_command)
        selmode(lwsdk.OPSEL_DIRECT)

        ret = editbegin()

        n = pointcount()
        if n == 3:
            points = getpoints()
            p1 = pointinfo(points[0])
            p2 = pointinfo(points[1])
            p3 = pointinfo(points[2])

            p4 = self.calculatePoint4(p1, p2, p3)
            point = addpoint(p4)

            listPoints = list(points)
            listPoints.append(point)
            addpolygon(listPoints)

            mod_command.evaluate(mod_command.data, "SEL_POINT CLEAR")

        editend()

        return lwsdk.AFUNC_OK


ServerTagInfo = [
    ("SK_MakePoly3PO", lwsdk.SRVTAG_USERNAME | lwsdk.LANGID_USENGLISH),
    ("SK_MakePoly3PO", lwsdk.SRVTAG_BUTTONNAME | lwsdk.LANGID_USENGLISH),
    ("Utilities/SK_MakePoly3PO", lwsdk.SRVTAG_MENU | lwsdk.LANGID_USENGLISH)
]

ServerRecord = {lwsdk.CommandSequenceFactory(
    "SK_MakePoly3PO", makePoly3PO): ServerTagInfo}
