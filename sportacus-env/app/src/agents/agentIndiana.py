import time
import json
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

import newManager as nm

XMPP_SERVER = "arcipelago.ml"
SECRETARY = "secretarydasi" + "@" + XMPP_SERVER


''' Agente Indiana

Es el encargado de buscar las noticias segun la nueva busqueda del usuario. Se funcionalidades son:
 - Recibir esta busqueda del agente Store.
 - Buscar la noticia mas relevante (A).
 - Buscar las noticias que se mostraron en las 3 busquedas mas recientes (B, C, D).
 - Guardará esta nueva busqueda A (C, D, A).
 - Enviara las noticias a Secretary directamente.
'''

class IndianaAgent(Agent):
       
    class InteractWithStore(PeriodicBehaviour):
        ''' Class InteractWithStore
        
        Es un comportamiento "periodico" que cada cierto tiempo comprueba si hay mensajes
        del Store y posteriormente envia la informacion a Secretary.
        '''
         
        async def run(self):
            
            # Comprueba si ha recibido algun mensaje
            msg = await self.receive() # wait for a message for 10 seconds
            
            # En el caso de que se haya recibido
            if msg:
                # Se convierte ese mensaje en un dict
                request = json.loads(msg.body)
                               
                # Si es una peticion de busqueda
                if request["Type"] == "SEARCH_NEW":    
                    
                    # Creara un diccionario con la busqueda relevante y las 3 ultimas busquedas
                    # {
                    #   "new":{
                    #       "Title": "",
                    #       "Text": ""
                    #   },
                    #   "previous":[
                    #       {NOTICIA 1}, {NOTICIA 2}, ...
                    #   ]
                    # }            
                    newSearched = nm.getUserSearchNew(request["Search"])
                                        
                    # Envia estas noticias al Secretary                    
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
    
# class "IndianaAgent"