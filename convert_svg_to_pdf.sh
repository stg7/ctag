#!/bin/bash
#
#    Cloudtag
#
#    author: Steve Göring
#    contact: stg7@gmx.de
#
#
#
#    This file is part of cloudtag.
#
#    cloudtag is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    cloudtag is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with cloudtag.  If not, see <http://www.gnu.org/licenses/

if [[ "$#" != 2 ]]; then
    echo "usage: $0 input_svg output_pdf"
    exit 1
fi

if [[ "$(which inkscape | wc -l)" == 0 ]]; then
    echo "you need to install inkscape."
    exit 1
fi

inkscape "$1" --export-pdf="$2"
