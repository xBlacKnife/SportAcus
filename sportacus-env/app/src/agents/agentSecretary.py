import time
import json
from os.path import exists

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

import showInterface as si

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


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



                    
# ==================================================================================
#   CLASS SECRETARYAGENT
# ==================================================================================            

class SecretaryAgent(Agent):
    
    chatbot = None
    
    async def setup(self):
        
        fsm = self.TalkWithClientBehav()
        
        fsm.add_state(name=STATE_ONE, state=self.StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=self.StateTwo())
        fsm.add_state(name=STATE_THREE, state=self.StateThree())
        fsm.add_state(name=STATE_FOUR, state=self.StateFour())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_TWO, dest=STATE_ONE)
        fsm.add_transition(source=STATE_ONE, dest=STATE_THREE)
        fsm.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        fsm.add_transition(source=STATE_FOUR, dest=STATE_ONE)
        
        self.add_behaviour(fsm)
    
    # function "setup"
            
    
    class TalkWithClientBehav(FSMBehaviour):
        ''' Class TalkWithClientBehav
        
        Es un comportamiento de "Maquina de Estados".
        '''
        
        async def on_end(self):
            
            await self.agent.stop()
        
        # function "on_end"
        
    # class "TalkWithClientBehav"
    
    class StateOne(State):
        ''' Primer estado
        
        Primera pantalla que verá el usuario. Aquí se podrá seleccionar entre tres
        acciones distintas que te llevarán a sus respectivos estados. Las acciones son:
        - Introducir una nueva noticia (ESTADO 2)
        - Buscar una noticia (ESTADO 3)
        - Salir (MUERE EL AGENTE)
        '''
        
        async def run(self):
            
            if self.agent.chatbot == None:
            
                self._textToSearchNew = "OK! Tell me what you want to search."
                self._textToAddNew = "Perfect! What news do you want to add?"
                self._textToBye = "See you soon!!"
                self._defaultAnswer = "I'm sorry, but I don't understand."
                
                # Instanciamos un chatBot.
                self.agent.chatbot = ChatBot(
                    silence_performance_warning=True,
                    name='ChatBot',
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=[
                        {
                            'import_path': 'chatterbot.logic.BestMatch',
                            'maximum_similarity_threshold': 0.60,
                            'default_response': self._defaultAnswer
                        }
                    ]
                )
                
                trainer = ListTrainer(self.agent.chatbot)

                conversation = (
                    ['search', self._textToSearchNew],
                    ['search new', self._textToSearchNew],
                    ['i want to search new', self._textToSearchNew],
                    ['search football new', self._textToSearchNew],
                    ['i want to search football new', self._textToSearchNew],
                    ['search basket new', self._textToSearchNew],
                    ['i want to search basket new', self._textToSearchNew],
                    ['search tennis new', self._textToSearchNew],
                    ['i want to search tennis new', self._textToSearchNew],
                    ['search sports new', self._textToSearchNew],
                    ['i want to search sports new', self._textToSearchNew],
                    ['add', self._textToAddNew],
                    ['add new', self._textToAddNew],
                    ['i want to add new', self._textToAddNew],
                    ['include', self._textToAddNew],
                    ['include new', self._textToAddNew],
                    ['i want to include new', self._textToAddNew],
                    ['import', self._textToAddNew],
                    ['import new', self._textToAddNew],
                    ['i want to import new', self._textToAddNew],
                    ['insert', self._textToAddNew],
                    ['insert new', self._textToAddNew],
                    ['i want to insert new', self._textToAddNew],
                    ['bye', self._textToBye],
                    ['exit', self._textToBye]
                )
                
                for c in conversation:
                    trainer.train(c)
                
            
            # Dibuja el logo de la aplicacion
            si.printLogo()
            
            bot_response = self._defaultAnswer
            while bot_response == self._defaultAnswer:
                print("Hello, can I help you? :)")
                
                user_input = input()
                bot_response = str(self.agent.chatbot.get_response(user_input))
                print(bot_response, "\n")
                
                if bot_response != self._defaultAnswer:
                    if bot_response == self._textToAddNew:
                        self.set_next_state(STATE_TWO)
                    elif bot_response == self._textToSearchNew:
                        self.set_next_state(STATE_THREE)
                    elif bot_response == self._textToBye:
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
            print("Which news item would you like to add? Please fill in the following fields:")
            news = {
                "Type": "ADD_NEW",                  # Tipo de evento para que el agente receptor actue en consonancia
                "Title": input("\nHeadline:\n\t"),   # Titular de la noticia
                "Text": input("\nText:\n\t")       # Texto de la noticia
            }
            
            # Envia la noticia al agente Store. Para ello transforma el diccionario "new" en un string
            await self.send(
                Message(
                    to=STORE,               # Agente receptor
                    body=json.dumps(news),  # Noticia en formato string
                    metadata={"performative": "inform"}))
            
            print("\n")
            print("Adding...")
            
            # Espera el mensaje de Store que confirma o deniega la nueva noticia.
            msg = await self.receive(timeout=5)
            if msg:
                if msg.body == 1:
                    print("Your news have been correctly introduced.")
                else:
                    print("Your news could not be added, please try again.")
            else:
                print("Your news could not be added, please try again.")
            
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
            print("What news do you want to search?")
            search = input("\nSearch:\n\t")
            
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
            
            print("We are searching for news ...")
            
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
            exit = input("Do you want to go back? (y/n)")
            if exit == "y":
                self.set_next_state(STATE_ONE)
            else:
                print("See you soon!!!")
                await self.agent.stop()
                
        # function "run"
        
    # class "StateFour"
            
# class "SecretaryAgent"