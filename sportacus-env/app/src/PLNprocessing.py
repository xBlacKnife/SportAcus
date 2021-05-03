import nltk

# esto es para descargar los paquetes de nltk, 
# en principio solo hay que hacerlo una vez 
# y creo que no es necesario realmente, no lo hagas
# nltk.download() 
testFilePath = '../resources/bbc-sport/001.txt'
with open(testFilePath) as reader: 
    text = reader.read()
    tokens = [t for t in text.split()]

    freq = nltk.FreqDist(tokens)

    for key,val in freq.items():

        print (str(key) + ': ' + str(val))
