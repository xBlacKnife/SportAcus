from gatenlp import Document
from gatenlp.gateworker import GateWorker, GateWorkerAnnotator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from collections import Counter
from operator import itemgetter
import json

# IMPORTS END----------------

''' Devuelve una cantidad num_files de noticias relacionadas con una serie de keywords. 

Archivo que contiene las funciones para recuperar un numero X de noticias relacionadas con las palabras clave de búsqueda
detecta las categorias de GATE de las palabras de búsqueda, 
las localiza en las palabras clave de los clusterings a los que pertenece 
y se contabiliza las veces que aparece el nombre de un archivo entre esos clusters, 
asumiendo que cuantas más veces aparezca, más relevante resultará, devolviendo los X mejores
'''
# PATHS ----------------------
FILES_DIR_PATH = '../resources/annieApp/application-resources/bbc-sport/'

GATE_EXE_PATH = 'D:/Programs/GateJava'
ANNIEAPP_PATH = '../resources/annieApp/application.xgapp' 

MODELS_CL_DIR_PATH = '../resources/clusters/models/' 
WEIGHTS_CL_DIR_PATH = '../resources/clusters/weights/' 

CLUSTERS_PATH = '../resources/clusters/'
# PATHS END ------------------


def get_file_name(keywords, gate_path = None, num_files = 1):
    if gate_path:
        GATE_EXE_PATH = gate_path
        
    keySet = process_wrds_gate(keywords)
    # print(keySet)
    
    estractedFiles = []
    
    for wrd in keySet:
        # print(wrd)
        for t in keySet[wrd]['majorType']:
            cluster = load_relevant_cluster('majorType', t)
            estractedFiles += find_related_files_in_cluster(cluster, wrd)
        # for
        
        for t in keySet[wrd]['minorType']:
            cluster = load_relevant_cluster('minorType', t)
            estractedFiles += find_related_files_in_cluster(cluster, wrd)
            # como las pesonas y apellidos suelen ser bastante unívocos, 
            # se da más peso a los clusters relacionados con nombres de personalidades
            if 'sportperson' in keySet[wrd]['majorType']:
                estractedFiles += find_related_files_in_cluster(cluster, wrd)
            #if
        # for
    # for
    
    topXFile = get_top_X_relevant_files(estractedFiles, num_files = num_files)
    if (topXFile == 0):
        print("ERROR: No files found related to search: %s" % keywords)
    # if
    if num_files == 1:
        return topXFile[0]
    # if
    else:
        return topXFile
    # else
    
# function "get_file_name"

def process_wrds_gate(keywords):
    keySentence = ' '.join(word for word in keywords) # para pasarselo a gate como frase una vez solo en lugar de múltiples envíos
    keyCategories = {} # keeps categories of all words
    
    with GateWorker(start= True, gatehome=GATE_EXE_PATH) as gw:
        pipeline = GateWorkerAnnotator(ANNIEAPP_PATH, gw)
    
        word_tokens = word_tokenize(keySentence)
        filtered_sentence = [w for w in word_tokens if not w.lower() in set(stopwords.words('english'))]
        text = ' '.join([word for word in filtered_sentence])
        corpus = [Document(text)]
        for idx, doc in enumerate(corpus):
            corpus[idx] = pipeline(doc)
        # for
        
        for idx in range(len(corpus)):
            for f in corpus[idx].annset():
                if (f.type == 'Lookup'):
                    wrd = ""
                    for i in range(f.start, f.end):
                        wrd += corpus[0][i]
                    # for
                    
                    if wrd in keywords and wrd not in keyCategories:
                        keyCategories[wrd]= {}
                        keyCategories[wrd]['majorType']= []
                        keyCategories[wrd]['minorType']= []
                    # if
                    
                    if ('majorType' in f.features.names()):
                        
                        if f.features['majorType'] not in keyCategories[wrd]['majorType']:
                            keyCategories[wrd]['majorType'].append(f.features['majorType'])
                        # if
                    # if
                        
                    if ('minorType' in f.features.names()):
                        
                        if f.features['minorType'] not in keyCategories[wrd]['minorType']:
                            keyCategories[wrd]['minorType'].append(f.features['minorType'])
                        # if
                    # if              
                # if
            # for
        # for
        
        gw.close()  
    return keyCategories
# function "process_wrds_gate"

def load_relevant_cluster(mType, mmType):
    with open(CLUSTERS_PATH + mType + '/' + mmType + '_cluster.json', 'r') as readClFile:
        cluster = json.load(readClFile)
    return cluster
# function "load_relevant_cluster"

def find_related_files_in_cluster(cluster, wrd):
    wrd = wrd.lower()
    for c in cluster:
        if wrd in c['keywords']:
            return c['file']
    return []
# function "find_related_files_in_cluster"

def get_top_X_relevant_files(filesLst, num_files = 5):
    elemCount = Counter(filesLst)
    sortedDict = sorted(elemCount.items(), key = itemgetter(1), reverse = True)
    maxCount = dict(sortedDict[:min([len(sortedDict), num_files])])
    if len(maxCount) > 0:
        return list(maxCount.keys())
    else:
        return 0
# function "get_top_relevant_files"
