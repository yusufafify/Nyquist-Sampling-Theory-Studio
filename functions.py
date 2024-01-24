from PyQt5 import QtGui, QtCore, QtWidgets
import csv
from PyQt5.QtWidgets import QFileDialog, QColorDialog,QMessageBox
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import numpy as np
from classes import composerSignal
import pandas as pd
import random
import os
import wfdb
from classes import composerSignal
from functools import partial
from random import randint
from scipy.signal import resample
import Utility
import pyqtgraph


arrayOfSignalsData=[]
arrayOfComposerSignals=[]
dummySignal=[]
ComposedSignal=[]
maxFreq=0
maxFreqOfComposer=0
addedsignals=[]
snr_signal=ComposedSignal

def compose_signal(self,frequencyselector,Amplitudeselector,PhaseShiftselector,addtiongraph,valueoffreq,valueofamp,valueofphase):
    global dummySignal
    #Callling a dummy array to avoid overriding frequency variable
    dummyArray = []
    #Callling data to set values in slider and draw signal
    frequency = frequencyselector.value()
    magnitude = Amplitudeselector.value()
    phase = PhaseShiftselector.value()

    #for better optimzation made a function that set the labels of the slider
    Utility.setSliderLabelText(valueoffreq,valueofamp,valueofphase,frequency,magnitude,phase)

    # Generate a signal based on the slider values
    t = np.linspace(0, 3, 3000, endpoint=False)
    # for better optimzation made a function that generates a sin signal
    signal = Utility.generateSinSignal(t,magnitude,phase,frequency)

    #setting dummy signal to pass to add signal
    dummySignal=signal
    # Plot the composed signal in Graph 1
    addtiongraph.clear()
    addtiongraph.plot(t, signal, pen='b', name='Composed Signal')


def signalselector(self,signalsaver,frequencyselector,Amplitudeselector,PhaseShiftselector,addtiongraph,valueoffreq,valueofamp,valueofphase):
    global arrayOfSignalsData
    global arrayOfComposerSignals
    index=signalsaver.currentIndex()
    if index<0:
        return
    #setting slider values to selected signal

    frequencyselector.setValue(arrayOfSignalsData[index].frequency)
    Amplitudeselector.setValue(arrayOfSignalsData[index].amplitude)
    PhaseShiftselector.setValue(arrayOfSignalsData[index].phaseShift)
    Utility.setSliderLabelText(valueoffreq,valueofamp,valueofphase,arrayOfSignalsData[index].frequency,arrayOfSignalsData[index].amplitude,arrayOfSignalsData[index].phaseShift)

    addtiongraph.clear()
    t = Utility.generateLinspace3000()
    addtiongraph.plot(t,arrayOfComposerSignals[index],pen='b')

def addSignal(self,totalSignals,signalsaver,frequencyselector,Amplitudeselector,PhaseShiftselector):
    global arrayOfComposerSignals
    global dummySignal
    global addedsignals
    global maxFreqOfComposer
    global arrayOfSignalsData
    # tell the user that there is no signal
    if not any(dummySignal):
        QMessageBox.warning(self,'No Signal', 'There is No signal constructed')
        return
    dummy=composerSignal()
    #using the only value in the dummy array that has the latest frequency set in the sin composer
    arrayOfComposerSignals.append(dummySignal)
    arrayOfSignalsData.append(dummy)
    arrayOfSignalsData[-1].savedata(frequencyselector.value(),Amplitudeselector.value(),PhaseShiftselector.value())
    signalsaver.addItem(f"Signal {signalsaver.count()+1}")
    #check if the latest signal has the highest frequency or not
    maxFreqOfComposer= Utility.findMaxFrequencyOfComposer(arrayOfSignalsData)
    #after that clearing the totalsignal vireport to take the new combined sin waves
    totalSignals.clear()
    addedsignals=0
    for i in arrayOfComposerSignals:
        addedsignals+=i
    

    t = Utility.generateLinspace3000()
    totalSignals.plot(t,addedsignals, pen='b')

