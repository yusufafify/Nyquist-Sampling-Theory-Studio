import numpy as np
import random
from pyqtgraph import PlotWidget


class composerSignal():
    def __init__(self):
        self.frequency=0
        self.amplitude=0
        self.phaseShift=0
        self.plotRef=PlotWidget()
    def savedata(self,freq,amp,phase):
        self.frequency=freq
        self.amplitude=amp
        self.phaseShift=phase