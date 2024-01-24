from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QPushButton
import pyqtgraph
import functions
import Utility
import numpy as np

def initConnectors(self):

    #finds combo box that saves signals same idea as channel selector
    signalsaver=self.findChild(QtWidgets.QComboBox,"composerSignalSaver")
    signalsaver.currentIndexChanged.connect(lambda:functions.signalselector(self,signalsaver,frequencyselector,Amplitudeselector,PhaseShiftselector,addtiongraph,valueoffreq,valueofamp,valueofphase))

    #deletes one of the signals added
    signalremover=self.findChild(QtWidgets.QPushButton,"deleteComposerSignal")
    signalremover.clicked.connect(lambda:functions.removeSignal(self,totalSignals,signalsaver))

    #sets the frequency
    frequencyselector=self.findChild(QtWidgets.QSlider, "FrequencySlider")
    frequencyselector.setRange(1, 100)
    frequencyselector.valueChanged.connect(lambda: functions.compose_signal(self,frequencyselector,Amplitudeselector,PhaseShiftselector,addtiongraph,valueoffreq,valueofamp,valueofphase))

    # sets the Amplitude
    Amplitudeselector = self.findChild(QtWidgets.QSlider, "AmplitudeSlider")
    Amplitudeselector.setRange(1, 100)
    Amplitudeselector.valueChanged.connect(lambda: functions.compose_signal(self,frequencyselector,Amplitudeselector,PhaseShiftselector,addtiongraph,valueoffreq,valueofamp,valueofphase))

    # sets the PhaseShift
    PhaseShiftselector = self.findChild(QtWidgets.QSlider, "PhaseShiftSlider")
    PhaseShiftselector.setRange(0, 360)
    PhaseShiftselector.valueChanged.connect(lambda: functions.compose_signal(self,frequencyselector,Amplitudeselector,PhaseShiftselector,addtiongraph,valueoffreq,valueofamp,valueofphase))

    # sends signal to other graph
    sendsignal=self.findChild(QtWidgets.QPushButton,"sendComposerSignal")
    sendsignal.clicked.connect(lambda:functions.sendSignal(self,originalSignalViewPort,reconstructedSignalViewPort,differenceBetweenSignalsViewPort,sampleController,sampleRatioLabel,fmaxradio,hertzradio,SNRcontrol,SNRnumber))

    #Add Signal Button
    addSignal=self.findChild(QtWidgets.QPushButton,"saveComposerSignal")
    addSignal.clicked.connect(lambda:functions.addSignal(self,totalSignals,signalsaver,frequencyselector,Amplitudeselector,PhaseShiftselector))

    #contains graph that has signals to be added
    addtiongraph=self.findChild(PlotWidget,"signalToBeAddedGraph")
    totalSignals=self.findChild(PlotWidget,"AdditionOfAllSignalGraphs")

    # next three lines are labels used to define numbers of stuff
    valueoffreq=self.findChild(QtWidgets.QLabel,"ValueofFrequency")
    valueofamp = self.findChild(QtWidgets.QLabel, "valueOfAmplitude")
    valueofphase = self.findChild(QtWidgets.QLabel, "valueOfPhaseShift")

    #viewer section
    #original graph drawn
    originalSignalViewPort=self.findChild(pyqtgraph.PlotWidget, "Originaldrawinggraph")
    reconstructedSignalViewPort=self.findChild(pyqtgraph.PlotWidget, "reconstrudctedDrawingGraph")
    differenceBetweenSignalsViewPort=self.findChild(pyqtgraph.PlotWidget,"differenceGraph")

    #sets the Sample slider
    sampleController=self.findChild(QtWidgets.QSlider, "sampleSliderControl")
    sampleController.setMinimum(0)
    sampleController.setMaximum(40)
    sampleController.setValue(1)
    sampleController.setTickInterval(1)
    sampleController.valueChanged.connect(lambda: Utility.sampleAndInterpolate(self,originalSignalViewPort,reconstructedSignalViewPort,differenceBetweenSignalsViewPort,sampleController,sampleRatioLabel,functions.ComposedSignal,functions.maxFreq,functions.snr_signal,fmaxradio,hertzradio))

    sampleRatioLabel=self.findChild(QtWidgets.QLabel, "sampleRatioNumber")
    loadCsv=self.findChild(QtWidgets.QPushButton,"browseSignal")
    loadCsv.clicked.connect(lambda:functions.browse(self,originalSignalViewPort,reconstructedSignalViewPort,differenceBetweenSignalsViewPort,sampleController,sampleRatioLabel,fmaxradio,hertzradio,SNRcontrol,SNRnumber))

    clearallbutton=self.findChild(QtWidgets.QPushButton,"clearAllSignals")
    clearallbutton.clicked.connect(lambda:functions.clearall(self,totalSignals,signalsaver))

    # actualsamplecontrol=self.findChild(QtWidgets.QSlider,"realFrequencyControl")
    # actualsamplecontrol.setMinimum(1)
    # actualsamplecontrol.setMaximum(10)
    # actualsamplecontrol.setValue(1)
    # actualsamplecontrol.setTickInterval(1)
    # actualsamplecontrol.valueChanged.connect(lambda: Utility.sampleAndInterpolate(self, originalSignalViewPort, reconstructedSignalViewPort,differenceBetweenSignalsViewPort,actualsamplecontrol,sampleController, sampleRatioLabel,functions.ComposedSignal, functions.maxFreq, actualfrequency))

    fmaxradio=self.findChild(QtWidgets.QRadioButton,"fmaxRadio")
    fmaxradio.setChecked(True)
    # fmaxradio.toggled.connect(lambda: functions.applychanges(fmaxradio,hertzradio,sampleController,sampleRatioLabel))
    hertzradio = self.findChild(QtWidgets.QRadioButton, "hertzRadio")
    hertzradio.toggled.connect(lambda: functions.applychanges(fmaxradio, hertzradio, sampleController, sampleRatioLabel))

    SNRcontrol = self.findChild(QtWidgets.QSlider, "SNRsliderControl")
    SNRcontrol.setMinimum(0)
    SNRcontrol.setMaximum(50)
    SNRcontrol.setValue(50)
    SNRcontrol.valueChanged.connect(
        lambda: functions.changeSNR(self, originalSignalViewPort, reconstructedSignalViewPort,
                                    differenceBetweenSignalsViewPort, sampleController, SNRcontrol,
                                    sampleRatioLabel, SNRnumber,fmaxradio,hertzradio))

    SNRnumber = self.findChild(QtWidgets.QLabel, "SNRRatioNumber")
    SNRnumber.setText("50 db")

    exportSignalbtn = self.findChild(QtWidgets.QPushButton, "saveSignal")
    exportSignalbtn.clicked.connect(lambda: functions.export_summed_signal(self))

    hidesamples=self.findChild(QtWidgets.QPushButton,"hideSamples")
    hidesamples.clicked.connect(lambda: Utility.hidesample())