#!/usr/bin/python3
"""
    Cloudtag

    author: Steve Göring
    contact: stg7@gmx.de

"""
"""
    This file is part of cloudtag.

    cloudtag is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    cloudtag is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with cloudtag.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import random
import math

# for font measuring
from tkinter import *
from tkinter import font

from .log import lInfo

Tk()




class ctag_color:
    """
    color class
    """

    def __init__(self, minColor, maxColor):
        self._minCol = (int(minColor[0:2], 16), int(minColor[2:4], 16), int(minColor[4:6], 16))
        self._maxCol = (int(maxColor[0:2], 16), int(maxColor[2:4], 16), int(maxColor[4:6], 16))
        self._colors = {}

    def __get_hex(self, a):
        """
        convert value a to hex string, with leading zeros
        """
        aa = hex(a)[2:]
        if len(aa) < 2:
            aa = "0" + aa
        return aa

    def scale(self, minfreq, maxfreq):
        self._scalefactor = ((self._maxCol[0] - self._minCol[0] + 0.0) / (maxfreq - minfreq),
                             (self._maxCol[1] - self._minCol[1] + 0.0) / (maxfreq - minfreq),
                             (self._maxCol[2] - self._minCol[2] + 0.0) / (maxfreq - minfreq))
        self._minfreq = minfreq
        self._maxfreq = maxfreq

    def calc_color(self, key, freq):
        self._colors[key] = "#" + "".join([self.__get_hex(self._minCol[j] + int(round((freq - self._minfreq) * self._scalefactor[j]))) for j in range(0, 3)])
        return self._colors[key]

    def get_color(self, key):
        return self._colors[key]


class ctag_font:
    """
    font class
    """

    def __init__(self, minSize, maxSize):
        self._minSize = int(minSize)
        self._maxSize = int(maxSize)
        self._sizes = {}

    def scale(self, minfreq, maxfreq):
        self._scalefactor = (self._maxSize - self._minSize + 0.0) / (maxfreq - minfreq)
        self._minfreq = minfreq
        self._maxfreq = maxfreq

    def calc_size(self, key, freq):
        self._sizes[key] = str(self._minSize + int(round((freq - self._minfreq) * self._scalefactor)))
        return int(self._sizes[key])

    def get_size(self, key):
        return int(self._sizes[key])


def svg_cloud(histogram, min_font_size=14, max_font_size=90, min_font_color="001122", max_font_color="0000FF"):

    template_base ="""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:ev="http://www.w3.org/2001/xml-events"
        version="1.1" baseProfile="full"
        width="{w}px" height="{h}px" viewBox="0 0 {w} {h}"> <!-- dont change viewbox, and aspect ratio-->
<!-- translate to center  -->
<g transform="translate({halfW},{halfH})">
{text}
</g>

