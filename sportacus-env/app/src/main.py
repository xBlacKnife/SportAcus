import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from agents.agentSecretary import SecretaryAgent
from agents.agentStore import StoreAgent
from agents.agentIndiana import IndianaAgent

XMPP_SERVER = "arcipelago.ml"

SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER


PASS = "sportacus"


if __name__ == "__main__":
    
    indianaAgent = IndianaAgent(INDIANA, PASS)
    future = indianaAgent.start()
    future.result()
    
    # Store
    storeAgent = StoreAgent(STORE, PASS)
    future = storeAgent.start()
    future.result()
    
    # Secretary
    secretaryAgent = SecretaryAgent(SECRETARY, PASS)
    future = secretaryAgent.start()
    future.result()

    while secretaryAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            secretaryAgent.stop()
            storeAgent.stop()
            indianaAgent.stop()
            break