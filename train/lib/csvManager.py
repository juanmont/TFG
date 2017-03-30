# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:14:50 2016

@author: slide22
"""

import pandas
import os
import json

"""
Read all CSV in a specific folder and create a new one based on the condition
dictionary

Args:
    sourceFolder (str): csv source folder. It have to ends in /
    destinationPath (str): new csv filename
    cond (dict): dictionary with the filter conditios
                 - startDate (int): the date on which begins csv. Format: YYYYMMDD
                 - endDate (int): the date on which ends csv. Format: YYYYMMDD
                 - startHour (int): the hour on which begins csv. Format: HHMM
                 - endHour (int): the hout on which ends csv. Format: HHMM
                 - ubication (list): list with the ubications of the csv
"""
def createCSVWithConditions(sourceFolder, destinationPath=None, cond = dict(), verbose = True):
   
    relativePath = os.path.dirname(__file__)
    sourceFolder = os.path.join(relativePath, sourceFolder)

    from os import listdir

    # dictionary with the default conditions
    conditions = {'dateStart': 0,
                  'dateEnd': None,
                  'hourStart': 100,
                  'hourEnd': 2400,
                  'ubication': list()
                  }
    
    # merge the conditions dict with the parameters cond
    conditions.update(cond)
    
    #filter data by date
    if conditions['dateEnd'] != None:
        csvFiles = [f for f in listdir(sourceFolder) \
                      if f[:8].isdigit() \
                      and int(f[:8]) >= conditions['dateStart'] \
                      and int(f[:8]) <= conditions['dateEnd']]
    else:
        csvFiles = [f for f in listdir(sourceFolder) \
                      if f[:8].isdigit() \
                      and int(f[:8]) >= conditions['dateStart']]
    
    if len(csvFiles) == 0:
        print 'No csv Files found'
        return None

    csvFiles = sorted(csvFiles)
    
    origColumns = ['Codigo', 'Fecha (AAAA-MM-DD)', 'Hora (HHMM)','Temperatura (oC)', 'Humedad relativa (%)', 'Radiacion (W/m2)']

    columns = ['codigo', 'fecha', 'hora', 'temperatura', 'humedad', 'radiacion']

    df = pandas.DataFrame(columns = columns)

    # loading the files
    i = 0
    for f in csvFiles:
        
        i += 1
        if verbose:
            print '\rReading '+ f + '('+ str(i) +'/'+ str(len(csvFiles)) +')'
            
        dfAux = pandas.read_csv(sourceFolder + f, ';', usecols=origColumns)

        dfAux.columns = columns

        df = df.append(dfAux)
   
    #sort values
    df = df.sort_values(by=['codigo', 'fecha', 'hora'], ascending=True)                         
      
    #patching the 2015-06-06 csv
    df['fecha'] = df['fecha'].str.replace('-', '').astype(float)

    df.loc[df['fecha'] == 20120406, 'fecha'] = 20150206
    df.loc[df['fecha'] == 20120408, 'fecha'] = 20150208
    df.loc[df['fecha'] == 20120511, 'fecha'] = 20150118
    df.loc[df['fecha'] == 20120526, 'fecha'] = 20150622
    df.loc[df['fecha'] == 20120607, 'fecha'] = 20150409
    df.loc[df['fecha'] == 20130429, 'fecha'] = 20150329
    df.loc[df['fecha'] == 20120714, 'fecha'] = 20150516
    df.loc[df['fecha'] == 20130502, 'fecha'] = 20150401
    df.loc[df['fecha'] == 20130525, 'fecha'] = 20150424
    df.loc[df['fecha'] == 20130612, 'fecha'] = 20150512
    df.loc[df['fecha'] == 20140129, 'fecha'] = 20150111
    df.loc[df['fecha'] == 20140624, 'fecha'] = 20150606
    df.loc[df['fecha'] == 20140624, 'fecha'] = 20150606
    df.loc[df['fecha'] == 20140626, 'fecha'] = 20150608
    df.loc[df['fecha'] == 20140628, 'fecha'] = 20150610
   
    for i, codigo in enumerate(df['codigo'].unique()):
        df.loc[df['codigo'] == codigo, 'codigo'] = i

    #filter the data by hour and ubication
    if len(conditions['ubication']) > 0:
      
        df = pandas.DataFrame(df[(df['hora'] >= conditions['hourStart']) \
                               & (df['hora'] <= conditions['hourEnd']) \
                               & (df['Ubicacion'].isin(conditions['ubication']))])
    else:
        df = pandas.DataFrame(df[(df['hora'] >= conditions['hourStart']) \
                               & (df['hora'] <= conditions['hourEnd'])])
  
    normpath = sourceFolder + '../reverseNorm/'+ str(conditions['hourStart']) + str(conditions['hourEnd']) + '.json'

    df, normValues = normalizeCSV(df)

    with open(normpath, 'w') as outfile:
        json.dump(normValues, outfile)

    if destinationPath != None:
        df.to_csv(destinationPath, index = False)
        
    return df
        
#
#Normalize a pandas column
#
def normalize(col):
    return (col - col.mean()) / (col.max() - col.min()), [col.mean(), col.max(), col.min()]

#
#normalize dataframe values and get the control values to restore the data
#
def normalizeCSV(df):
    
    normValues = dict()
    
    for column in list(df):
        df[column], normValues[column] = normalize(df[column])
    
    return df, normValues

def deNormalizeCSV(df):
    pass
    
if __name__ == "__main__":

    conditions = dict()
    conditions['dateStart'] = 20010101
    conditions['dateEnd'] = 20020101
    #conditions['hourStart'] = 100
    #conditions['hourEnd'] = 200
    conditions['ubication'] = ['Nava de Arevalo']
    
    createCSVWithConditions('../data/csvFiles/', '../data/filteredFile.csv', conditions)
