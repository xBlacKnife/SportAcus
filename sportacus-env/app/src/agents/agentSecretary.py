import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from spade.behaviour import FSMBehaviour, State

XMPP_SERVER = "arcipelago.ml"
SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER
PASS = "sportacus"

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"



class StateOne(State):
    
    task = 0
    
    async def run(self):
        print("\n")
        print("Bienvenido a SportAcus, tu periódico de deportes de confianza.")
        print("Por favor, selecciona la acción que quieres realizar")
        print("1. Introducir una nueva noticia.")
        print("2. Buscar una noticia.")
        
        while self.task != 1 and self.task != 2:
            self.task = int(input("Indica el numero de la accion correspondiente: "))
        
        if self.task == 1:
            self.set_next_state(STATE_TWO)
        elif self.task == 2:
            self.set_next_state(STATE_THREE)
        
        #msg = Message(to="fsmagent@your_xmpp_server")
        #msg.body = "msg_from_state_one_to_state_three"
        #await self.send(msg)
        #self.set_next_state(STATE_TWO)


class StateTwo(State):
    async def run(self):
        print("\n")
        print("¿Qué noticia quieres introducir? Por favor, rellena los siguientes campos:")
        title = input("Titulo: ")
        text = input("Texto: ")
        
        print("\n")
        print("Estamos introducciendo tu noticia en nuestra base de datos.")
        print("Muchas gracias por tu aportación.")
        
        #self.set_next_state(STATE_THREE)


class StateThree(State):
    async def run(self):
        print("\n")
        print("¿Que noticias quieres ver?")
        news = input("Buscador: ")
        #msg = await self.receive(timeout=5)
        #print(f"State Three received message {msg.body}")
        # no final state is setted, since this is a final state

class SecretaryAgent(Agent):
    
    class TalkWithClientBehav(FSMBehaviour):
        async def on_start(self):
            print(f"FSM starting at initial state {self.current_state}")

        async def on_end(self):
            print(f"FSM finished at state {self.current_state}")
            await self.agent.stop()
    
    class SendMessageBehav(OneShotBehaviour):
        
        
        async def run(self):          
            
            msg = Message(to=STORE)     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Me llamo Alejandro"                 # Set the message content

            await self.send(msg)
            print("¡Mensaje enviado!")

            # stop agent from behaviour
            #await self.agent.stop()
    
    '''class RecvMessageBehav(OneShotBehaviour):
        async def run(self):
            print("[SecretaryAgent] RecvMessageBehav -> run")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Mensaje recibido con el siguiente contenido: {}".format(msg.body))
                print("De acuerdo, ahora la almaceno")
            else:
                print("No se ha recibido ningun mensaje despues de 10 segundoss")

            # stop agent from behaviour
            await self.agent.stop()'''

    async def setup(self):
        print("SecretaryAgent ha comenzado")       
        self.add_behaviour(self.SendMessageBehav())
        
        fsm = self.TalkWithClientBehav()
        fsm.add_state(name=STATE_ONE, state=StateOne(), initial=True)
        fsm.add_state(name=STATE_TWO, state=StateTwo())
        fsm.add_state(name=STATE_THREE, state=StateThree())
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_ONE, dest=STATE_THREE)
        #fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)
        self.add_behaviour(fsm)
        
        #template = Template()
        #template.set_metadata("performative", "inform")
        #self.add_behaviour(self.RecvMessageBehav(), template)