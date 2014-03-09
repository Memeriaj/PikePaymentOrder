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
        printDetails(request)
        return json.dumps(self.type.get(self.type.id == self.id), cls=TablesEncoder)
    
    def render_DELETE(self, request):
        printDetails(request)
        self.type.get(self.type.id == self.id).delete_instance()
        return '<html><body></body></html>'

class DataPage(Resource):
    def __init__(self, type):
        Resource.__init__(self)
        self.type = type

    def render_GET(self, request):
        allData = []
        printDetails(request)
        for data in self.type.select():
            allData.append(data)
        return json.dumps(allData, cls=TablesEncoder)
    
    def render_POST(self, request):
        printDetails(request)
        print self.type
        possibleAttribute = self.type().checkNotInNewDictionary(request.args)
        if possibleAttribute:
            request.setResponseCode(400)
            return '<html><body>"'+possibleAttribute+'" is needed.</body></html>'
        id = self.type().createNew(request.args)
        return '<html><body>'+str(id)+'</body></html>'
    
    def getChild(self, name, request):
        return IndividualDataPage(self.type, int(name))
    
def printDetails(request):
    print 'method: '+str(request.method)
    print 'uri: '+str(request.uri)
    print 'path: '+str(request.path)
    print 'args: '+str(request.args)
    print 'request headers: '+str(request.requestHeaders)
    print 'headers: '+str(request.headers)

def RESTfulAPIResource():
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
    return data


# print Department.get(Department.id == 14)