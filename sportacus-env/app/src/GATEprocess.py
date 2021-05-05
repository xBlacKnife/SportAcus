from gatenlp import Document
from gatenlp.gateworker import GateWorker
from gatenlp.gateworker import GateWorkerAnnotator
from gatenlp.processing.executor import SerialCorpusExecutor

tagLst = ['Date', 'Location', 'SpaceToken', 
          'Token', 'Person', 'Sentence', 
          'Split', 'Lookup', 'Unknown']


path = "../resources/001.txt.xml"
gateHomePath = "D:/Programs/GateJava" # hay que meter el path de la carpeta donde esta el exe de GATE

with open(path, 'r') as file:
    fileRead = file.read() 


    with GateWorker(start= True, gatehome=gateHomePath) as gw:
        corpus = [Document(fileRead)]
        pipeline = GateWorkerAnnotator("../resources/annieApp/bbcSports.xgapp", gw)
        for idx, doc in enumerate(corpus):
            corpus[idx] = pipeline(doc)

        for f in corpus[0].annset():
            if (f.type != 'SpaceToken') and (f.type != 'Token'):
                wrd = ""
                for i in range(f.start, f.end):
                    wrd += corpus[0][i]
                print("Type: %s, wrd: %s " % (f.type, wrd))
                print()
            
            
        print(corpus[0].features.get('Original markups'))
        corpus[0]
        gw.close()