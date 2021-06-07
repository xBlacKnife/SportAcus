import yake
import json
from os import walk

from addNew import set_new_file
from getNewsFiles import get_file_name

DIRNAME = "../resources/annieApp/application-resources/bbc-sport/"
GATEEXEPATH = 'D:/Programs/GateJava'

# El primer elemento que hemos introducido nosotros es el "512.txt"
def saveNew(new_to_save):
    ''' Guarda la nueva noticia en un archivo de TXT nuevo.
    '''
    
    # Recoge la lista de nombres de los archivos que hay localmente
    # Los nombres de los archivos estan enumerados y en un principio van
    # del 1 al 511
    _, _, filenames = next(walk(DIRNAME))
    
    # Coge el nombre del ultimo archivo almacenado
    last_file = filenames[len(filenames) - 1].replace('.txt', '')
    
    # Nombre del archivo que se va a crear
    file_name = str((int(last_file) + 1)) + '.txt'
    
    # Se escribe la noticia en dicho archivo y se almacena
    with open(DIRNAME + file_name, 'w') as f:
        f.write(new_to_save["Title"])
        f.write("\n\n")
        f.write(new_to_save["Text"])
        
    # Se analiza esta nueva noticia para realizar una agrupacion y extraer keywords
    # Esto devuelve:
    #  - "1" si se ha podido añadir
    #  - "0" si no se ha podido añadir
    return set_new_file(file_name, gate_path = GATEEXEPATH)

# function "saveNew"



def getKeywords(search, lim):
    ''' Extrae las palabras mas importantes (keywords) de un texto dado.
    Ademas, el parametro "lim" ajusta esta busqueda dando mas o menos libertad
    a la eleccion de estas keywords. En el caso de que este parametro sea lo mas
    cercano a 0, la seleccion de keywords es mas exhaustiva que si fuera cercano a 1.
    Este parametro es importante para la busqueda de la noticia concreta y las noticias
    relevantes. Donde para el primero el parametro sea grande y nos quedaremos con un mayor numero
    de keywords que deben coincidir y para el segundo sera mas pequeño para que nos devuelva
    menor keywords y asi tener mas posibilidades de noticias.
    '''
    kw_extractor = yake.KeywordExtractor()
    custom_kw_extractor = yake.KeywordExtractor(
        lan="en", 
        n=1, # Numero de palabras que puede tener una keyword
        dedupLim=lim, # Si es mas pequeño, se queda con menos palabras pero mejores
        top=20, # Numero maximo que puede alcanzar la lista de keywords
        features=None) # Ni idea
    
    # Esto te da una lista de keywords con un valor por cada una
    # que parece ser la importancia que tiene
    keywords_aux = custom_kw_extractor.extract_keywords(search)
    
    # Le quita ese valor y solo se queda con las palabras
    keywords = [word[0] for word in keywords_aux]
    
    return keywords

# function "getKeywords"


def getNew(filename):  
    ''' Abre el archivo que almacena la noticia y lo almacena en formato diccionario
    '''
    with open(DIRNAME + filename.rstrip("\n")) as f:
        new_lines = f.readlines()
        
    new_info = {
        "Title": new_lines[0],
        "Text": ' '.join(new_lines[1:])
    }
    
    return new_info

# function "getNew"



def getLastNews(new_filename): 
    ''' Recoge las noticias relevantes de las 3 busquedas mas recientes  
    '''
    
    searchListAux = None
    news_list = []
    
    # Abre el archivo que contiene los "filenames" de las noticias que se buscaron
    # previamente
    f = open('../data/LastSearches.txt', "r")
    searchListAux = f.readlines() # Lista con las lineas del archivo, las cuales corresponden con filenames
    f.close()
        
    # Se almacena cada filename en una lista auxiliar
    for search in searchListAux:
        news_list.append(getNew(search))
        
    # En el caso de que haya 3 lineas en el archivo
    if (len(searchListAux) == 3):
        # Se elimina la primera ya que corresponde al archivo mas antiguo
        searchListAux.pop(0)
        
    # Se añade a la lista de archivos la nueva busqueda
    searchListAux.append(new_filename)
    searchList = [s.rstrip("\n") for s in searchListAux]
    
    # Se escribe esta lista actualizada de archivos buscados
    f = open('../data/LastSearches.txt', "w")
    for element in searchList:
        f.write(element + "\n")
    f.close()
    
    # Se devuelte la lista con los archivos previos
    return news_list

# function "getLastNews"



def getUserSearchNew(search):
    ''' Recoge la noticia mas relevante segun la busqueda y las noticias
    relacionadas con las 3 busquedas previas
    '''
    
    # Se recogen las keywords relacionadas con la noticia
    # El segundo parametro es grande para que podamos recibir mas keywords
    # y asi ser mas precisos con la noticia que queremos buscar
    keywords = getKeywords(search, 0.9)
    
    # Se recoge el nombre del archivo que tiene nuestra noticia
    new_filename = get_file_name(keywords, gate_path = GATEEXEPATH)
    
    # Se crea el diccionario
    new_info = {
        "new":{},
        "previous":[]
    }
    
    # Se almacena la info en el diccionario
    new_info["new"] = getNew(new_filename)
    new_info["previous"] = getLastNews(new_filename)
    
    # Devuelve el diccionario en formato de cadena de texto
    return json.dumps(new_info)

# function "getUserSearchNew"



def getRelatedNews(search, num_files = 7):
    ''' Recoge una lista de noticias relacionadas de la base de datos.
    '''
    news_list = []
    
    # Se recogen las keywords relacionadas con la noticia
    # El segundo parametro es pequeño para que podamos recibir menos keywords
    # y asi ser menos precisos con las noticias que queremos buscar
    keywords = getKeywords(search, 0.2)
    
    # Se recoge una lista de nombres de archivos donde se encuentran las noticias relacionadas
    # segun las keywors que teniamos.
    new_filenames = get_file_name(keywords, gate_path = GATEEXEPATH, num_files = num_files)
    print(new_filenames)
    
    # Por cada archivo, se almacena la noticia
    for file in new_filenames:
        news_list.append(getNew(file))
            
    # Se devuelve la lista de noticias en formato de cadena de texto
    return json.dumps(news_list)

# function "getRelatedNews"
