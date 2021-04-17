from pade.misc.utility import display_message
from pade.core.agent import Agent
        
class AgentSecretary(Agent):
    def __init__(self, aid):
        super(AgentSecretary, self).__init__(aid=aid)
        display_message(self.aid.localname, "Soy el agente  \'Secretario\'.")
        
class AgentStore(Agent):
    def __init__(self, aid):
        super(AgentStore, self).__init__(aid=aid)
        display_message(self.aid.localname, "Soy el agente \'Mozo de Almacen\'.")
        
        
class AgentArchaeologist(Agent):
    def __init__(self, aid):
        super(AgentArchaeologist, self).__init__(aid=aid)
        display_message(self.aid.localname, "Soy el agente  \'Arqueologo\'.")
        
        
class AgentMarketing(Agent):
    def __init__(self, aid):
        super(AgentMarketing, self).__init__(aid=aid)
        display_message(self.aid.localname, "Soy el agente  \'Marketing\'.")