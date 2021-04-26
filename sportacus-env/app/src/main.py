# agent_example_1.py
# A simple hello agent in PADE!

from pade.misc.utility import start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv

from agents.agentSecretary import AgentSecretary
from agents.agentStore import AgentStore
from agents.agentArchaeologist import AgentArchaeologist
from agents.agentMarketing import AgentMarketing


def create_agents():
    c = 0
    agents = list()
    
    port = int(argv[1]) + c
    agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
    agents.append(AgentSecretary(AID(name=agent_name)))        
    
    port = port + 1000
    agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
    agents.append(AgentStore(AID(name=agent_name)))       
    
    port = port + 1000
    agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
    agents.append(AgentArchaeologist(AID(name=agent_name)))       
    
    port = port + 1000
    agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
    agents.append(AgentMarketing(AID(name=agent_name)))
                  
    return agents
    


if __name__ == '__main__':
    start_loop(create_agents())