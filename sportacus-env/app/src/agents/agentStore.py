import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

XMPP_SERVER = "arcipelago.ml"

SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER


PASS = "sportacus"

class StoreAgent(Agent):
    '''class SendMessageBehav(OneShotBehaviour):
        async def run(self):
            print("[StoreAgent] SendMessageBehav -> run")
            msg = Message(to=STORE)     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Almacena esta nueva noticia."                    # Set the message content

            await self.send(msg)
            print("¡Mensaje enviado!")

            # stop agent from behaviour
            await self.agent.stop()'''
    
    class RecvMessageBehav(OneShotBehaviour):
        async def run(self):
            print("[StoreAgent] RecvMessageBehav -> run")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Mensaje recibido con el siguiente contenido: {}".format(msg.body))
                print("De acuerdo, ahora la almaceno")
            else:
                print("No se ha recibido ningun mensaje despues de 10 segundoss")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("StoreAgent ha comenzado")
        template = Template()
        template.set_metadata("performative", "inform")
        
        #self.add_behaviour(self.SendMessageBehav())
        self.add_behaviour(self.RecvMessageBehav(), template)