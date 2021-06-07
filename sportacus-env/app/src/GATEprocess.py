from gatenlp import Document
from gatenlp.gateworker import GateWorker
from gatenlp.gateworker import GateWorkerAnnotator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import glob
import json
# IMPORTS END----------------
''' Genera el procesado inicial con GATE de los archivos iniciales. 

Archivo que se encarga de procesar todas las noticias iniciales a través de GATE, 
guardando en tokenDict un diccionario con las palabras de los archivos separadas por categoría de GATE
'''
# PATHS ----------------------
tokenDict = {}

PATH = "../resources/annieApp/application-resources/bbc-sport/"
GATE_EXE_PATH = 'D:/Programs/GateJava' # hay que meter el path de la carpeta donde esta el exe de GATE
ANNIEAPP_PATH = '../resources/annieApp/application.xgapp' 
# PATHS END ------------------


stop_words = set(stopwords.words('english'))
    
with GateWorker(start= True, gatehome=GATE_EXE_PATH) as gw:
    pipeline = GateWorkerAnnotator(ANNIEAPP_PATH, gw)
    
    for fileName in glob.glob(PATH + '*.txt'):
        
        cleanFName = fileName.split('/')[-1].split('\\')[-1]
        tokenDict[cleanFName] = {}
        tokenDict[cleanFName]['majorType'] = {}
        tokenDict[cleanFName]['minorType'] = {}
        
        with open(fileName, 'r') as file:
            fileRead = file.read() 
            
        word_tokens = word_tokenize(fileRead)
        filtered_text = [w for w in word_tokens if not w.lower() in stop_words]
        text=' '.join([word for word in filtered_text])
        
        print("FILE: %s" % cleanFName )
        corpus = [Document(text)]
        
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