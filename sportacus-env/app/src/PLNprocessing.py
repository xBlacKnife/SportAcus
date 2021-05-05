import os
import string

import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.text import ContextIndex 

corpusDir = 'Corpus/'
documentsDir = '../resources/bbc-sport/' # Directory of corpus.

if not os.path.isdir(corpusDir):
    os.mkdir(corpusDir)
    
newcorpus = PlaintextCorpusReader(documentsDir, '.*')
print (newcorpus.paras(newcorpus.fileids()[0]))

# esto es para descargar los paquetes de nltk, 
# en principio solo hay que hacerlo una vez 
# y creo que no es necesario realmente, no lo hagas
# nltk.download() 
# testFilePath = '../resources/bbc-sport/001.txt'
# with open(testFilePath) as reader: 
    # text = reader.read()
    # tokens = [t for t in word_tokenize(text)]

    # freq = nltk.FreqDist(tokens)
    # # tokenized = nltk.word_tokenize(tokens)
    
    # for key,val in freq.items():
    #     print (str(key) + ': ' + str(val))

    # freq.plot(20, cumulative=False)
    
    
    # clean_tokens = tokens[:]

    # sr = stopwords.words('english')
    # for token in tokens:
    #     if token in sr:
    #         clean_tokens.remove(token)
    #     elif token in string.punctuation:
    #         clean_tokens.remove(token)
            
            
    # freq = nltk.FreqDist(clean_tokens)
    # freq.plot(20, cumulative=False)
    