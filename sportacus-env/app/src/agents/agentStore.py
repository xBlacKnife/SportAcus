import time
import json
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

import newManager as nm

XMPP_SERVER = "arcipelago.ml"

SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER


''' Agente Store

Es el encargado de almacenar las nuevas noticias en la BD y en el caso de que
se quiera buscar alguna noticia, se hara un reenvio de esta peticion a Indiana
para que relice dicha busqueda.
'''
        
class StoreAgent(Agent):
    
    class InteractWithSecretary(PeriodicBehaviour):
        ''' Class InteractWithSecretary
        
        Es un comportamiento "Periodico" que cada cierto tiempo busca si tiene mensajes de parte
        del Secretary.
        '''
        
        async def run(self):
            
            # Intenta recibir un mensaje con un tiempo maximo de 5 segundos
            msg = await self.receive(timeout=5)
            
            # En el caso de que se haya recibido un mensaje
            if msg:
                # Convierte la cadena de texto en diccionario
                request = json.loads(msg.body)
                
                # Comprueba el tipo de la peticion
                # En el caso que se quiera añadir una nueva noticia
                if request["Type"] == "ADD_NEW":
                    
                    # Se almacena la nueva noticia en la BD                 
                    saved = nm.saveNew(request)
                    
                    # Se envia una respuesta a Secretary
                    await self.send(
                        Message(
                            to=SECRETARY,       # Agente Secretary
                            body=str(saved),    # Info de si se ha podido añadir o no
                            metadata={"performative": "inform"}))
                
                # En el caso que se quiera buscar una noticia
                elif request["Type"] == "SEARCH_NEW":      
                    # Se reenvia esta informacion a Indiana              
                    await self.send(
                        Message(
                            to=INDIANA,         # Agente indiana
                            body=msg.body,      # Misma informacion
                            metadata={"performative": "inform"}))
                    
                elif request["Type"] == "CLOSE":
                    self.agent.stop()
                    
        # function "run"
        
    # class "InteractWithSecretary"
            


    async def setup(self): 
        self.add_behaviour(self.InteractWithSecretary(period=1))
        
    # function "setup"
    
# class "StoreAgent"