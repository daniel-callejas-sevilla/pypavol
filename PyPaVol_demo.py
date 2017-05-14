#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSlider, QCheckBox, QApplication
from PyQt5.QtCore import Qt
import random

class PyPaVol_demo(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        tracks = [ ["Amarok",     [0, 1, 0, 0], 100],
                   ["Chrome",     [0, 0, 1, 0], 100],
                   ["Half-Life",  [0, 0, 0, 1], 100],
                   ["VLC",        [0, 0, 1, 0], 100],
                   ["USB Webcam", [0, 0, 0, 0], 100],
                   ["M2496 Line", [1, 0, 0, 0], 100],
                   ["Intel Line", [0, 0, 0, 0], 100]
                 ]
        sinks = [ ["Intel",    30],
                     ["M2496",    50],
                     ["La Tele", 100],
                     ["Ardour",  100]
                   ]
        
        for i, track in enumerate(tracks):
            print(i, track)
            name, patches, vol = track
            l = QLabel(name)
            l.setMaximumWidth(80)
            l.setMinimumWidth(80)
            grid.addWidget(l, 0, i)
            for j, p in enumerate(patches):
                c = QCheckBox(self)
                c.setChecked(p == 1)
                grid.addWidget(c, j + 1, i)
            s = QSlider(Qt.Vertical, self)
            s.setValue(vol)
            grid.addWidget(s, len(patches) + 2, i)
            
        skip_h = len(tracks) + 1
        skip_v = len(sinks) + 1
        
        for i, sink in enumerate(sinks):
            name, vol = sink
            l = QLabel(name)
            grid.addWidget(l, skip_v, skip_h + i)
            s = QSlider(Qt.Vertical, self)
            s.setValue(vol)
            grid.addWidget(s, skip_v + 1, skip_h + i)
                    
        self.setWindowTitle('PyPaVol')
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyPaVol_demo()
    sys.exit(app.exec_())
    


