from gatenlp import Document
from gatenlp.gateworker import GateWorker
from gatenlp.gateworker import GateWorkerAnnotator
from gatenlp.processing.executor import SerialCorpusExecutor

import json

tagLst = ['Date', 'Location', 'SpaceToken', 
          'Token', 'Person', 'Sentence', 
          'Split', 'Lookup', 'Unknown']

tokenDict = {}

path = "../resources/bbc-sport/xml/001.txt.xml"
gateHomePath = "D:/Programs/GateJava" # hay que meter el path de la carpeta donde esta el exe de GATE
filename = "001.txt.xml"

with open(path, 'r') as file:
    fileRead = file.read() 

    with GateWorker(start= True, gatehome=gateHomePath) as gw:
        corpus = [Document(fileRead)]
        pipeline = GateWorkerAnnotator("../resources/annieApp/bbcSports.xgapp", gw)
        for idx, doc in enumerate(corpus):
            corpus[idx] = pipeline(doc)

        for f in corpus[0].annset():
            if (f.type != 'SpaceToken') and (f.type != 'Token') and (f.type != 'Split'):
                wrd = ""
                for i in range(f.start, f.end):
                    wrd += corpus[0][i]
                
                if (f.type not in tokenDict): 
                    tokenDict[f.type] = {}
                if filename not in tokenDict[f.type]:
                    tokenDict[f.type][filename] = []
                
                tokenDict[f.type][filename].append(wrd)
                print("Type: %s, wrd: %s " % (f.type, wrd))
                print()
            
        corpus[0]        
        gw.close()
        
        with open("tokenDict.json", 'w') as tokenFile:
            json.dump(tokenDict, tokenFile, indent=4)