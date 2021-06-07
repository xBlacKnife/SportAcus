from gatenlp import Document
from gatenlp.gateworker import GateWorker, GateWorkerAnnotator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import json
import pickle
# IMPORTS END----------------

''' Añade nueva noticia a la base de datos tras procesarla

Archivo que contiene las funciones para clasificar y añadir a los clusters una nueva noticia.
'''
# PATHS ----------------------
FILES_DIR_PATH = '../resources/annieApp/application-resources/bbc-sport/'

GATE_EXE_PATH = 'D:/Programs/GateJava'
ANNIEAPP_PATH = '../resources/annieApp/application.xgapp' 

MODELS_CL_DIR_PATH = '../resources/clusters/models/' 
WEIGHTS_CL_DIR_PATH = '../resources/clusters/weights/' 

CLUSTERS_PATH = '../resources/clusters/'
# PATHS END ------------------

def set_new_file(file_name, gate_path=None):
    ''' Recibe un nombre de noticia generada y lo añade a los clusters correspondientes
        Comunicacion con newManager.py
        Return 1 si correcto, 0 si fallo
    '''
    if gate_path:
        GATE_EXE_PATH = gate_path
    try:  
        with open(FILES_DIR_PATH + file_name, 'r') as readFile:
            newsText = readFile.read()
            gate_process(file_name, newsText)
            return 1
    except:
        return 0
        
# function "set_new_file"

def gate_process(file_name, newsText):
        ''' Recoge el archivo, lo procesa con GATE
            Genera un archivo tokens con las distintas palabras de cada categoría
        '''
        tokensInFile = {}
        tokensInFile['majorType'] = {}
        tokensInFile['minorType'] = {}
        with GateWorker(start= True, gatehome=GATE_EXE_PATH) as gw:
            pipeline = GateWorkerAnnotator(ANNIEAPP_PATH, gw)
        
            word_tokens = word_tokenize(newsText)
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

        cluster_label(file_name, tokensInFile) # lo casifica en los clusters correspondientes
    
# function "gate_process"
    
def cluster_label(file_name, tokens):
    '''clasifica en los clusters
    '''
    update_clustering(file_name, tokens, 'majorType')
    update_clustering(file_name, tokens, 'minorType')
    
# function "cluster_label"

def get_all_types(tokensDict, mType):
    ''' Crea una lista con todas las categorias 
        con las que está relacionado el archivo
    '''
    mTypesLst = []
    for f in tokensDict:
        for t in tokensDict[mType]:
            mTypesLst.append(t)
            
    return mTypesLst
# function "get_all_types"

def generate_documents_of_type(tokensDict, mType, mmType):
    ''' 
        Busca el tipo mmType de cada archivo y une todas las palabras de ese tipo en una única frase, 
        ya que serán tratados como documentos completos por separado
    '''
    docs = []
        
    sentence = ''    
    if mmType in tokensDict[mType]:               
        for wrd in tokensDict[mType][mmType]:
            sentence = sentence + wrd + ' '        
        docs.append(sentence)
        
    return docs
# function "generate_documents_of_type"

def load_relevant_cluster(mType, mmType):
    ''' carga los clusters (modelo, cluster data y pesos TFIDF) 
        de la categoría mType (major, minor) mmType
    '''
    
    model = pickle.load(MODELS_CL_DIR_PATH + mmType + '_model.pkl')
    with open(CLUSTERS_PATH + mType + '/' + mmType + '_cluster.json', 'r') as readClFile:
        cluster = json.load(readClFile)
        
    weights = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(WEIGHTS_CL_DIR_PATH + mmType + "_feature.pkl", "rb")))
    
    return model, cluster, weights

# function "load_relevant_cluster"

def predict_cluster_and_add(file_name, sentence, model, cluster, weights):
    ''' Predice el conjunto al que pertenece el nuevo archivo 
        devuelve la prediccion y el cluster modificado (con el nuevo archivo añadido)
    '''
    
    vectorizer = TfidfTransformer()
    Y = vectorizer.fit_transform(weights.fit_transform(sentence))
    prediction = model.predict(Y)[0]
    
    if prediction < len(cluster):
        print(cluster[prediction]['keywords'])
        if file_name not in cluster[prediction]['file']:
            cluster[prediction]['file'].append(file_name)
    else: 
        prediction = -1
        
    return prediction, cluster

# function "predict_cluster_and_save"

def update_clustering(file_name, tokens, token_type='majorType'):
    ''' Por cada categoría, carga el cluster relevante, 
        predice la posición del archivo nuevo, 
        añade el nombre de archivo al cluster data y lo guarda
    '''
    
    allTypes = get_all_types(tokens, token_type)
    for t in allTypes:
        sentence = generate_documents_of_type(tokens, token_type, t)
        model, cluster, weights = load_relevant_cluster(token_type, t)
        prediction, cluster = predict_cluster_and_add(file_name, sentence, model, cluster, weights)
        print("Prediction %s: %s" % (t, prediction))
        print()
        if prediction != -1:
            with open(CLUSTERS_PATH + token_type + '/' + t + '_cluster.json', 'w') as wrFile:
                json.dump(cluster, wrFile, indent=4)
        else:
            raise Exception("Predicted -1. Cluster error, something went wrong.")
    
    print("Database correctly updated.")
# function "get_words_from_tokens"