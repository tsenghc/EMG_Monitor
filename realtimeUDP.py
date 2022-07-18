import socket
import json
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import time



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
PORT = 1234
s.bind(('0.0.0.0', PORT))
print('Listening for broadcast at ', s.getsockname())

EMG_data_list = []
gry_data = []

gry_curves = []
ptr1 = 0

win = pg.GraphicsLayoutWidget(show=True)
pg.setConfigOptions(antialias=True)

win.resize(1200, 700)
p1 = win.addPlot(title="EMG curves", row=1, col=0)
p2 = win.addPlot(title="GYO curves", row=2, col=0)

curve1 = p1.plot(pen=(255, 255, 0))


for i in range(1, 7):
    curve = pg.PlotCurveItem(pen=(np.random.randint(255)))
    p2.addItem(curve)
    gry_curves.append(curve)


start_time = time.time()

temp = []


def update1():
    global ptr1,  EMG_data_list, gry_data, temp
    while len(temp) < 10:
        raw_data, address = s.recvfrom(1024)
        EMG_and_MPU6050 = raw_data.decode().split(" ")
        temp.append(EMG_and_MPU6050)
        ptr1 += 1
        EMG_data = int(EMG_and_MPU6050[0])
        gy_data_1 = float(EMG_and_MPU6050[1])
        gy_data_2 = float(EMG_and_MPU6050[2])
        gy_data_3 = float(EMG_and_MPU6050[3])
        gy_data_4 = float(EMG_and_MPU6050[4])
        gy_data_5 = float(EMG_and_MPU6050[5])
        gy_data_6 = float(EMG_and_MPU6050[6].replace('\x00', ''))
        gry_data.append([gy_data_1, gy_data_2, gy_data_3,
                         gy_data_4, gy_data_5, gy_data_6])

        EMG_data_list.append(EMG_data)

    curve1.setData(EMG_data_list[-100:])
    curve1.setPos(ptr1, 0)

    for j in range(6):
        _gry_temp = []
        for k in range(len(gry_data)):
            _gry_temp.append(gry_data[k][j])
        gry_curves[j].setData(_gry_temp[-100:])
        gry_curves[j].setPos(ptr1, 0)

    temp = []


def update():
    update1()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
