#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
    Cloudtag 
    
    author: steve göring
    contact: stg7@gmx.de
    2012
    
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
import urllib.request, re 

films= ["Star_Trek:_Der_Film",\
"Star_Trek_II:_Der_Zorn_des_Khan",\
"Star_Trek_III:_Auf_der_Suche_nach_Mr._Spock",\
"Star_Trek_IV:_Zur%C3%BCck_in_die_Gegenwart",\
"Star_Trek_V:_Am_Rande_des_Universums",\
"Star_Trek_VI:_Das_unentdeckte_Land",\
"Star_Trek:_Treffen_der_Generationen",\
"Star_Trek:_Der_erste_Kontakt",\
"Star_Trek:_Der_Aufstand",\
"Star_Trek:_Nemesis",\
"Star_Trek_(2009)"]

i = 1
for title in films:
    patt = """http://de.wikipedia.org/w/api.php?format=xml&action=query&titles="""+title+"""&rvprop=content&prop=revisions"""
    content = urllib.request.urlopen(patt).read().decode("utf8")
    
    content = re.compile(r'<.*?>').sub('', content) # remove tags stuff
    
    stri = "%.2d" % (i)
    print(stri)
    f = open(stri+".txt","w")
    f.write(content)
    f.close()
    i+=1

