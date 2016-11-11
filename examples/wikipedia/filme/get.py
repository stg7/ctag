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

films= ["Avatar_%E2%80%93_Aufbruch_nach_Pandora",\
"Harry_Potter_und_die_Heiligt%C3%BCmer_des_Todes:_Teil_2",\
"Transformers_3",\
"Der_Herr_der_Ringe:_Die_R%C3%BCckkehr_des_K%C3%B6nigs_(Film)",\
"Pirates_of_the_Caribbean_%E2%80%93_Fluch_der_Karibik_2",\
"Toy_Story_3",\
"Pirates_of_the_Caribbean_%E2%80%93_Fremde_Gezeiten",\
"Alice_im_Wunderland_(2010)",\
"Star_Wars:_Episode_I_%E2%80%93_Die_dunkle_Bedrohung",\
"The_Dark_Knight",\
"Harry_Potter_und_der_Stein_der_Weisen_(Film)",\
"Pirates_of_the_Caribbean_%E2%80%93_Am_Ende_der_Welt",\
"Harry_Potter_und_die_Heiligt%C3%BCmer_des_Todes:_Teil_1",\
"Der_K%C3%B6nig_der_L%C3%B6wen",\
"Harry_Potter_und_der_Orden_des_Ph%C3%B6nix_(Film)",\
"Harry_Potter_und_der_Halbblutprinz_(Film)",\
"Der_Herr_der_Ringe:_Die_zwei_T%C3%BCrme_(Film)",\
"Shrek_2_%E2%80%93_Der_tollk%C3%BChne_Held_kehrt_zur%C3%BCck",\
"Jurassic_Park",\
"Harry_Potter_und_der_Feuerkelch_(Film)",\
"Spider-Man_3",\
"Ice_Age_3:_Die_Dinosaurier_sind_los",\
"Harry_Potter_und_die_Kammer_des_Schreckens_(Film)",\
"Der_Herr_der_Ringe:_Die_Gef%C3%A4hrten_(Film)",\
"Findet_Nemo",\
"Star_Wars:_Episode_III_%E2%80%93_Die_Rache_der_Sith",\
"Transformers_%E2%80%93_Die_Rache",\
"Inception",\
"Spider-Man_(Film)",\
"Independence_Day_(1996)",\
"Shrek_der_Dritte",\
"Harry_Potter_und_der_Gefangene_von_Askaban_(Film)",\
"E._T._%E2%80%93_Der_Au%C3%9Ferirdische",\
"Indiana_Jones_und_das_K%C3%B6nigreich_des_Kristallsch%C3%A4dels",\
"Spider-Man_2",\
"Krieg_der_Sterne",\
"2012_(Film)",\
"The_Da_Vinci_Code_%E2%80%93_Sakrileg",\
"F%C3%BCr_immer_Shrek",\
"Die_Chroniken_von_Narnia:_Der_K%C3%B6nig_von_Narnia_(2005)",\
"Matrix_Reloaded"
]

i = 1
for title in films:
    patt = """http://de.wikipedia.org/w/api.php?format=xml&action=query&titles="""+title+"""&rvprop=content&prop=revisions"""
    content = urllib.request.urlopen(patt).read().decode("utf8")
    
    content = re.compile(r'<.*?>').sub('', content) # remove tags stuff
    
    stri = "%.3d" % (i)
    print(stri)
    f = open(stri+".txt","w")
    f.write(content)
    f.close()
    i+=1

