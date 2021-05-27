import os
import bcolors

''' Interfaz grafica

Archivo que contiene las funciones para mostrar por pantalla la informacion.
'''

def printLogo():
    ''' Dibuja el logo de la aplicación
    '''
    
    os.system('cls')
    print(" --------                                                                                 -------- ")
    print("|                                                                                                 |")
    print("|     #######   #######   #######   #######   #######     ###     #######   ##   ##   #######     |")
    print("|     ##        ##   ##   ##   ##   ##   ##     ###      ## ##    ##        ##   ##   ##          |")
    print("|     #######   #######   ##   ##   #######     ###     #######   ##        ##   ##   #######     |")
    print("|          ##   ##        ##   ##   ## ##       ###     ##   ##   ##        ##   ##        ##     |")
    print("|     #######   ##        #######   ##   ##     ###     ##   ##   #######   #######   #######     |")
    print("|                                                                                                 |")
    print(" --------                                                                                 -------- ")
    print("                        Welcome to SportAcus, the best sports newspaper!!!!                        ")
    print("\n")


def showSearchedNew(new):
    ''' Muestra la noticia mas relevante y las noticias de las busquedas mas recientes
    '''
    if new:
        # Dibuja el logo de la aplicacion
        printLogo()

        # Muestra el titular
        print (bcolors.HEADER + bcolors.UNDERLINE +  new["new"]["Title"] + bcolors.ENDC)
        # Muestra el texto
        print(new["new"]["Text"])
        # Muesta las noticias de busquedas mas recientes
        showLastNews(new["previous"])    
    else:
        print("No se ha encontrado ninguna noticia.")
         
         
def showLastNews(news):
    ''' Muestra las noticias de las busquedas previas
    '''
    if news:  
        print("\n")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("|                                         Lastest Searches                                        |")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("\n")    
                
        for new in news:
            print (bcolors.HEADER + bcolors.UNDERLINE +  new["Title"] + bcolors.ENDC)
            print(new["Text"])
            print("\n")
    else:
        print("No se han podido recuperar las busquedas previas.")
    
    
    
def showRelatedNews(news):
    ''' Muestra las noticias relacionadas con la busqueda
    '''
    if news:  
        print("\n")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("|                                          Related News                                           |")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("\n")    
                
        for new in news:
            print (bcolors.HEADER + bcolors.UNDERLINE +  new["Title"] + bcolors.ENDC)
            print(new["Text"])
            print("\n")
    else:
        print("No se han encontrado noticias relacionadas.")