def removeSignal(self,totalSignals,signalsaver):
    global arrayOfComposerSignals
    global addedsignals
    global maxFreqOfComposer

    global arrayOfSignalsData

    

    # tell the user that there is no signal
    if len(arrayOfComposerSignals) == 0:
        QMessageBox.warning(self,'No Signal', 'There is No signals to be deleted')
        return
    #ask the user if they're sure they want to delete the signal
    choice=QMessageBox.warning(self,'Delete', 'Are you sure you want to delete this signal?',QMessageBox.Yes|QMessageBox.No)

    if(choice == QMessageBox.No):
        return
    #get signal and remove it from array
    signaltoberemoved=arrayOfComposerSignals[signalsaver.currentIndex()]
    del arrayOfComposerSignals[signalsaver.currentIndex()]
    del arrayOfSignalsData[signalsaver.currentIndex()]
    #remove the signal from total signal
    addedsignals=addedsignals-signaltoberemoved
    totalSignals.clear()
    maxFreqOfComposer= Utility.findMaxFrequencyOfComposer(arrayOfSignalsData)
    t = np.linspace(0, 3, 3000)
    if len(arrayOfComposerSignals)==0:
        totalSignals.clear()
        addedsignals=[]
    else:
        totalSignals.plot(t, addedsignals, pen='b')
    signalsaver.removeItem(signalsaver.currentIndex())
    for i in range(signalsaver.currentIndex(), signalsaver.count()):
        item_text = signalsaver.itemText(i)
        signalsaver.setItemText(i, f"Signal {i + 1}")
    # Reset the selection if an item was removed
    if signalsaver.currentIndex() < signalsaver.count():
        signalsaver.setCurrentIndex(signalsaver.currentIndex())
    else:
        signalsaver.setCurrentIndex(signalsaver.count() - 1)


def sendSignal(self,viewportup,viewportmiddle,viewportdown,sampleController,sampleRatioNumber,fmaxradio,hertzradio,SNRcontrol,SNRnumber):

    global ComposedSignal
    global addedsignals
    global maxFreq
    global maxFreqOfComposer
    global snr_signal
    #tell the user that there is no signal
    if len(addedsignals)==0:
        QMessageBox.warning(self, "Warning!", "There is no signal composed to be sent")
        return
    #ask the user if they're sure they want to send the signal
    choice = QMessageBox.warning(self, "Warning! Send Signal",
                                 "Adding a new signal will clear the existing signal. Do you want to continue? ",
                                 QMessageBox.Yes | QMessageBox.No)
    if (choice == QMessageBox.No):
        return
    #putting data in composed and maxfreq to use later in viewer tab
    ComposedSignal=addedsignals
    maxFreq=maxFreqOfComposer

    #generating a new linspace for the total time of the signal
    t = Utility.generateLinspace3000()
    if not len(snr_signal) == 0:
        changeSNR(self,viewportup,viewportmiddle,viewportdown,sampleController,SNRcontrol,sampleRatioNumber,SNRnumber,fmaxradio,hertzradio)

    else:
        #plotting the total composed signal
        Utility.draw3Graphs(self,viewportup, viewportmiddle,viewportdown,sampleController,sampleRatioNumber,ComposedSignal,maxFreq,snr_signal,fmaxradio,hertzradio)
    #send user to viewer tab to see the signal
    self.ChangeBetweenApps.setCurrentIndex(1)



