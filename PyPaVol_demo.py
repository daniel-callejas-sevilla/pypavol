#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSlider, QRadioButton, QApplication, QButtonGroup
from PyQt5.QtGui import QPixmap, QPainter, QPen
import PyQt5.QtCore
import textwrap
from functools import partial

import pulsectl

pulse = pulsectl.Pulse('PyPaVol') # TODO get rid of global object

# temp method for the demo; final solution must populate from pulseaudio events
# TODO can a track go to multiple sinks? if so, format of returned tracks needs to evolve
def get_tracks():
    tracks = []
    for t in pulse.sink_input_list():
        track = (t.proplist['application.name'], t.sink, int(100 * t.volume.value_flat), t)
        tracks.append(track)
    return tracks

def get_sinks():
    sinks = []
    for s in pulse.sink_list():
        sink = (textwrap.shorten(s.description, width=18), int(100 * s.volume.value_flat), s)
        sinks.append(sink)
    return sinks

class Corner(QWidget):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
    
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(PyQt5.QtCore.Qt.black, 1)
        pen.setDashPattern([1, 1])
        painter.setPen(pen)
        half_width, half_height = self.width() / 2, self.height() / 2
        full_width, full_height = self.width(), self.height()
        if self.x < self.y:    # ──
            painter.drawLine(0, half_height, full_width, half_height)
        elif self.x == self.y: # ───┐
            painter.drawLine(0, half_height, half_width, half_height)
            painter.drawLine(half_width, half_height, half_width, full_height)
        else:                  #    │
            painter.drawLine(half_width, 0, half_width, full_height)
        painter.end()

class PyPaVol_demo(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def setVolume(self, o, volume):
        vol = volume / 100
        # TODO assumes two channels
        v = pulsectl.PulseVolumeInfo([vol, vol])
        pulse.volume_set(o, v)

    def setSink(self, track, sink, connect):
        if connect:
            print("Send track {} to sink {}".format(track, sink))
            pulse.sink_input_move(track.index, sink.index)            
    
    def initUI(self):
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        self.setLayout(grid)
        
        tracks = get_tracks()
        sinks = get_sinks()
        
        # TODO clean up this mess
        for i, track in enumerate(tracks):
            print(i, track)
            name, sink, vol, o = track
            l = QLabel(name)
            grid.addWidget(l, 0, i, PyQt5.QtCore.Qt.AlignHCenter)
            bgr = QButtonGroup(self)
            for j, a_sink in enumerate(sinks):
                c = QRadioButton(self)
                bgr.addButton(c)
                c.setChecked(j == sink)
                _, _, sink_o = a_sink
                c.toggled.connect(partial(self.setSink, o, sink_o))
                grid.addWidget(c, j + 1, i, PyQt5.QtCore.Qt.AlignHCenter)
            s = QSlider(PyQt5.QtCore.Qt.Vertical, self)
            s.setMaximum(153)
            s.setMinimum(0)
            s.setValue(vol)
            s.valueChanged.connect(partial(self.setVolume, o))
            grid.addWidget(s, len(sinks) + 2, i, PyQt5.QtCore.Qt.AlignHCenter)
            l = QLabel(str(vol))
            grid.addWidget(l, len(sinks) + 3, i, PyQt5.QtCore.Qt.AlignHCenter)
            
        skip_h = len(tracks)
        skip_v = len(sinks) + 1
        
        for i, sink in enumerate(sinks):
            name, vol, o = sink
            l = QLabel(name)
            pos = skip_h + len(sinks) - i - 1
            grid.addWidget(l, skip_v, pos)
            s = QSlider(PyQt5.QtCore.Qt.Vertical, self)
            s.setMaximum(153)
            s.setMinimum(0)
            s.setValue(vol)
            s.valueChanged.connect(partial(self.setVolume, o))
            grid.addWidget(s, skip_v + 1, pos, PyQt5.QtCore.Qt.AlignHCenter)
            l = QLabel(str(vol))
            grid.addWidget(l, skip_v + 2, pos, PyQt5.QtCore.Qt.AlignHCenter)

        blocks = [(x, y) for x in range(skip_h, skip_h + len(sinks)) 
                         for y in range(1, skip_v)]
        
        for x, y in blocks:
            l = Corner(x - skip_h + 1, skip_v - y)
            grid.addWidget(l, y, x)
        
        print(blocks)
                    
        self.setWindowTitle('PyPaVol')
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyPaVol_demo()
    sys.exit(app.exec_())
    


