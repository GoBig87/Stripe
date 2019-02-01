from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log
import ast
import os
import stripe

_stripe_api_key = "your key here"
stripe.api_key = _stripe_api_key


class NodeProtocol(Protocol):
    nodeDataDict = ''

    def dataReceived(self, data):
        log.msg(data)
        dataString = str(data)
        self.deferred = self.factory.service.check_data(dataString)
        self.transport.write(self.factory.service.status)
        self.transport.loseConnection()


class NodeFactory(ServerFactory):

    protocol = NodeProtocol

    def __init__(self, service):
        self.service = service

    def data_finished(self, nodeData):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(nodeData)

class NodeService(service.Service):

    def __init__(self):
        pass

    def startService(self):
        service.Service.startService(self)

    def check_data(self, data):
        self.dataDict = None
        log.msg(data)
        try:
            self.dataDict = ast.literal_eval(data)
        except:
            pass

        if "function" in self.dataDict.keys():
            function = self.dataDict['function']
            if function == 'client_token':
                self.processCustomer(self.dataDict)
            if function == 'check_valid_payment':
                self.checkPayment(self.dataDict)
            if function == 'Create_Charge':
                self.createCharge(self.dataDict)
        else:
            log.msg('Error 101. No valid argument presented.')



    def createCharge(self,dict):
        customerToken = dict['customerID']
        amountCharged = 100
        charge = stripe.Charge.create(amount=amountCharged, currency='usd', description='Add info here', customer=customerToken, capture=False)

        if charge["status"] == "succeeded":
            self.receipt(dict['email'],userDict[dict['email']]['Start_Time'],dict['end_time'],stringCharge,duration)
            msg = self.Cipher.encrypt('{"rsp":"succeeded"}')
        else:
            msg = self.Cipher.encrypt('{"rsp":"failed"}')

        self.status = msg

    def checkPayment(self,dict):
        customerToken = dict['customerID']
        charge = stripe.Charge.create(amount=1,currency='usd',description='Test charge',source=customerToken,capture=False)

        if charge["status"] == "succeeded":
            msg = self.Cipher.encrypt('{"rsp":"succeeded"}')
        else:
            msg = self.Cipher.encrypt('{"rsp":"failed"}')

        self.status = msg


# configuration parameters
port = 8080
#ifacev4 = '0.0.0.0'
iface = '::0'

# this will hold the services that combine to form the poetry server
top_service = service.MultiService()

# the poetry service holds the poem. it will load the poem when it is
# started
node_service = NodeService()
node_service.setServiceParent(top_service)

# the tcp service connects the factory to a listening socket. it will
# create the listening socket when it is started
factory = NodeFactory(node_service)
tcp_service = internet.TCPServer(port, factory, interface=iface)
tcp_service.setServiceParent(top_service)

# this variable has to be named 'application'
application = service.Application("stripe_server")

# this hooks the collection we made to the application
top_service.setServiceParent(application)

