import itertools
import threading
import time
import sys
import os

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

from agents.agentSecretary import SecretaryAgent
from agents.agentStore import StoreAgent
from agents.agentIndiana import IndianaAgent
from agents.agentMarketing import MarketingAgent

XMPP_SERVER = "arcipelago.ml"
SECRETARY = "secretarydasi" + "@" + XMPP_SERVER
STORE = "storedasi" + "@" + XMPP_SERVER
INDIANA = "indianadasi" + "@" + XMPP_SERVER
MARKETING = "marketingdasi" + "@" + XMPP_SERVER

PASS = "sportacus"

done = False

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rLoading... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)


if __name__ == "__main__":
    os.system('cls')
    t = threading.Thread(target=animate)
    t.start()         
    
    # Marketing
    marketingAgent = MarketingAgent(MARKETING, PASS)
    future = marketingAgent.start()
    future.result()
    
    # Indiana
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
    
    done = True

    while secretaryAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            secretaryAgent.stop()
            storeAgent.stop()
            indianaAgent.stop()
            marketingAgent.stop()
            break