# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:09:47 2016

@author: slide22
"""

from infoRiegoData import dataManager as dM
from infoRiegoData import csvManager as cM

dM.downloadData(2001, 2002, 'data/zipFiles/')
dM.uncompressData('data/zipFiles/', 'data/csvFiles/')
dM.correctCharacters('data/csvFiles/')

conditions = dict()
conditions['dateStart'] = 20010101
conditions['dateEnd'] = 20010102
conditions['hourStart'] = 100
conditions['hourEnd'] = 200
conditions['ubication'] = ['Nava de Arevalo', 'Miranda de Ebro']

cM.createCSVWithConditions('data/csvFiles/', 'data/filteredFile.csv', conditions)

