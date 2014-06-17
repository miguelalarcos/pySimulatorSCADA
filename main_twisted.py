from simple_json import dumps
from twisted.web import resource
from twisted.internet import reactor, task

from twisted.application import service
from twisted.web import server

balbula_1 = True
input1 = 100


class DataResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader("content-type", "application/json")
        return dumps({'balbula_1': balbula_1, 'input1': input1})


class SetBalbula_1(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        global balbula_1
        value = request.args['value'][0]
        if value == '0':
            balbula_1 = False
        else:
            balbula_1 = True
        return ''


def f():
    global input1
    input1 -= 1
    input1 += balbula_1*2
    print input1

t = task.LoopingCall(f)
t.start(1.0)

root = resource.Resource()
root.putChild('data', DataResource())
root.putChild('set_balbula_1', SetBalbula_1())

application = service.Application('SCADA')
service = reactor.listenTCP(8080, server.Site(root))
print dir(application)
application.addComponent(service)
#reactor.run()
