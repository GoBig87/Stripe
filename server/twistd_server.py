from twisted.application import internet, service
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.python import log
import ast
import os
import stripe

_stripe_api_key = "your key here"
stripe.api_key = _stripe_api_key

#copied from stack over flow, it works dont touch
class NodeProtocol(Protocol):
    nodeDataDict = ''

    def dataReceived(self, data):
        log.msg(data)
        dataString = str(data)
        self.deferred = self.factory.service.check_data(dataString)
        self.transport.write(self.factory.service.status)
        self.transport.loseConnection()
#copied from stack over flow, it works dont touch
#copied from stack over flow, it works dont touch
class NodeFactory(ServerFactory):

    protocol = NodeProtocol

    def __init__(self, service):
        self.service = service

    def data_finished(self, nodeData):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.callback(nodeData)
#copied from stack over flow, it works dont touch

class NodeService(service.Service):
    #Begin touching stuff
    def __init__(self):
        self.customertoken = ''
        self.customeremail = ''

    def startService(self):
        service.Service.startService(self)

    def check_data(self, data):
        self.clientDict = None
        log.msg(data)
        try:
            self.clientDict = ast.literal_eval(data)
        except:
            pass

        if "function" in self.clientDict.keys():
            function = self.clientDict['function']
            if function == 'client_token':
                self.processCustomer(self.clientDict)
            if function == 'Create_Charge':
                self.createCharge(self.clientDict)
        else:
            log.msg('Error 101. No valid argument presented.')

    def processCustomer(self,dict):
        #Dict Format
        #{"function": "client_token", "token":token, "email":"email"}
        self.customertoken = dict['client_token']
        self.customeremail = dict['email']

    def createCharge(self,dict):
        #Dict Format
        #{"function": "Create_Charge", "amount":amount, "email":"email"}
        customerToken = self.customertoken
        amountCharged = dict['amount']
        charge = stripe.Charge.create(amount=amountCharged, currency='usd', description='Add info here', customer=customerToken, capture=False)
        if charge["status"] == "succeeded":
            msg = self.Cipher.encrypt('{"rsp":"succeeded"}')
        else:
            msg = self.Cipher.encrypt('{"rsp":"failed"}')

        self.status = msg

port = 8080 #edit your port here
#ifacev4 = '0.0.0.0'
iface = '::0' #edit your ip address here
#This is as far as you go! Now stop touching stuff!!!

#copied from stack over flow, it works dont touch
top_service = service.MultiService()
node_service = NodeService()
node_service.setServiceParent(top_service)
factory = NodeFactory(node_service)
tcp_service = internet.TCPServer(port, factory, interface=iface)
tcp_service.setServiceParent(top_service)
application = service.Application("stripe_server")
top_service.setServiceParent(application)
#copied from stack over flow, it works dont touch
