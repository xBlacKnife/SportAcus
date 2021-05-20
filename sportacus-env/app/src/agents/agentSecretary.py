import time
import json

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

import showInterface as si


XMPP_SERVER = "arcipelago.ml"
SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER
PASS = "sportacus"


''' Agente Secretary

Agente encargado de la comunicación con el usuario y con los demás agentes.
Sus funcionalidades son las siguientes:
 - Muestra por pantalla la interfaz de la aplicación.
 - Recoge las peticiones del usuario.
 - Envia las peticiones a los respectivos agentes.
 - Recibe las respuestas (noticias) de cada agente.
 - Muestra por pantalla las noticias al usuario
 
Cuando este agente "muere", la aplicación termina.
'''


# ==================================================================================
#   ESTADOS
# ==================================================================================

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"
STATE_FOUR = "STATE_FOUR"

class StateOne(State):
    ''' Primer estado
    
    Primera pantalla que verá el usuario. Aquí se podrá seleccionar entre tres
    acciones distintas que te llevarán a sus respectivos estados. Las acciones son:
     - Introducir una nueva noticia (ESTADO 2)
     - Buscar una noticia (ESTADO 3)
     - Salir (MUERE EL AGENTE)
    '''
    
    async def run(self):
        # Variable que almacenara la accion que quiere realizar el usuario
        task = 0
        
        # Dibuja el logo de la aplicacion
        si.printLogo()
        
        # Muestra las 3 opciones
        print("¿Que quieres hacer?")
        print("[1] Introducir una nueva noticia")
        print("[2] Buscar una noticia")
        print("[3] Salir")
        
        # Mientras que el input del usuario no corresponda a ninguna de las 
        # tareas que se plantean
        while task < 1 or task > 3:
            
            # Se captura la excepcion por casos como que introduzca texto
            try:
                # Se pide el input al usuario
                task = int(input("\nIndica el numero de la accion que quieres realizar: "))
            except:
                # Se muestra un error por pantalla
                print(
                    bcolors.FAIL 
                    + "Ha ocurrido un error, por favor introduce el numero de la accion de nuevo."
                    + bcolors.ENDC)
        
        # Si quiere "introducir una nueva noticia", va al estado 2
        if task == 1:
            self.set_next_state(STATE_TWO)
        # Si quiere "buscar una noticia", va al estado 3
        elif task == 2:
            self.set_next_state(STATE_THREE)
        # Si quiere "salir", el agente muere
        elif task == 3:
            print("Hasta pronto!!!")
            await self.agent.stop()
            
    # function "run"
    
# class "StateOne"


class StateTwo(State):
    ''' Segundo estado
    
    Pantalla que se muestra en el caso de que el usuario quiera añadir una nueva noticia. Para 
    ello el usuario podrá introducir lo siguientes campos: titular y texto.
    Posteriormente, esta información se enviará a Store para que la almacene.
    '''
    
    async def run(self):
        
        # Dibuja el logo de la aplicacion
        si.printLogo()
        
        # Hace una peticion de los parametros de la noticia
        print("¿Qué noticia quieres introducir? Por favor, rellena los siguientes campos:")
        news = {
            "Type": "ADD_NEW",                  # Tipo de evento para que el agente receptor actue en consonancia
            "Title": input("\nTitular:\n\t"),   # Titular de la noticia
            "Text": input("\nTexto:\n\t")       # Texto de la noticia
        }
        
        # Envia la noticia al agente Store. Para ello transforma el diccionario "new" en un string
        await self.send(
            Message(
                to=STORE,               # Agente receptor
                body=json.dumps(news),  # Noticia en formato string
                metadata={"performative": "inform"}))
        
        print("\n")
        print("Añadiendo...")
        
        # Espera el mensaje de Store que confirma o deniega la nueva noticia.
        msg = await self.receive(timeout=5)
        if msg:
            if msg.body == 1:
                print("Tu noticia ha sido introducida con exito.")
            else:
                print("No se ha podido añadir tu noticia, intentalo de nuevo.")
        else:
            print("No se ha podido añadir tu noticia, intentalo de nuevo.")
        
        # Vuelve al estado inicial
        self.set_next_state(STATE_ONE)
        
    # function "run"
    
# class "StateTwo"


class StateThree(State):
    '''Tercer estado
    
    Pantalla que se muestra si el usuario quiere buscar una noticia. Para ello el usuario
    solo tendra que introducir un texto corto y se le terminara mostrando:
     - Noticia mas relevante
     - Noticias de las busquedas previas
     - Noticias relacionadas con su búsqueda actual
    '''
    
    async def run(self):
        
        # Dibuja el logo de la aplicacion
        si.printLogo()
        
        # Pide al usuario la noticia que quiere ver
        print("¿Que noticias quieres ver?")
        search = input("\nBuscar:\n\t")
        
        # Informacion de la noticia
        news = {
            "Type": "SEARCH_NEW",   # Tipo de evento para que el agente receptor actue en consonancia
            "Search": search        # Texto a buscar    
        }
        
        # Transforma el diccionario con la informacion a cadena de texto
        new_string = json.dumps(news)
        
        # Envia la info a Store para que devuelve la noticia mas relevante y las relacionadas
        # con las tres ultimas busquedas
        await self.send(
            Message(
                to=STORE,
                body=new_string,
                metadata={"performative": "inform"}))
        
        # Envia la info a Marketing para que le devuelva las noticias relacionadas con la peticion
        # actual
        await self.send(
            Message(
                to=MARKETING,
                body=new_string,
                metadata={"performative": "inform"}))
                
        
        # Cambia al estado 4 donde mostrara las noticias
        self.set_next_state(STATE_FOUR)
        
    # function "run"
    
# class "StateThree"
        
        
class StateFour(State):
    ''' Cuarto estado

    Pantalla que se muestra con las noticias relacionadas con la busqueda del usuario. Para
    ello recibe la informacion de los agentes Store y Marketing.
    '''
    
    async def run(self):
        # Variables que almacenaran las noticias
        new_searched = None
        related = None
        
        print("Estamos buscando las noticias ...")
        
        # Recibe las noticias de Marketing
        related_msg = await self.receive(timeout=10) 
        if related_msg:
            related = json.loads(related_msg.body)
        
        # Recibe las noticias de Indiana
        searched_msg = await self.receive(timeout=10) 
        if searched_msg:
            new_searched = json.loads(searched_msg.body)
                                
              
        # Muestra las noticias por pantalla
        si.showSearchedNew(new_searched)
        si.showRelatedNews(related)   
        
        # Pregunta al usuario si quiere volver a la pantalla principal o
        # quiere cerrar la aplicacion    
        print("\n")
        exit = input("¿Quieres volver al inicio? (s/n)")
        if exit == "s":
            self.set_next_state(STATE_ONE)
        else:
            print("Hasta pronto!!!")
            await self.agent.stop()
            
    # function "run"
    
# class "StateFour"
             
            
            
# ==================================================================================
#   CLASS SECRETARYAGENT
# ==================================================================================            

class SecretaryAgent(Agent):
    
    class TalkWithClientBehav(FSMBehaviour):
        ''' Class TalkWithClientBehav
        
        Es un comportamiento de "Maquina de Estados".
        '''
        
        async def on_end(self):
            
            await self.agent.stop()
        
        # function "on_end"
        
    # class "TalkWithClientBehav"
    

    async def setup(self):
        
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
    
    # function "setup"
        
# class "SecretaryAgent"