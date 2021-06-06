from operator import add
from typing import Text
from gatenlp import Document
from gatenlp.gateworker import GateWorker, GateWorkerAnnotator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from pandas.core.base import NoNewAttributesMixin
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import pandas as pd
import json

#-- K MEANS -----------------------
class AddNewFile:
    TOKEN_DICT_FILE = "tokenDict.json"
    
    def __init__(self, file_name, 
                 files_dir_path = '../resources/annieApp/application-resources/bbc-sport/',
                 gate_exe_path = 'D:/Programs/GateJava', 
                 annie_app_file = '../resources/annieApp/application.xgapp', 
                 models_path = '../resources/clusters/models/', clusters_path = '../resources/clusters/'):
        
        self.file_name = file_name
        self.files_dir_path = files_dir_path
        self.gate_exe_path = gate_exe_path
        self.annie_app_file = annie_app_file
        self.models_path = models_path
        self.clusters_path = clusters_path
        self.stop_words = set(stopwords.words('english'))
        
        with open(files_dir_path + file_name, 'r') as newF:
            text = newF.read()
            self.gate_process(text)
        
    # function "__init__"

    def gate_process(self, newsText):
        '''
        '''
        tokensInFile = {}
        tokensInFile['majorType'] = {}
        tokensInFile['minorType'] = {}
        with GateWorker(start= True, gatehome=self.gate_exe_path) as gw:
            pipeline = GateWorkerAnnotator(self.annie_app_file, gw)
        
            word_tokens = word_tokenize(newsText)
            filtered_sentence = [w for w in word_tokens if not w.lower() in self.stop_words]
            text=' '.join([word for word in filtered_sentence])
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
                    if ('majorType' in f.features.names()):
                        if f.features['majorType'] not in tokensInFile['majorType']:
                            tokensInFile['majorType'][f.features['majorType']] = []
                        # if
                        tokensInFile['majorType'][f.features['majorType']].append(wrd)
                    # if
                        
                    if ('minorType' in f.features.names()):
                        if f.features['minorType'] not in tokensInFile['minorType']:
                            tokensInFile['minorType'][f.features['minorType']] = []
                        # if
                        tokensInFile['minorType'][f.features['minorType']].append(wrd)
                    # if                 
                # if
            # for
        # for
        
        gw.close()  
        
        self.cluster_label(tokensInFile)  
    
    # function "gate_process"
    
    def cluster_label(self, tokens):
        self.update_clustering(tokens, 'majorType')
        # self.update_clustering(tokens, 'minorTypes')
        
    # function "cluster_label"
      
    def update_clustering(self, tokens, token_type='majorType'):
        vectorizer = TfidfVectorizer(stop_words={'english'})
        for mjtype in tokens[token_type]:
            
            loaded_model = joblib.load(self.models_path + mjtype + 'model.pkl')

            values = tokens[token_type][mjtype]
            print('########## COSO : %s ' % values)
            
            X = vectorizer.fit_transform(values)
            cluster_num = loaded_model.predict(X)
            
            print('Text: %s, type: %s to cluster %s' % (self.file_name, mjtype, cluster_num))
            
            with open(self.clusters_path + token_type + '/cluster_' + mjtype + '.txt', 'r+') as rwFile:
                clusterFile = json.load(rwFile)
                clusterFile[cluster_num]['files'].append(self.file_name)
            
    # function "get_words_from_tokens"
    
# class "AddNewFile"

addF = AddNewFile('000.txt')
