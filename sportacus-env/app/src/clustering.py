from pandas.core.base import NoNewAttributesMixin
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import glob
import os
import json

docsPath = "../resources/bbc-sport/" 
tokenPath = "tokenDict.json" 

typeLst = {}
wrdsLst = []
title = []
clustersList = []

# for fullFileName in sorted(glob.glob(docsPath + '*txt')):
#     fileName = fullFileName.split(os.sep)[-1]
#     with open(fullFileName, 'r') as file:
#         docsLst.append(file.read())
#         title.append(fileName)
#     print(fileName)
tokenFile = None
with open(tokenPath, 'r') as fileRead:
    tokenFile = json.load(fileRead)
for f in tokenFile:
    for mjtype in tokenFile[f]['majorType']:
        wrdsLst = []
        if (mjtype not in typeLst):
            typeLst[mjtype]={}
        for wrd in tokenFile[f]['majorType'][mjtype]:
            wrdsLst.append(wrd)  
        typeLst[mjtype][f] = wrd
        
    sentence = ' '.join(wrdsLst[-1])
    wrdsLst[-1] = sentence 
    
vectorizer = TfidfVectorizer(stop_words={'english'})

for mjtype in typeLst:
    values = list(typeLst[mjtype].values())
    title = list(typeLst[mjtype].keys())
    
    X = vectorizer.fit_transform(values)

    # Sum_of_squared_distances = []
    # K = range(1, 50)
    # for k in K:
    #     km = KMeans(n_clusters=k, max_iter=200, n_init=10)
    #     km = km.fit(X)
    #     Sum_of_squared_distances.append(km.inertia_)
    # plt.plot(K, Sum_of_squared_distances, 'bx-')
    # plt.xlabel('k')
    # plt.ylabel('Sum_of_squared_distances')
    # plt.title('Elbow Method For Optimal k')
    # plt.show()

    true_k = 43
    if len(values) < true_k:
        true_k = len(values)

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    labels=model.labels_
    wiki_cl=pd.DataFrame(list(zip(title, labels)),columns=['title','cluster'])
    print(wiki_cl.sort_values(by=['cluster']))

    result={'cluster':labels,'wiki':values}
    print(len(result))
    result=pd.DataFrame(result)
    clustersList = []
    for k in range(0,true_k):
        s=result[result.cluster==k]
        text=s['wiki'].str.cat(sep=' ')
        text=text.lower()
        text=' '.join([word for word in text.split()])
        # wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
        # print('Cluster: {}'.format(k))
        # print('Titles')
        titles=wiki_cl[wiki_cl.cluster==k]['title']   
        clustersList.append(titles.to_string(index=False).split())
        # print(titles.to_string(index=False))
    #    plt.figure()
    #    plt.imshow(wordcloud, interpolation="bilinear")
    #    plt.axis("off")
    #    plt.show()
    with open('clusters/cluster_'+ mjtype +'.txt', 'w') as writeF:
        json.dump(clustersList, writeF, indent=4)