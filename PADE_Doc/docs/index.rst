.. Pade documentation master file, created by
   sphinx-quickstart on Sat Sep 12 19:30:28 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Agent DEvelopment framework
==================================

Sistemas Multiagentes para Python!
----------------------------------

PADE é um framework para desenvolvimento, execução e gerenciamento de sistemas multiagentes em ambientes de computação distribuída.

PADE é escrito 100% em Python e utiliza as bibliotecas do projeto `Twisted <http://twistedmatrix.com/>`_ para implementar a comunicação entre os nós da rede.

PADE é software livre, licenciado sob os termos da licença MIT, desenvolvido pelo Grupo de Redes Elétricas Inteligentes (GREI) do Departamento de Engenharia Elétrica da Universidade Federal do Ceará.

Qualquer um que queira contribuir com o projeto é convidado a baixar, executar, testar e enviar feedback a respeito das impressões tiradas da plataforma. 

PADE é simples!
~~~~~~~~~~~~~~~~~

::

    # agent_example_1.py
    # A simple hello agent in PADE!

    from pade.misc.utility import display_message, start_loop
    from pade.core.agent import Agent
    from pade.acl.aid import AID
    from sys import argv

    class AgenteHelloWorld(Agent):
        def __init__(self, aid):
            super(AgenteHelloWorld, self).__init__(aid=aid)
            display_message(self.aid.localname, 'Hello World!')


    if __name__ == '__main__':
        agents_per_process = 3
        c = 0
        agents = list()
        for i in range(agents_per_process):
            port = int(argv[1]) + c
            agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
            agente_hello = AgenteHelloWorld(AID(name=agent_name))
            agents.append(agente_hello)
            c += 1000
        
        start_loop(agents)

Neste arquivo exemplo (que está na pasta de exemplos no repositório PADE) é possível visualizar três sessões bem definidas.

A primeira contém as importações necessárias de classes que se encontram nos módulos do pade.

Na segunda uma classe que herda da classe pade Agent é definida com as pricipais atribuições do agente.

Na terceira parte que está encapsulada em uma estrutura if são realizados os procedimentos para lançar os agentes.

Se você quiser saber mais basta seguir a documentação aqui: :ref:`hello-world-page`. 

E fácil de instalar!
~~~~~~~~~~~~~~~~~~~~

Para instalar o PADE basta executar o seguinte comando em um terminal linux: 

::

    $ pip install pade
    $ pade start-runtime --port 20000 agent_example_1.py

Veja mais aqui: :ref:`installation-page`.

Funcionalidades
~~~~~~~~~~~~~~~

O PADE foi desenvolvido tendo em vista os requisitos para sistema de automação. PADE oferece os seguintes recursos em sua biblioteca para desenvolvimento de sistemas multiagentes:


**Orientação a Objetos**
  Abstração para construção de agentes e seus comportamentos utilizando conceitos de orientação a objetos;

**Ambiente de execução**
  Módulo para inicialização do ambiente de execução de agentes, inteiramente em código Python;

**Mensagens no padrão FIPA-ACL**
  Módulo para construção e tratamento de mensagens no padrão FIPA-ACL;

**Filtragem de Mensagens**
  Módulo para filtragem de mensagens;

**Protocolos FIPA**
  Módulo para a implementação dos protocolos definidos pela FIPA;

**Comportamentos Cíclicos e Temporais**
  Módulo para implementação de comportamentos cíclicos e temporais;

**Banco de Dados**
  Módulo para interação com banco de dados;

**Envio de Objetos Serializados**
  Possibilidade de envio de objetos serializados como conteúdo das mensagens FIPA-ACL.


Além dessas funcionalidades, o PADE é de fácil instalação e configuração, multiplataforma, podendo ser instalado e utilizado em hardwares embarcados que executam sistema operacional Linux, como Raspberry Pi e BeagleBone Black, bem como sistema operacional Windows.



Guia do Usuário
----------------

.. toctree::
   :maxdepth: 2

   user/instalacao
   user/pade-cli
   user/hello-world
   user/agentes-temporais
   user/enviando-mensagens
   user/recebendo-mensagens
   user/um-momento
   user/enviando-objetos
   user/selecao-de-mensagens
   user/interface-grafica
   user/protocolos
   user/desenvolvedores



.. Referência da API do PADE 
.. -------------------------

.. .. toctree::
..    :maxdepth: 2

..    api


