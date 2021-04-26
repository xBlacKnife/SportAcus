from pade.misc.utility import display_message
from pade.core.agent import Agent
        
class AgentSecretary(Agent):
    def __init__(self, aid):
        super(AgentSecretary, self).__init__(aid=aid)
        display_message(self.aid.localname, "Soy el agente  \'Secretario\'.")