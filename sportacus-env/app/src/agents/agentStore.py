import time
import json
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

XMPP_SERVER = "arcipelago.ml"

SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER

PASS = "sportacus"

class StoreAgent(Agent):
    
    class RecvMessageFromSecretary(PeriodicBehaviour):
        async def run(self):
            msg = await self.receive() # wait for a message for 10 seconds
            
            if msg:
                request = json.loads(msg.body)
                
                if request["Type"] == "ADD_NEW":
                    print(
                        "Tengo que almacenar esta nueva noticia.\nTitulo:", 
                        request["Title"], "\nTexto:", request["Text"])
                    
                    await self.send(
                        Message(
                            to=SECRETARY, 
                            body="1", 
                            metadata={"performative": "inform"}))
                    
                elif request["Type"] == "SEARCH_NEW":                    
                    await self.send(
                        Message(
                            to=INDIANA, 
                            body=msg.body, 
                            metadata={"performative": "inform"}))
                    
                elif request["Type"] == "CLOSE":
                    self.agent.stop()
            


    async def setup(self): 
        self.add_behaviour(self.RecvMessageFromSecretary(period=1))