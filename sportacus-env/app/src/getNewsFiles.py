from numpy.lib.npyio import load
from gatenlp import Document
from gatenlp.gateworker import GateWorker, GateWorkerAnnotator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib
import json
import pickle

# IMPORTS END----------------

# PATHS ----------------------
FILES_DIR_PATH = '../resources/annieApp/application-resources/bbc-sport/'

GATE_EXE_PATH = 'D:/Programs/GateJava'
ANNIEAPP_PATH = '../resources/annieApp/application.xgapp' 

MODELS_CL_DIR_PATH = '../resources/clusters/models/' 
WEIGHTS_CL_DIR_PATH = '../resources/clusters/weights/' 

CLUSTERS_PATH = '../resources/clusters/'
# PATHS END ------------------


def get_file_name(keywords, gate_path = None):
    if gate_path:
        GATE_EXE_PATH = gate_path
        
    keySet = process_wrds_gate(keywords)
    print(keySet)
    
    for wrd in keySet:
        # NOTA : este se añaden todos en una variable y el otra solo la union de files, ir descartando 
        for t in keySet[wrd]['majorType']:
            cluster = load_relevant_cluster('majorType', t)
            find_related_files_in_cluster(cluster, wrd)
        
        # cribado más fino
        for t in keySet[wrd]['minorType']:
            cluster = load_relevant_cluster('minorType', t)
            find_related_files_in_cluster(cluster, wrd)
            
    return "001.txt"
    

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
                    
                    if wrd in keywords and wrd not in keyCategories:
                        keyCategories[wrd]= {}
                        keyCategories[wrd]['majorType']= []
                        keyCategories[wrd]['minorType']= []
                    # for
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


def load_relevant_cluster(mType, mmType):
    with open(CLUSTERS_PATH + mType + '/' + mmType + '_cluster.json', 'r') as readClFile:
        cluster = json.load(readClFile)
    return cluster

def find_related_files_in_cluster(cluster, wrd):
    for c in cluster:
        if wrd in c['keywords']:
            return c['files']
    return []

get_file_name(['Wimbledon', 'Nadal', 'tennis', 'set'])