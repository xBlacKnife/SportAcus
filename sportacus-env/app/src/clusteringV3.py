from typing import ValuesView
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.externals import joblib
import json

tokensFilePath = "tokenDict.json"
MODELS_PATH = '../resources/clusters/models/'
MAJOR_PATH = '../resources/clusters/majorType/'
MINOR_PATH = '../resources/clusters/minorType/'

def do_kmeans(documents, vectorizer, numClusters = 10, numKeywords = 10):
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
    vectorizer = TfidfVectorizer(stop_words='english')
    Y = vectorizer.transform([document])
    prediction = model.predict(Y)
    
    print("Prediction: %s " % prediction)
    
    return prediction

def get_all_types(tokensDict, mType):
    mTypesLst = []
    for f in tokensDict:
        for t in tokensDict[f][mType]:
            mTypesLst.append(t)
            
    return mTypesLst
            
def generate_documents_of_type(tokensDict, mType, mmType):
    ''' 
        Busca el tipo mmType de cada archivo y une todas las palabras de ese tipo en una única frase, 
        ya que serán tratados como documentos completos por separado
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
    
    mayorTypes = None
    minorTypes = None
    
    with open(tokensFilePath, 'r') as fileRead:
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
    clusters = [None] * numClusters
    for i in range(len(labels)):
        if clusters[labels[i]] == None:
            clusters[labels[i]] = {}
            clusters[labels[i]]['keywords'] = keywords[labels[i]]
            clusters[labels[i]]['file'] = []
            
        clusters[labels[i]]['file'].append(docNames[i])
        
    # print("CLUSTERS:")
    # print(clusters)
    # print()
    # print("DOCS:")
    # print(docNames)
    # print()

    with open(path + mType + '_cluster.json', 'w') as wrFile:
        json.dump(clusters, wrFile, indent=4)

def generate_all_models():
    majorDocs, majorDocsFiles, minorDocs, minorDocsNames = generate_all_documents()

    for t in majorDocs:
        vectorizer = TfidfVectorizer(stop_words='english')
        # print(t)
        model, keys, labels = do_kmeans(majorDocs[t], vectorizer)
        numClusters = max(labels) + 1
        # print("Num Clusters: %s" % numClusters)
        save_clusters(t, numClusters, keys, labels, majorDocsFiles[t], MAJOR_PATH)
        joblib.dump(model, MODELS_PATH + t +'_model.pkl')
        # print()
        
    for t in minorDocs:
        vectorizer = TfidfVectorizer(stop_words='english')
        model, keys, labels = do_kmeans(minorDocs[t], vectorizer)
        numClusters = max(labels) + 1
        save_clusters(t, numClusters, keys, labels, minorDocsNames[t], MINOR_PATH)
        joblib.dump(model, MODELS_PATH + t +'_model.pkl')

def generate_document_all_types_from_file (fileName):
    
    pass




# for i in docsToPred2:
#     do_predictions(i, model)    
# print(docs[0])
# print(docsN[0])