</svg>
"""
    template_text = """<text x='{x}' y='{y}' font-size='{fsize}px'   style='{style}' font-family='Courier New' {add}>{text}</text>"""
    template_rectangle = """<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:{color};fill-opacity:0.1;" /> """

    _color = ctag_color(min_font_color, max_font_color)
    _font = ctag_font(min_font_size, max_font_size)

    sorted_hist = sorted(histogram.items(), key=lambda x: x[1], reverse=True)

    min_freq = sorted_hist[-1][1]
    max_freq = sorted_hist[0][1]
    _font.scale(min_freq, max_freq)
    _color.scale(min_freq, max_freq)

    initial_max_pos = 30  # same for x and y
    direction = 1
    random.seed(1)

    # initialize positions (random)
    lInfo("initialize positions randomly")
    layout = []
    for (token, freq) in sorted_hist:

        size = _font.calc_size(token, freq)
        color = _color.calc_color(token, freq)

        font_instance = font.Font(family="courier", size=-int(size), weight=NORMAL)
        text_height = font_instance.metrics("ascent")# + font_instance.metrics("descent")
        descent = font_instance.metrics("descent")
        text_width = font_instance.measure(token)

        # get random x,y positions within a circle: x^2+y^2<= initial_max_pos^2
        x = random.randint(-initial_max_pos, initial_max_pos)
        y = math.sqrt(random.randint(0, initial_max_pos * initial_max_pos - x * x))
        if random.randint(0, 1) == 0:
            y = -y

        if direction % 2 == 0:
            # text is vertical: change size
            # find letter with max width
            #text_width = max([font_instance.measure(c) for c in token])
            direction = 0
            layout.append([x, y, direction, text_height, text_width, size, descent])
        else:
            layout.append([x, y, direction, text_height, text_width, size, descent])
        #direction += 1

    lInfo("align positions")

    from .rtree import RTree, Rect

    def colission(aligned, rect):
        (x, y, xx, yy) = rect
        w = xx - x
        h = yy - y
        tx = x + w / 2
        ty = y + h / 2
        for (_x, _y, _xx, _yy) in aligned:
            _w = _xx - _x
            _h = _yy - _y
            _tx = _x + _w / 2
            _ty = _y + _h / 2
            if abs(_tx - tx) < (w + _w) / 2 and abs(_ty - ty) < (h + _h) / 2:
                return True
        return False

    rt = RTree()
    max_steps = 100000
    i = 0
    aligned = []
    for (token, freq) in sorted_hist:
        x, y, direction, h, w, size, descent = layout[i]

        # find new position with archimedis spiral
        # (1) spiralstep width = 1:
        a = 1
        # (2) angle step delta phi
        dF = 0.1
        F = dF
        steps = 0
        while list(rt.query_rect(Rect(x, y, x + w, y + h))) != [] and steps < max_steps:
            x = x + math.sin(F) * a * F
            y = y + math.cos(F) * a * F
            F += dF
            steps += 1
        steps = 0
        while colission(aligned, (x, y, x + w, y + h)) and steps < max_steps:
            print("col test")
            x = x + math.sin(F) * a * F
            y = y + math.cos(F) * a * F
            F += dF
            steps += 1

        aligned.append((x, y, x + w, y + h))
        rt.insert(i, Rect(x, y, x + w, y + h))
        layout[i] = x, y, direction, h, w, size, descent
        i += 1

    print(layout[0])
    print(layout[1])

    text = ""
    i = 0
    for (token, freq) in sorted_hist:
        x, y, direction, text_height, text_width, size, descent = layout[i]

        style = "fill:" + _color.get_color(token)

        """xx = int(x - text_width / 2)
        yy = int(y + text_height / 3 )
        """
        transform = ""

        if direction == 0:  # text `token` is vertical
            xx = int(x + text_height / 3)
            yy = int(y + text_width / 2)
            transform = "transform='rotate(-90,{},{})'".format(xx, yy)
        rect_color = _color.get_color(token)

        if i == 0:
            rect_color = "green"

        text += template_rectangle.format(x=x, y=y, h=text_height, w=text_width, color=rect_color)
        text += template_text.format(x=x, y=y + size - descent, fsize=size, style=style, add=transform, text=token) + "\n"
        i += 1

    result = template_base.format(text=text, w=800, h=800, halfW=800/2, halfH=800/2)

    return result


