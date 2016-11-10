#!/usr/bin/env python3
"""
    Copyright 2016-today
    Project Ctag

    Author: Steve Göring
"""
"""
    colored simple logging methods

    This file is part of ctag.

    ctag is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ctag is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ctag.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import pprint


def colorred(m):
    return "\033[91m" + m + "\033[0m"


def colorblue(m):
    return "\033[94m" + m + "\033[0m"


def colorgreen(m):
    return "\033[92m" + m + "\033[0m"


def colorcyan(m):
    return "\033[96m" + m + "\033[0m"


def lInfo(msg):
    print(colorgreen("[INFO ] ") + str(msg))


def lError(msg):
    print(colorred("[ERROR] ") + str(msg))


def lDbg(msg):
    print(colorblue("[DEBUG] ") + str(msg))


def lWarn(msg):
    print(colorcyan("[WARN ] ") + str(msg))


def lHelp(msg):
    print(colorblue("[HELP ] ") + str(msg))


def jPrint(x, output=True):
    str_x = json.dumps(x, indent=4, sort_keys=True)
    if output:
        lInfo("\n" + str_x)
    return str_x


def pPrint(x, output=True):
    pp = pprint.PrettyPrinter(indent=4)
    str_x = pp.pformat(x)
    if output:
        lInfo("\n" + str_x)
    return str_x


if __name__ == "__main__":
    lError("lib is not a standalone module")
    exit(-1)
