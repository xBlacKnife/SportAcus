import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from agents.agentSecretary import SecretaryAgent
from agents.agentStore import StoreAgent

XMPP_SERVER = "arcipelago.ml"

SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER


PASS = "sportacus"


if __name__ == "__main__":
    secretaryAgent = SecretaryAgent(SECRETARY, PASS)
    secretaryAgent.start()
    
    storeAgent = StoreAgent(STORE, PASS)
    future = storeAgent.start()
    future.result() # wait for receiver agent to be prepared.

    while storeAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            secretaryAgent.stop()
            storeAgent.stop()
            break
    print("Agents finished")