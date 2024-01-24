import numpy as np
import csv
import pandas as pd
from scipy.signal import resample
# from PyQt5.QtCore import qWarning
# import warnings

plotref=0
ishidden=False

def findMaxFrequencyOfComposer(arrayOfSignalsData):
    fMaxComposer=-9999
    for i in arrayOfSignalsData:
        if(i.frequency>=fMaxComposer):
            fMaxComposer=i.frequency
        value = fMaxComposer
    return value

def setSliderLabelText(freq,amp,phase,freqVal,ampVal,phaseVal):
    freq.setText(str(freqVal))
    amp.setText(str(ampVal))
    phase.setText(str(phaseVal))



def generateSinSignal(t,magnitude,phase,frequency):
    return magnitude * np.sin(2 * np.pi * frequency * t + np.deg2rad(phase))


def generateLinspace3000():
    return np.linspace(0, 3, 3000, endpoint=False)

def generateLinspaceWithNumberOfSamples(n):
    return np.linspace(0, 1, n, endpoint=False)


def sinc_interpolation(input_magnitude, input_time, original_time):
    '''Whittaker Shannon interpolation formula linked here:
      https://en.wikipedia.org/wiki/Whittaker%E2%80%93Shannon_interpolation_formula '''

    # Check if the lengths of input_magnitude and input_time are not the same
    if len(input_magnitude) != len(input_time):
        print('not same')
        return  # If they are not the same, exit the function

    # Find the period T, assuming that input_time is equidistant (which is common)
    if len(input_time)==1:
        if input_time[0]==0:
            T=1
        else:
            T=input_time[0]
    elif len(input_time) != 0:
        T = input_time[1] - input_time[0]  # Calculate the period (time difference between two adjacent samples)

    # Create a matrix sincM that represents the differences between the original_time
    # and each sample time in input_time
    sincM = np.tile(original_time, (len(input_time), 1)) - \
        np.tile(input_time[:, np.newaxis], (1, len(original_time)))

    # Calculate the output_magnitude by performing dot product between input_magnitude
    # and the sinc function evaluated at sincM divided by the period T
    output_magnitude = np.dot(input_magnitude, np.sinc(sincM/T))

    return output_magnitude  # Return the interpolated signal



def sampleAndInterpolate(self, viewportup, viewportmiddle, viewportdown,samplecontrol, sampleRatioNumber, ComposedSignal, maxFreq,snr_signal,fmaxradio,hertzradio):
    # Get the desired sampling rate from the user
    global plotref
    if fmaxradio.isChecked():
        value = samplecontrol.value()/10
        fs = (value * maxFreq)
        sampleRatioNumber.setText(f"{str(value)} Fmax")
    elif hertzradio.isChecked():
        value = samplecontrol.value()
        fs = (value)
        sampleRatioNumber.setText(f"{str(value)} Hz")
    

    # Generate a new linspace for the total time of the signal based on maxFreq
    t = generateLinspace3000()

    # Calculate the number of samples based on the desired sampling rate

    # Generate time points for sampling
    if fs==0:
        viewportup.plot(t,ComposedSignal,pen='r')
        return
    time_interval=1/fs
    t_samples = np.arange(0, 3, time_interval)

    if len(snr_signal)==0:
        sampledPoints = np.interp(t_samples, t, ComposedSignal)

        # # Perform cubic spline interpolation
        reconstructedSignal =sinc_interpolation(sampledPoints, t_samples, t)

        # Calculate the difference between the original and reconstructed signals
        difference=ComposedSignal-reconstructedSignal

        clearallgraphs(self, viewportup, viewportmiddle, viewportdown)

        # Plot the sampled points, original signal, reconstructed signal, and difference
        viewportup.plot(t, ComposedSignal, pen='r', name='Original')
    else:
        sampledPoints = np.interp(t_samples, t, snr_signal)

        # # Perform cubic spline interpolation
        reconstructedSignal = sinc_interpolation(sampledPoints, t_samples, t)

        # Calculate the difference between the original and reconstructed signals
        difference = snr_signal - reconstructedSignal

        clearallgraphs(self, viewportup, viewportmiddle, viewportdown)
        # Plot the sampled points, original signal, reconstructed signal, and difference
        viewportup.plot(t, snr_signal, pen='r', name='Original')

    if ishidden==False:
        plotref=viewportup.plot(t_samples, sampledPoints, pen=None, symbol='x', symbolPen='r', symbolBrush='b', symbolSize=10)
    else:
        plotref = viewportup.plot(t_samples, sampledPoints, pen=None, symbol='x', symbolPen='r', symbolBrush='b',
                                  symbolSize=10)
        plotref.hide()
    viewportmiddle.plot(t, reconstructedSignal, pen='b', name='Reconstructed signal')
    viewportdown.plot(t, difference, pen='g', name='Difference')




def read_csv_file(path):
    datContent = [i.strip().split() for i in open(path).readlines()]
    with open(path, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(datContent)
    return pd.read_csv(path)

def draw3Graphs(self,viewportup, viewportmiddle,viewportdown,sampleController,sampleRatioNumber,ComposedSignal,maxFreq,snr_signal,fmaxradio,hertzradio):
    t=generateLinspace3000()
    clearallgraphs(self,viewportup,viewportmiddle,viewportdown)

    sampleAndInterpolate(self,viewportup, viewportmiddle,viewportdown,sampleController,sampleRatioNumber,ComposedSignal,maxFreq,snr_signal,fmaxradio,hertzradio)

def clearallgraphs(self,viewportup, viewportmiddle,viewportdown):
    viewportup.clear()
    viewportmiddle.clear()
    viewportdown.clear()



def handle_pyqt_warning(message):
    # You can customize how you handle warnings here
    print(f'PyQt5 Warning: {message})')

def hidesample():
    global ishidden
    if ishidden==False:
        ishidden=True
        plotref.hide()
    else:
        ishidden = False
        plotref.show()

