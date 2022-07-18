import asyncio
from http.client import GONE
import websockets
import json
import pyqtgraph as pg
from websocket import create_connection
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui


ws = create_connection("ws://192.168.1.37/")
global data
data = []
temp = []

win = pg.GraphicsLayoutWidget(show=True)
p2 = win.addPlot()

ptr1 = 0
curve2 = p2.plot(temp)


def update1():
    global ptr1, temp, data
    while len(data) < 1:
        result = ws.recv()
        data.append(int(result))
        temp.append(int(result))
    data1 = temp[-1000:]
    curve2.setData(data1)
    curve2.setPos(ptr1, 0)
    data = []
    # data[:-1] = data[1:]  # shift data in the array one sample left
    # data[-1] = data
    ptr1 += 1


def update():
    update1()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
