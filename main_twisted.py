from simple_json import dumps
from twisted.web import resource
from twisted.internet import reactor, task

from twisted.application import service
from twisted.web import server

#from temperature import read_temp
from time import time

sets = {}
sets['balbula_1'] = True
input1 = 0.0


class DataResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        return dumps({'time': time(), 'balbula_1': sets['balbula_1'], 'input1': input1})


class Set(resource.Resource):
    isLeaf = True

    def render_POST(self, request):
        variable = request.args['var'][0]
        sets[variable] = not sets[variable]
        return ''


def f():
    global input1
    input1 -= 1
    input1 += sets['balbula_1']*2
    #input1 = read_temp() or input1

t = task.LoopingCall(f)
t.start(1.0)

root = resource.Resource()
root.putChild('data', DataResource())
root.putChild('set', Set())

application = service.Application('SCADA')
service = reactor.listenTCP(8080, server.Site(root))
application.addComponent(service)
if __name__ == '__main__':
    reactor.run()
