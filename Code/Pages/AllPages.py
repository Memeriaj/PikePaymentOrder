from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File
from Restful import RESTfulAPIResource

root = File('./HTML')
root.putChild("Data", RESTfulAPIResource())
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()