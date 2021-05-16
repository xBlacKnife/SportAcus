import time
import json
import os
import bcolors

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message



XMPP_SERVER = "arcipelago.ml"
SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER
PASS = "sportacus"

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"
STATE_FOUR = "STATE_FOUR"

def printLogo():
    #os.system('cls')
    print(" --------                                                                                 -------- ")
    print("|                                                                                                 |")
    print("|     #######   #######   #######   #######   #######     ###     #######   ##   ##   #######     |")
    print("|     ##        ##   ##   ##   ##   ##   ##     ###      ## ##    ##        ##   ##   ##          |")
    print("|     #######   #######   ##   ##   #######     ###     #######   ##        ##   ##   #######     |")
    print("|          ##   ##        ##   ##   ## ##       ###     ##   ##   ##        ##   ##        ##     |")
    print("|     #######   ##        #######   ##   ##     ###     ##   ##   #######   #######   #######     |")
    print("|                                                                                                 |")
    print(" --------                                                                                 -------- ")
    print("               ¡¡¡¡Bienvenido a SportAcus, tu periodico de deportes de confianza!!!!               ")
    print("\n")

class StateOne(State):
    
    task = 0
    
    async def run(self):
        self.task = 0
        
        printLogo()
        print("¿Que quieres hacer?")
        print("[1] Introducir una nueva noticia")
        print("[2] Buscar una noticia")
        print("[3] Salir")
        
        while self.task < 1 or self.task > 3:
            try:
                self.task = int(input("\nIndica el numero de la accion que quieres realizar: "))
            except:
                print(
                    bcolors.FAIL 
                    + "Ha ocurrido un error, por favor introduce el numero de la accion de nuevo."
                    + bcolors.ENDC)
        
        if self.task == 1:
            self.set_next_state(STATE_TWO)
        elif self.task == 2:
            self.set_next_state(STATE_THREE)
        elif self.task == 3:
            print("Hasta pronto!!!")
            await self.agent.stop()


class StateTwo(State):
    async def run(self):
        printLogo()
        print("¿Qué noticia quieres introducir? Por favor, rellena los siguientes campos:")
        
        news = {
            "Type": "ADD_NEW",
            "Title": input("\nTitulo:\n\t"),
            "Text": input("\nTexto:\n\t")
        }
        
        await self.send(
            Message(
                to=STORE,
                body=json.dumps(news),
                metadata={"performative": "inform"}))
        
        print("\n")
        print("Añadiendo...")
        
        msg = await self.receive(timeout=5)
        if msg:
            print("Tu noticia ha sido introducida con exito.")
        else:
            print("No se ha podido añadir tu noticia, intentalo de nuevo.")
        
        self.set_next_state(STATE_ONE)

class StateThree(State):
    async def run(self):
        printLogo()
        print("¿Que noticias quieres ver?")
        
        search = input("\nBuscar:\n\t")
        
        news = {
            "Type": "SEARCH_NEW",
            "Search": search
        }
        
        new_string = json.dumps(news)
        
        await self.send(
            Message(
                to=STORE,
                body=new_string,
                metadata={"performative": "inform"}))
        
        await self.send(
            Message(
                to=MARKETING,
                body=new_string,
                metadata={"performative": "inform"}))
                
        
        
        self.set_next_state(STATE_FOUR)
        

def showSearchedNew(new):
    if new:
        printLogo()

        print (bcolors.HEADER + bcolors.UNDERLINE +  new["new"]["Title"] + bcolors.ENDC)
        print(new["new"]["Text"])
        showLastNews(new["previous"])    
    else:
        print("No se ha encontrado ninguna noticia.")
        
        
def showLastNews(news):
    if news:  
        print("\n")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("|                                        Busquedas previas                                        |")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("\n")    
                
        for new in news:
            print (bcolors.HEADER + bcolors.UNDERLINE +  new["Title"] + bcolors.ENDC)
            print(new["Text"])
            print("\n")
    else:
        print("No se han podido recuperar las busquedas previas.")
    
    
    
def showRelatedNews(news):
    if news:  
        print("\n")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("|                                      Noticias Relacionadas                                      |")
        print(" ------------------------------------------------------------------------------------------------- ")
        print("\n")    
                
        for new in news:
            print (bcolors.HEADER + bcolors.UNDERLINE +  new["Title"] + bcolors.ENDC)
            print(new["Text"])
            print("\n")
    else:
        print("No se han encontrado noticias relacionadas.")

        
class StateFour(State):
    async def run(self):
        new_searched = None
        related = None
        
        print("Estamos buscando las noticias ...")
        
        related_msg = await self.receive(timeout=10) 
        if related_msg:
            related = json.loads(related_msg.body)
        
        searched_msg = await self.receive(timeout=10) 
        if searched_msg:
            new_searched = json.loads(searched_msg.body)
                                
              
        showSearchedNew(new_searched)
        showRelatedNews(related)   
        
            
        print("\n")
        exit = input("¿Quieres volver al inicio? (s/n)")
        if exit == "s":
            self.set_next_state(STATE_ONE)
        else:
            print("Hasta pronto!!!")
            await self.agent.stop()
            
            
class SecretaryAgent(Agent):
    
    class TalkWithClientBehav(FSMBehaviour):
        async def on_end(self):
            await self.agent.stop()
    

    async def setup(self):
        print("============== Secretary started ==============")
        
        fsm = self.TalkWithClientBehav()
        
        fsm.add_state(name=STATE_ONE, state=StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=StateTwo())
        fsm.add_state(name=STATE_THREE, state=StateThree())
        fsm.add_state(name=STATE_FOUR, state=StateFour())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_TWO, dest=STATE_ONE)
        fsm.add_transition(source=STATE_ONE, dest=STATE_THREE)
        fsm.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        fsm.add_transition(source=STATE_FOUR, dest=STATE_ONE)
        
        self.add_behaviour(fsm)