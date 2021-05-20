import time
import json
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

import newManager as nm

XMPP_SERVER = "arcipelago.ml"
SECRETARY = "secretarydasi" + "@" + XMPP_SERVER


''' Agente Marketing

Es el encargado de buscar las noticias relacionadas con la busqueda
del usuario
'''

class MarketingAgent(Agent):
       
    class InteractWithStore(PeriodicBehaviour):
        ''' Class InteractWithStore
        Es un comportamiento "periodico" que cada cierto tiempo comprueba si hay mensajes
        del Secretary y posteriormente le envia la informacion.
        '''
         
        async def run(self):
            
            # Intenta recibir un mensaje
            msg = await self.receive() # wait for a message for 10 seconds
            
            # En el caso de que se haya recibido un mensaje
            if msg:
                
                # Transforma el mensaje en un diccionario
                request = json.loads(msg.body)
                               
                # Si es una peticion de busqueda
                if request["Type"] == "SEARCH_NEW":     
                    
                    # Busca las noticias relacionadas              
                    newSearched = nm.getRelatedNews(request["Search"])
                                   
                    # Envia dichas noticias al Secretary     
                    await self.send(
                        Message(
                            to=SECRETARY, 
                            body=newSearched, 
                            metadata={"performative": "inform"}))
                    
                elif request["Type"] == "CLOSE":
                    await self.agent.stop()
        
        # function "run"
        
    # class "InteractWithStore"
                
    
    async def setup(self): 
              
        self.add_behaviour(self.InteractWithStore(period=1))
    
    # function "setup"
    
# class "MarketingAgent"