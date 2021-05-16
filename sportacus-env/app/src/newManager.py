import yake
import json
from os import walk

# El primer elemento que hemos introducido nosotros es el "512.txt"
def saveNew(new_to_save):
    
    _, _, filenames = next(walk("../resources/bbc-sport/"))
    
    last_file = filenames[len(filenames) - 1].replace('.txt', '')
    
    file_name = str((int(last_file) + 1)) + '.txt'
    # LEONOR -----> SET_NEW_FILE(file_name)
    
    with open("../resources/bbc-sport/" + file_name, 'w') as f:
        f.write(new_to_save["Title"])
        f.write("\n\n")
        f.write(new_to_save["Text"])

def getKeywords(search, importance):
    kw_extractor = yake.KeywordExtractor()
    custom_kw_extractor = yake.KeywordExtractor(
        lan="en", 
        n=1, # Numero de palabras que puede tener una keyword
        dedupLim=importance, # Si es mas pequeño, se queda con menos palabras pero mejores
        top=20, # Numero maximo que puede alcanzar la lista de keywords
        features=None) # Ni idea
    
    # Esto te da una lista de keywords con un valor por cada una
    # que parece ser la importancia que tiene
    keywords_aux = custom_kw_extractor.extract_keywords(search)
    
    # Le quita ese valor y solo se queda con las palabras
    keywords = [word[0] for word in keywords_aux]
    
    return keywords

def getNew(filename):  
    with open('../resources/bbc-sport/' + filename.rstrip("\n")) as f:
        new_lines = f.readlines()
        
    new_info = {
        "Title": new_lines[0],
        "Text": ' '.join(new_lines[1:])
    }
    
    return new_info

def getUserSearchNew(search):
    keywords = getKeywords(search, 0.2)
    
    # LEONOR -----> new_filename = DAME_EL_NOMBRE_DEL_ARCHIVO(keywords)
    new_filename = "001.txt"
    
    new_info = {
        "new":{},
        "previous":[]
    }
    
    new_info["new"] = getNew(new_filename)
    new_info["previous"] = getLastNews(new_filename)
    
    return json.dumps(new_info)



def getRelatedNews(search):
    news_list = []
    keywords = getKeywords(search, 0.9)
    
    # LEONOR -----> news_filename = DAME_LA_LISTA_DE_NOMBRES_DE_ARCHIVOS(keywords)
    new_filenames = ["002.txt", "003.txt", "004.txt"]
    
    for file in new_filenames:
        news_list.append(getNew(file))
            
    return json.dumps(news_list)



def getLastNews(new_filename): 
    searchListAux = None
    news_list = []
    
    f = open('../data/LastSearches.txt', "r")
    searchListAux = f.readlines()
    f.close()
        
    for search in searchListAux:
        news_list.append(getNew(search))
        
    searchListAux.pop(0)
    searchListAux.append(new_filename)
    searchList = [s.rstrip("\n") for s in searchListAux]
    
    f = open('../data/LastSearches.txt', "w")
    for element in searchList:
        f.write(element + "\n")
    f.close()
    
    return news_list
    
    