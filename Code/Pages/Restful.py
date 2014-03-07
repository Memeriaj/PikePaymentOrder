from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from Code.Database.Tables import *
import json
    
class IndividualDataPage(Resource):
    isLeaf = True
    def __init__(self, type, id):
        Resource.__init__(self)
        self.type = type
        self.id = id
        
    def render_GET(self, request):
        return json.dumps(self.type.get(self.type.id == self.id), cls=TablesEncoder)

class DataPage(Resource):
    def __init__(self, type):
        Resource.__init__(self)
        self.type = type
    
    def render_GET(self, request):
        allData = []
        for data in self.type.select():
            allData.append(data)
        return json.dumps(allData, cls=TablesEncoder)
    
    def getChild(self, name, request):
        return IndividualDataPage(self.type, int(name))

data = Resource()
data.putChild("User", DataPage(User))
data.putChild("Quarter", DataPage(Quarter))
data.putChild("Department", DataPage(Department))
data.putChild("Chairmen", DataPage(Chairmen))
data.putChild("PaymentOrder", DataPage(PaymentOrder))
data.putChild("LineItem", DataPage(LineItem))
data.putChild("Receipt", DataPage(Receipt))
data.putChild("LineReceipt", DataPage(LineReceipt))
data.putChild("Approvals", DataPage(Approvals))
root = Resource()
root.putChild("Data", data)
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()