import socket
import sys

import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
from pyqtgraph.Qt import QtCore, QtGui

# 設定socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
PORT = 1234
s.bind(('0.0.0.0', PORT))
print('Listening for broadcast at ', s.getsockname())

# 宣告必要全域變數
EMG_data_list = []
gry_data = []
gry_curves = []
sample_count = 0

# 建立pyqtgraph
win = pg.GraphicsLayoutWidget(show=True)
win.resize(1200, 700)
EMG_plot = win.addPlot(title="EMG curves", row=1, col=0)
GYO_plot = win.addPlot(title="GYO curves", row=2, col=0)
EMG_curve = EMG_plot.plot(pen=(255, 255, 0))
# 預先建立陀螺儀曲線
for i in range(1, 7):
    curve = pg.PlotCurveItem(pen=(np.random.randint(100, 255)))
    GYO_plot.addItem(curve)
    gry_curves.append(curve)


def update1():
    _temp = []
    global sample_count,  EMG_data_list, gry_data
    s_t = time()
    # 這裡採用while是為了避免每一筆資料就重新繪製導致的效能浪費
    # 但過少次數從新繪製會導致感測器資料與sample數量對不上(延遲感)
    # 建議收集超過五筆以上更新圖表比較好
    while len(_temp) <= 8:
        sample_count += 1
        raw_data = s.recv(50)  # 感測器資料長度通常不超過50
        _temp.append(raw_data)
        # 解析資料
        EMG_and_MPU6050 = raw_data.decode().split(" ")
        EMG_data_list.append(int(EMG_and_MPU6050[0]))
        gy_data_1 = float(EMG_and_MPU6050[1])
        gy_data_2 = float(EMG_and_MPU6050[2])
        gy_data_3 = float(EMG_and_MPU6050[3])
        gy_data_4 = float(EMG_and_MPU6050[4])
        gy_data_5 = float(EMG_and_MPU6050[5])
        gy_data_6 = float(EMG_and_MPU6050[6].replace('\x00', ''))
        gry_data.append([gy_data_1, gy_data_2, gy_data_3,
                         gy_data_4, gy_data_5, gy_data_6])

    # 繪製資料，可依據顯示寬幅調整
    EMG_curve.setData(EMG_data_list[-300:])
    EMG_curve.setPos(sample_count, 0)

    # 根據每一條線去繪製
    for j in range(6):
        _gry_temp = []
        for k in range(len(gry_data)):
            _gry_temp.append(gry_data[k][j])
        gry_curves[j].setData(_gry_temp[-300:])
        gry_curves[j].setPos(sample_count, 0)
    EMG_plot.setTitle('%0.2f fps' % (1//(time()-s_t)))

    # 清除不必要的舊資料
    if len(gry_data) > 500:
        del gry_data[:-500]
        del EMG_data_list[:-500]


def update():
    update1()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1)
if __name__ == '__main__':

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
