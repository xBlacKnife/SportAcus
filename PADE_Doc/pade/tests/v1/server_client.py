from twisted.internet import protocol, reactor

class Sniffer(protocol.Protocol):
    
    def __init__(self, factory):
        self.factory = factory
    
    def connectionMade(self):
        if self.factory.isClient:
            self.transport.write('Connection is made with ' + str(self.transport.getPeer()))
        else:
            self.transport.write('You are a client and you are connected!')
        
    def dataReceived(self, data):
        if 'quit' in data:
            self.transport.loseConnection()
        else:
            if self.factory.isClient:
                print 'Menssage received: ', data
            else:
                print 'Trying to connect'
                reactor.connectTCP('localhost', 1234, SnifferFactory(isClient=True))

class SnifferFactory(protocol.ClientFactory):
    
    def __init__(self, isClient):
        self.isClient = isClient
        
    def buildProtocol(self, addr):
        return Sniffer(self)

reactor.listenTCP(1235, SnifferFactory(isClient=False))
reactor.run()