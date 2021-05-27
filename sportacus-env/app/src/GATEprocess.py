from gatenlp import Document
from gatenlp.gateworker import GateWorker
from gatenlp.gateworker import GateWorkerAnnotator
from gatenlp.processing.executor import SerialCorpusExecutor

import glob
import json

tagLst = ['Date', 'Location', 'SpaceToken', 
          'Token', 'Person', 'Sentence', 
          'Split', 'Lookup', 'Unknown']

tokenDict = {}

path = "../resources/annieApp/application-resources/bbc-sport/xml/"
gateHomePath = "D:/Programs/GateJava" # hay que meter el path de la carpeta donde esta el exe de GATE
# filename = "001.txt.xml"

    
with GateWorker(start= True, gatehome=gateHomePath) as gw:
    pipeline = GateWorkerAnnotator("../resources/annieApp/application.xgapp", gw)
    for fileName in glob.glob(path + '*.xml'):
        
        cleanFName = fileName.split('/')[-1].split('\\')[-1]
        tokenDict[cleanFName] = {}
        tokenDict[cleanFName]['majorType'] = {}
        tokenDict[cleanFName]['minorType'] = {}
        
        with open(fileName, 'r') as file:
            fileRead = file.read() 
        
        print("FILE: %s" % cleanFName )
        corpus = [Document(fileRead)]
        
        for idx, doc in enumerate(corpus):
            corpus[idx] = pipeline(doc)
            
        for idx in range(len(corpus)):
            for f in corpus[idx].annset():
                #if (f.type != 'SpaceToken') and (f.type != 'Token') and (f.type != 'Split'):
                if (f.type == 'Lookup'):
                    wrd = ""
                    for i in range(f.start, f.end):
                        wrd += corpus[0][i]
                    
                    if ('majorType' in f.features.names()):
                        if f.features['majorType'] not in tokenDict[cleanFName]['majorType']:
                            tokenDict[cleanFName]['majorType'][f.features['majorType']] = []
                        
                        tokenDict[cleanFName]['majorType'][f.features['majorType']].append(wrd)
                        
                        
                    if ('minorType' in f.features.names()):
                        if f.features['minorType'] not in tokenDict[cleanFName]['minorType']:
                            tokenDict[cleanFName]['minorType'][f.features['minorType']] = []
                        
                        tokenDict[cleanFName]['minorType'][f.features['minorType']].append(wrd)                 
            
             
gw.close()
        
with open("tokenDict.json", 'w') as tokenFile:
    json.dump(tokenDict, tokenFile, indent=4)