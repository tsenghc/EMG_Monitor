# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import csv

data = []
with open('emgsingle-1611092797.csv', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',')
    for i in rows:
        data.append(i[1])

del data[0]
data = [int(i) for i in data]
win = pg.GraphicsLayoutWidget(show=True)
# p1 = win.addPlot()
p2 = win.addPlot()
data1 = data[:100]

# curve1 = p1.plot(data1)
curve2 = p2.plot(data1)
ptr1 = 0


def update1():
    global data1, ptr1
    data1[:-1] = data1[1:]  # shift data in the array one sample left
    data1[-1] = data[100+int(ptr1)]
    ptr1 += 1
    # curve1.setData(data1)

    curve2.setData(data1)
    curve2.setPos(ptr1, 0)


# 3) Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 500
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()
win.nextRow()
p5 = win.addPlot(colspan=2)
p5.setLabel('bottom', 'Time', 's')
p5.setXRange(-20, 0)
curves = []
data5 = np.empty((chunkSize+1,2))
ptr5 = 0

def update3():
    global p5, data5, ptr5, curves
    now = pg.ptime.time()
    for c in curves:
        c.setPos(-(now-startTime), 0)
    
    i = ptr5 % chunkSize
    if i == 0:
        curve = p5.plot()
        curves.append(curve)
        last = data5[-1]
        data5 = np.empty((chunkSize+1,2))        
        data5[0] = last
        while len(curves) > maxChunks:
            c = curves.pop(0)
            p5.removeItem(c)
    else:
        curve = curves[-1]
    data5[i+1,0] = now - startTime
    data5[i+1,1] = data[int(ptr5)]
    curve.setData(x=data5[:i+2, 0], y=data5[:i+2, 1])
    ptr5 += 1


def update():
    update1()
    update3()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
