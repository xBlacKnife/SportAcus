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


class IndianaAgent(Agent):
    
    class RecvMessageFromStore(PeriodicBehaviour):
        async def run(self):
            msg = await self.receive() # wait for a message for 10 seconds
            
            if msg:
                print("\n## INDIANA ##")
                request = json.loads(msg.body)
                               
                if request["Type"] == "SEARCH_NEW":
                    print("Estoy buscando esta noticia", request["Search"])
                    
                    await self.send(
                        Message(
                            to=SECRETARY, 
                            body="Estas son las noticias de hoy!!!!", 
                            metadata={"performative": "inform"}))
                    
                elif request["Type"] == "CLOSE":
                    await self.agent.stop()
                    
                print("## ------- ##")
                
    
    async def setup(self):
        print("============== Indiana started ==============")  
        self.add_behaviour(self.RecvMessageFromStore(period=1))