def browse(self, viewportup, viewportmiddle, viewportdown, sampleController, sampleRatioNumber,fmaxradio,hertzradio,SNRcontrol,SNRnumber):
    global ComposedSignal
    global maxFreq
    global snr_signal
    #ask the user whether they're sure they want to override the signal
    choice = QMessageBox.warning(self, "Warning! Browse Signal",
                                 "Loading a new signal will clear the existing signal. Do you want to continue? ",
                                 QMessageBox.Yes | QMessageBox.No)
    if (choice == QMessageBox.No):
        return
    
    self.filename, _ = QFileDialog.getOpenFileName(None, 'Open the signal file', './', filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
    path = self.filename
    filetype = path[len(path) - 3:]
    dataframe = pd.DataFrame()

    if filetype == "dat":
       self.record = wfdb.rdrecord(path[:-4], channels=[0])
       temp_arr_y = self.record.p_signal
       temp_arr_y = np.concatenate(temp_arr_y)
       temp_arr_y = temp_arr_y[:3000]
       self.fsampling = self.record.fs
       maxFreq=self.fsampling/2
       ComposedSignal = temp_arr_y
       if not len(snr_signal) == 0:
           changeSNR(self, viewportup, viewportmiddle, viewportdown, sampleController, SNRcontrol, sampleRatioNumber,
                     SNRnumber, fmaxradio, hertzradio)
       else:
            Utility.draw3Graphs(self,viewportup, viewportmiddle,viewportdown,sampleController,sampleRatioNumber,ComposedSignal,maxFreq,snr_signal,fmaxradio,hertzradio)
       return  # Exit the function after reading and processing .dat file

    if self.filename:
        try:
            dataframe = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            # Handle the case when the CSV file is empty
            return
        except pd.errors.ParserError:
            # Handle the case when the CSV file has no header
            dataframe = pd.read_csv(path, header=None)

    ComposedSignal = dataframe.iloc[0:3000, 1]  # Load all rows from the second column
    maxFreq = dataframe.iloc[0,2]
    if not len(snr_signal) == 0:
        changeSNR(self, viewportup, viewportmiddle, viewportdown, sampleController, SNRcontrol, sampleRatioNumber,
                  SNRnumber, fmaxradio, hertzradio)
    else:
        Utility.draw3Graphs(self, viewportup, viewportmiddle, viewportdown, sampleController, sampleRatioNumber, ComposedSignal, maxFreq,snr_signal,fmaxradio,hertzradio)



def clearall(self,viewport,saver):
    choice = QMessageBox.warning(self, "Warning! Clear Al Signals",
                                 "Are you sure You want delete all the composed signals? ",
                                 QMessageBox.Yes | QMessageBox.No)
    if (choice == QMessageBox.No):
        return
    
    global maxFreqOfComposer
    global arrayOfComposerSignals
    global arrayOfSignalsData
    global ComposedSignal
    global addedsignals
    global maxFreqOfComposer
    maxFreqOfComposer=0
    ComposedSignal=[]
    addedsignals=[]
    saver.clear()
    viewport.clear()
    arrayOfSignalsData=[]
    arrayOfComposerSignals=[]



def export_summed_signal(self):
    t = Utility.generateLinspace3000()
    global maxFreq
    global ComposedSignal
    global addedsignals
    global maxFreqOfComposer
    ComposedSignal=addedsignals
    maxFreq=maxFreqOfComposer

    '''Saves the summed signal as a CSV file'''
    if len(arrayOfComposerSignals) == 0:
        QMessageBox.warning(
            self, 'NO SIGNAL ', 'You have to plot a signal first')
    else:
        FolderPath = QFileDialog.getSaveFileName(
            None, str('Save the summed signal'), None, str("CSV Files(*.csv)"))
        if FolderPath[0]:  # Check if the user selected a file path
            # Create a header row for the columns
            header = "Time,Signal,MaxFrequency"  # Modify column names as needed

            # Repeat maxFreq value to match the length of t
            maxFreq_array = np.full(t.shape, maxFreq)

            # Combine t, ComposedSignal, and maxFreq_array into a single array
            data_to_save = np.column_stack((t, ComposedSignal, maxFreq_array))

            # Save data with a header row
            np.savetxt(str(FolderPath[0]), data_to_save, delimiter=',', header=header, comments='', fmt='%s')

            QMessageBox.information(
                self, 'Complete ', 'The CSV was exported successfully at: \n ' + str(FolderPath[0]))





def changeSNR(self,viewportup,viewportmiddle,viewportdown,samplecontrol,SNRcontrol,sampleratiolabel,SNRNumber,fmaxradio,hertzradio):
    global ComposedSignal
    global maxFreq
    global snr_signal
    snrValue=SNRcontrol.value()
    SNRNumber.setText(f"{str(snrValue)} db")
    if snrValue==50:
        snr_signal=[]
    else:
        snr_signal = ComposedSignal + np.random.normal(0, 10 ** (-snrValue / 20), len(ComposedSignal))

    if len(snr_signal)==0:
        Utility.draw3Graphs(self,viewportup,viewportmiddle,viewportdown,samplecontrol,sampleratiolabel,ComposedSignal,maxFreq,snr_signal,fmaxradio,hertzradio)
    else:
        Utility.draw3Graphs(self,viewportup,viewportmiddle,viewportdown,samplecontrol,sampleratiolabel,snr_signal,maxFreq,snr_signal,fmaxradio,hertzradio)

def applychanges(fmaxradio, hertzradio, sampleController, sampleRatioLabel):
    global maxFreq
    if fmaxradio.isChecked():
        value=sampleController.value()
        value=value/maxFreq
        sampleController.setMaximum(40)
        sampleController.setTickInterval(10)
        sampleController.setValue(int(value*10))
        sampleRatioLabel.setText(f"{str(value)} Fmax")
    elif hertzradio.isChecked():
        value = sampleController.value()
        value = int((value/10)*maxFreq)
        sampleController.setMaximum(int(4*maxFreq))
        sampleController.setTickInterval(1)
        sampleController.setValue(int(value))
        sampleRatioLabel.setText(f"{str(value)} Hz")
    else:
        return
