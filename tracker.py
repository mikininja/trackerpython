# -*- coding: utf-8 -*-
"""
Created on Thu May 11 20:13:26 2017

@author: Michele
"""

import gmplot
import os
import socket
from string import split
from string import lstrip
from string import rstrip
from geoip import geolite2


ip=raw_input("Inserisci l'ip per visualizzare il percorso: ")
# chiede all'utente di inserire il nome/ip di un host
f=os.popen('tracert '+ip)
# usa os.open per lanciare un comando da cmd, in questo caso tracert che è 
#l'equivalente di traceroute
s=f.read()
# usa read per leggere il risultato del comando tracert, una serie di risultati 
#di request/reply ai router che collegano all'host inserito
lines=s.split('\n')
# divide la risposta in righe, creando un'array di stringhe
iplines=lines[4:-3]
# prende solo le righe significative, ovvero quelle contenenti ip

ips =[i.split(' ')[-2].lstrip('[').rstrip(']') for i in iplines]

# delle righe significative, prende solo l'ip, attraverso la separazione delle 
#linee in spazi seleziona il blocco con l'ip e grazie agli strip rimuove eventuali parentesi quadre

coordinates=[]
# crea un array per mantenere le coordinate dei router nel mondo (array di tuple)
for ip in ips:
#itero tra i vari ip
    r=geolite2.lookup(ip)
#compio una lookup per l'ip corrente, ossia ottengo le coordinate del router 
#dato il suo ip
    if r is not None:
#prende le coordinate solo se sono significative
        coordinates.append(r.location)
#inserisce le coordinate del router corrente all'interno dell'array NB sono 
#gestite come tuple
pathlon=[]
#un array per contenere le varie longitudini
pathlat=[]
#un array per contenere le varie latitudini
for i in coordinates:
#per ogni coppia di coordinate riempio i due array
    pathlat.append(i[0])
    pathlon.append(i[1])

gmap = gmplot.GoogleMapPlotter(pathlat[0],pathlon[0],3)
#uso gmplot.GoogleMapPlotter per creare il percorso, dati i valori iniziali 
#dei due array e lo zoom sulla mappa 
gmap.plot(pathlat,pathlon,'cornflowerblue', edge_width=2)
#uso plot per disegnare il percorso sulla mappa, dati gli array, il colore e 
#lo spessore della linea
gmap.draw('map.html')
#disegno su un file html la mappa
os.popen('map.html')
#apro il file per mostrarlo all'utente