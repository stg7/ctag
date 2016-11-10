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
    i = 0
    for (token, freq) in sorted_hist:

        size = _font.calc_size(token, freq)
        color = _color.calc_color(token, freq)

        font_instance = font.Font(family="courier", size=-int(size), weight=NORMAL)
        text_height = font_instance.metrics("ascent") + font_instance.metrics("descent")
        descent = font_instance.metrics("descent")
        text_width = font_instance.measure(token)

        # get random x,y positions within a circle: x^2+y^2<= initial_max_pos^2
        x = random.randint(-initial_max_pos, initial_max_pos)
        y = math.sqrt(random.randint(0, initial_max_pos * initial_max_pos - x * x))
        if i == 0:
            x = 0
            y = 0

        if random.randint(0, 1) == 0:
            y = -y

        if direction % 2 == 0:
            # text is vertical
            direction = 0
            layout.append([x, y, direction, text_width, text_height, size, descent])
        else:
            layout.append([x, y, direction, text_height, text_width, size, descent])
        direction += 1
        i += 1

    lInfo("align positions")

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

    max_steps = 10000000
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
        # Note: tried Rtree but it was bad
        while colission(aligned, (x, y, x + w, y + h)) and steps < max_steps:
            x += math.sin(F) * a * F
            y += math.cos(F) * a * F
            F += dF
            steps += 1

        aligned.append((x, y, x + w, y + h))
        layout[i] = x, y, direction, h, w, size, descent
        i += 1

    text = ""
    i = 0
    x, y, _, initial_text_height, initial_text_width, _, _ = layout[0]
    maxx = x
    maxy = y
    minx = x
    miny = y

    for (token, freq) in sorted_hist:
        x, y, direction, text_height, text_width, size, descent = layout[i]

        x = x - initial_text_width / 2
        y = y - initial_text_height / 2
        style = "fill:" + _color.get_color(token)
        yt = y
        xt = x
        transform = ""

        if direction == 0:  # text `token` is vertical
            transform = "transform='rotate(+90,{},{})'".format(x, y)
            yt += -descent / 2
            # after transformation your x and y axis are still the same

        else:
            yt += size - descent / 2

        rect_color = _color.get_color(token)

        if i == 0:
            rect_color = "green"

        #text += template_rectangle.format(x=x, y=y, h=text_height, w=text_width, color=rect_color)
        text += template_text.format(x=xt, y=yt, fsize=size, style=style, add=transform, text=token) + "\n"
        i += 1
        maxx = max(xt + size, maxx, xt + text_width + size)
        minx = min(xt - size, minx, xt + text_width - size)
        maxy = max(yt + size, maxy, yt + text_height + size)
        miny = min(yt - size, miny, xt + text_height - size)

    width = int(1.2 * (maxx - minx))
    height = int(1.2 * (maxy - miny))

    result = template_base.format(text=text, w=width, h=height, halfW=width/2, halfH=height/2)

    return result
