import daemon
from flask import Flask, jsonify
from multiprocessing import Process, Value
from time import sleep, time
from math import sin

balbula_1 = True
input1 = Value('d', 100.0)

app = Flask(__name__)

@app.route("/data")
def data():
    return jsonify(**{'balbula_1': balbula_1, 'input1': input1.value})

@app.route("/set_balbula_1/<int:value>")
def set_balbula_1(value):
    global balbula_1
    balbula_1 = bool(value)
    return ''


def f(input1):
    while True:
        sleep(1)
        input1.value = 50 + 50*sin(time()/10)
       

if __name__ == "__main__":
    with daemon.DaemonContext():
        Process(target=f, args=(input1,)).start()
        app.run(host='0.0.0.0')

