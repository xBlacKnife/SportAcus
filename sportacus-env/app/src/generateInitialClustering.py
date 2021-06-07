from typing import ValuesView
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.cluster import KMeans
import pickle
import json

# IMPORTS END----------------
''' Genera configuración de clusters inicial. 

Archivo que contiene las funciones para generar los clusters partiendo de los archivos iniciales.
Genera los clusters mediante algoritmo de Kmeans, 
guardando lo necesario para predecir posiciones de nuevos archivos (modelo y pesos TFIDF)
así como los archivos pertenecientes a cada cluster y sus palabras más representativas, separados por temática
Solo es necesario lanzarlo una vez, dado que se guarda lo necesario para su reconstruccion
'''
# PATHS ----------------------
TOKENS_FILE_NAME = "tokenDict.json"
MODELS_PATH = '../resources/clusters/models/'
WEIGHTS_PATH = '../resources/clusters/weights/'
MAJOR_PATH = '../resources/clusters/majorType/'
MINOR_PATH = '../resources/clusters/minorType/'
# PATHS END ------------------

def do_kmeans(documents, vectorizer, numClusters = 10, numKeywords = 30):
    ''' realiza el algoritmo de Kmeans para los documentos en docs
        En este caso, las palabras relevantes a la categoria concatenadas
        
        Ej:
            Frase = Nadal played yesterday's match perfectly
            Palabras de tenis = ['Nadal', 'match', 'played']
            doc = Nadal match played
            
        para cada categoria detectada
    '''
    
    print('Docs Len: %s' % len(documents))
    X = vectorizer.fit_transform(documents)   
    
    true_k = min([X.getnnz(), numClusters, len(documents)])
    print("Cluster Num: %s" % true_k)
    
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    # print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    keywordsClusters = []
    for i in range(true_k):
        # print("Cluster %d:" % i),
        keywordsClusters.append([])
        
        for ind in order_centroids[i, :numKeywords]:
            keywordsClusters[-1].append(terms[ind])
   
        # print(keywordsClusters[-1])
    
    return model, keywordsClusters, model.labels_

def do_predictions(document, model):
    ''' Predice el cluster al que pertenece un nuevo documento
    '''
    
    vectorizer = TfidfVectorizer(stop_words='english')
    Y = vectorizer.transform([document])
    prediction = model.predict(Y)
    
    print("Prediction: %s " % prediction)
    
    return prediction

def get_all_types(tokensDict, mType):
    ''' Genera una lista con todas las categorias a las que pertenece 
        el archivo X tras haber sido procesado por GATE 
    '''
    
    mTypesLst = []
    for f in tokensDict:
        for t in tokensDict[f][mType]:
            mTypesLst.append(t)
            
    return mTypesLst
            
def generate_documents_of_type(tokensDict, mType, mmType):
    ''' 
        Busca el tipo mmType de cada archivo y une todas las palabras de ese tipo en una única frase, 
        ya que serán tratados como documentos completos por separado
        
        Ej:
            Frase = Nadal played yesterday's match perfectly
            Palabras de tenis = ['Nadal', 'match', 'played']
            docTennis = Nadal match played
    '''
    docs = []
    docsNames = []
    for f in tokensDict:
        sentence = ''    
        if mmType in tokensDict[f][mType]:               
            for wrd in tokensDict[f][mType][mmType]:
                sentence = sentence + wrd + ' '        
            docs.append(sentence)
            docsNames.append(f)
        
    return docs, docsNames
            
def generate_all_documents():
    ''' Para todo el archivo 'TOKENS_FILE_NAME' (que contiene todo el procesado inicial con GATE)
        genera los 'documentos' separados por categorias
    '''
    mayorTypes = None
    minorTypes = None
    
    with open(TOKENS_FILE_NAME, 'r') as fileRead:
        tokensDict = json.load(fileRead)
        
        # crea lista con todos los posibles tipos
        mayorTypes = get_all_types(tokensDict, 'majorType')
        minorTypes = get_all_types(tokensDict, 'minorType')
        
        # por cada tipo mayor, genera un dict {tipo1: [palabras1, palabras2]} y otro dict {tipo1: [file1, file2]}
        # alineados, la frase 1 pertenece al archivo guardado como file1
        mayorDocs = {}
        mayorDocsNames = {}
        for t in mayorTypes:
            mayorDocs[t], mayorDocsNames[t] = generate_documents_of_type(tokensDict, 'majorType', t)
        
        # idem tipo mayor, con los tipos menores (subtipos)
        minorDocs = {}
        minorDocsNames = {}
        for t in minorTypes:
            minorDocs[t], minorDocsNames[t] = generate_documents_of_type(tokensDict, 'minorType', t)      

    return mayorDocs, mayorDocsNames, minorDocs, minorDocsNames

def save_clusters(mType, numClusters, keywords, labels, docNames, path):
    ''' Recibe los datos de un cluster (keywords y archivos pertenecientes a cada cluster)
        y los guarda como archivos
    '''
    clusters = [None] * numClusters
    for i in range(len(labels)):
        if clusters[labels[i]] == None:
            clusters[labels[i]] = {}
            clusters[labels[i]]['keywords'] = keywords[labels[i]]
            clusters[labels[i]]['file'] = []
            
        clusters[labels[i]]['file'].append(docNames[i])

    with open(path + mType + '_cluster.json', 'w') as wrFile:
        json.dump(clusters, wrFile, indent=4)

def generate_all_models():
    ''' Genera los modelos y clusters para todos los archivos procesados en TOKENS_FILE_NAME,
        guardando lo necesario para la reconstruccion de los mismos
    '''
    majorDocs, majorDocsFiles, minorDocs, minorDocsNames = generate_all_documents()

    for t in majorDocs:
        vectorizer = CountVectorizer(decode_error="replace", stop_words='english')
        # vectorizer = TfidfVectorizer(stop_words='english')
        # print(t)
        model, keys, labels = do_kmeans(majorDocs[t], vectorizer)
        numClusters = max(labels) + 1
        # print("Num Clusters: %s" % numClusters)
        save_clusters(t, numClusters, keys, labels, majorDocsFiles[t], MAJOR_PATH)
        pickle.dump(model, MODELS_PATH + t +'_model.pkl')
        
        pickle.dump(vectorizer.vocabulary_,open(WEIGHTS_PATH + t + "_feature.pkl","wb"))
        # print()
        
    for t in minorDocs:
        vectorizer = CountVectorizer(decode_error="replace", stop_words='english')
        # vectorizer = TfidfVectorizer(stop_words='english')
        model, keys, labels = do_kmeans(minorDocs[t], vectorizer)
        numClusters = max(labels) + 1
        save_clusters(t, numClusters, keys, labels, minorDocsNames[t], MINOR_PATH)
        pickle.dump(model, MODELS_PATH + t +'_model.pkl')
        pickle.dump(vectorizer.vocabulary_,open(WEIGHTS_PATH + t + "_feature.pkl","wb"))

generate_all_models()