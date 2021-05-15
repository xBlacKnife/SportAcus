import time
import json
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

import newManager as nm

XMPP_SERVER = "arcipelago.ml"

SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER

PASS = "sportacus"



class MarketingAgent(Agent):
       
    class RecvMessageFromStore(PeriodicBehaviour):
         
        async def run(self):
            msg = await self.receive() # wait for a message for 10 seconds
            
            if msg:
                request = json.loads(msg.body)
                               
                if request["Type"] == "SEARCH_NEW":                   
                    newSearched = nm.getRelatedNews(request["Search"])
                                        
                    await self.send(
                        Message(
                            to=SECRETARY, 
                            body=newSearched, 
                            metadata={"performative": "inform"}))
                    
                elif request["Type"] == "CLOSE":
                    await self.agent.stop()
                
    
    async def setup(self):       
        self.add_behaviour(self.RecvMessageFromStore(period=1))