def old():

    class xy(tuple):
        """
        minmal 2d vector class: no check that lengths are compatable.
        """

        def __add__(self, a):
            return xy(x + y for x, y in zip(self, a))

        def __sub__(self, a):
            return xy(x - y for x, y in zip(self, a))

        def __mul__(self, c):
            return xy(x * c for x in self)

        def __rmul__(self, c):
            return xy(c * x for x in self)

        def nabs(self):
            (x, y) = self
            return x * x + y * y

        def man(self, o):
            (x, y) = self - o
            return abs(x) + abs(y)

        def min(self):
            (x, y) = self
            return min(x, y)

        def x(self):
            (x, y) = self
            return x

        def y(self):
            (x, y) = self
            return y

        def swap(self):
            (x, y) = self
            return xy([y, x])


    def checkAll(worked, pos, i, sizes):
        """
        check collision with i and all nodes in worked

        !! learn, that python tuple unpacking is a performance killer
        """
        overlap = False
        ix = pos[i][0]
        iy = pos[i][1]

        six = sizes[i][0] / 2
        siy = sizes[i][1] / 2

        for k in worked.difference([i]):
            dx = ix - pos[k][0]
            dy = iy - pos[k][1]

            sx = six + sizes[k][0] / 2
            sy = siy + sizes[k][1] / 2
            # colision
            if abs(dx) < sx and abs(dy) < sy:
                return True
        return overlap


    class svgcloud:

        def __init__(self, patternFile, delim, config):
            # set color & font settings
            self._color = ctlib.ctcolor(config['color']['min'], config['color']['max'])
            self._font = ctlib.ctfont(config['font']['min'], config['font']['max'])

            # read pattern
            self._pattern = ctlib.ctpattern(patternFile, delim)

        def createCloud(self, Buckets, maxSize, minSize, maxWords, outfile):
            start = time.time()

            (minfreq, maxfreq, tmp) = ctlib.bucketsToList(Buckets, maxWords)

            self._font.scale(minfreq, maxfreq)
            self._color.scale(minfreq, maxfreq)

            pos = {}  # positions
            parent = Buckets[maxfreq][0]  # parent word

            sizes = {}  # width and hight
            fontsizes = {}
            info = {}  # freq values
            dirs = set([])  # directions
            colors = {}

            maxx = 30
            dir = 1
            dirstep = 1  # get from config param TODO
            random.seed(1)

            # for font measuing: initialize Tk
            Tk()

            print("precalculation")
            # initialize positions (random)
            for (i, k) in tmp:

                size = int(self._font.calcSize(k, i))
                color = self._color.calcColor(k, i)

                f = font.Font(family="courier", size=-int(size), weight=NORMAL)
                h = size
                w = f.measure(k)

                # get random x,y positions within a circle: x^2+y^2<= maxx^2
                x = random.randint(-maxx, maxx)
                yy = random.randint(0, maxx * maxx - x * x)
                y = math.sqrt(yy)
                if random.randint(0, 1) == 0:
                    y = -y

                info[k] = i
                sizes[k] = xy([w, h])

                if dir % 2 == 0:
                    # text is vertical: store direction and change size
                    dirs.add(k)
                    # find letter with max width
                    w = max([f.measure(c) for c in k])
                    # change dimension
                    sizes[k] = sizes[k].swap()
                    dir = 0

                pos[k] = xy([x, y])
                dir += dirstep
                print(".", end="")
                sys.stdout.flush()

            print("done")
            # center parent
            pos[parent] = xy([0, 0])

            # "pre"calculated spiral
            spiral = {}

            colisionSum = 0
            worked = set([parent])  # elements that fits
            print("calculate positions")

            # calculate positions that doesn't overlapp
            for (_, i) in tmp[1:]:
                # check if node i overlaps any other node in worked set
                overlap = checkAll(worked, pos, i, sizes)

                # find new position with archimedis spiral
                # (1) spiralstep width = 1:
                a = 1
                # (2) angle step delta phi
                dF = 0.1
                F = dF

                colisionCount = 1  # count collision tests
                while overlap:
                    if F not in spiral:  # store spiral values
                        spiral[F] = xy([math.sin(F) * a * F, math.cos(F) * a * F])
                    # calc new pos
                    pos[i] += spiral[F]
                    colisionCount += 1
                    F += dF
                    # check overlapping
                    overlap = checkAll(worked, pos, i, sizes)

                colisionSum += colisionCount
                worked.add(i)
                print(".", end="")
                sys.stdout.flush()

            end = time.time()
            rtime = str(end - start)

            print("done")
            print("with " + str(colisionSum) + " collision-tests in: " + rtime + " s")

            # output
            maxx = 0
            minx = 0
            maxy = 0
            miny = 0
            outfile.write(self._pattern.getHeader() + "\n")
            for (_, o) in tmp:
                freq = info[o]
                (x, y) = pos[o]
                (w, h) = sizes[o]

                # calculate max / min x/y values
                maxx = max(maxx, x, x + w)
                maxy = max(maxy, y, y + h)

                minx = min(minx, x, x + w)
                miny = min(miny, y, y + h)

                style = "fill:" + self._color.getColor(o)

                if o in dirs:  # text o is vertical
                    xx = int(x + w / 3)
                    yy = int(y + h / 2)
                    transform = "transform='rotate(-90," + str(xx) + "," + str(yy) + ")'"
                else:
                    xx = int(x - w / 2)
                    yy = int(y + h / 3)
                    transform = ""

                # content for pattern
                content = [xx, yy, self._font.getSize(o), style, transform, o, "\n"]

                outfile.write(self._pattern.getElement(content))

            outfile.write(self._pattern.getFooter())
            outfile.write("<!-- size = " + str(int(max(maxx - minx, maxy - miny))) + " (should be <= 800, otherwise change viewbox and translate param in svg -->")

            return

        def getExt(self):
            return ".svg"


