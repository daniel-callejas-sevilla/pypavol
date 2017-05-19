#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSlider, QCheckBox, QApplication
from PyQt5.QtCore import Qt

import pulsectl

pulse = pulsectl.Pulse('PyPaVol') # TODO get rid of global object

# temp method for the demo; final solution must populate from pulseaudio events
# TODO can a track go to multiple sinks? if so, format of returned tracks needs to evolve
def get_tracks():
    tracks = []
    for t in pulse.sink_input_list():
        track = (t.proplist['application.name'], t.sink, 100 * t.volume.value_flat)
        tracks.append(track)
    return tracks

def get_sinks():
    sinks = []
    for s in pulse.sink_list():
        sink = (s.description, 100 * s.volume.value_flat)
        sinks.append(sink)
    return sinks

class PyPaVol_demo(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        tracks = get_tracks()
        sinks = get_sinks()
        
        for i, track in enumerate(tracks):
            print(i, track)
            name, sink, vol = track
            l = QLabel(name)
            l.setMaximumWidth(80)
            l.setMinimumWidth(80)
            grid.addWidget(l, 0, i)
            for j, _ in enumerate(sinks):
                c = QCheckBox(self)
                c.setChecked(j == sink)
                grid.addWidget(c, j + 1, i)
            s = QSlider(Qt.Vertical, self)
            s.setMaximum(153)
            s.setMinimum(0)
            s.setValue(vol)
            grid.addWidget(s, len(sinks) + 2, i)
            l = QLabel(str(vol))
            l.setMaximumWidth(80)
            l.setMinimumWidth(80)
            grid.addWidget(l, len(sinks) + 3, i)
            
        skip_h = len(tracks) + 1
        skip_v = len(sinks) + 1
        
        for i, sink in enumerate(sinks):
            name, vol = sink
            l = QLabel(name)
            grid.addWidget(l, skip_v, skip_h + i)
            s = QSlider(Qt.Vertical, self)
            s.setMaximum(153)
            s.setMinimum(0)
            s.setValue(vol)
            grid.addWidget(s, skip_v + 1, skip_h + i)
                    
        self.setWindowTitle('PyPaVol')
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyPaVol_demo()
    sys.exit(app.exec_())
    


