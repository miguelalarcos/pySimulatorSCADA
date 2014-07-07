from simple_json import dumps
from twisted.web import resource
from twisted.internet import reactor, task

from twisted.application import service
from twisted.web import server

#from temperature import read_temp
from time import time
from random import random

sets = {}
sets['balbula_1'] = True
sets['control'] = False
input1 = 50.0


class DataResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        return dumps({'time': time(), 'control': sets['control'], 'balbula_1': sets['balbula_1'], 'input1': input1})


def setUnset(variable):
    sets[variable] = not sets[variable]

class Set(resource.Resource):
    isLeaf = True

    def render_POST(self, request):
        variable = request.args['var'][0]
        setUnset(variable)
        return ''


def simulacion():
    global input1
    input1 -= 1

    input1 += sets['balbula_1']*2 
    #input1 = read_temp() or input1
    print input1

t = task.LoopingCall(simulacion)


def f2():
    global input1
    if not sets['control']:
        if input1 <= 50:
            sets['balbula_1'] = True
        else:
            sets['balbula_1'] = False

t2 = task.LoopingCall(f2)


root = resource.Resource()
root.putChild('data', DataResource())
root.putChild('set', Set())

application = service.Application('SCADA')
service = reactor.listenTCP(8080, server.Site(root))
application.addComponent(service)

if __name__ == '__main__':
    t.start(0.5)
    t2.start(1.0)
    reactor.run()
