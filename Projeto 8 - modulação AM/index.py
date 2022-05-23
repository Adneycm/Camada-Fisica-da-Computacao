import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.fftpack import fft, fftshift
from scipy import signal as window
import sys
from scipy import signal as sg

class Signal:
    def __init__(self):
      self.fs = 44100
      self.time = 5
      self.n = self.time*self.fs #numero de pontos
      self.freqPortadora = 13000
      self.x = np.linspace(0.0, self.time, self.n)  # eixo do tempo
      self.signalPortadora = np.sin(self.freqPortadora*self.x*2*np.pi)
      

    #função para interromper programa
    def signal_handler(signal, frame):
            print('You pressed Ctrl+C!')
            sys.exit(0)

    #Converte intensidade em Db
    def todB(s):
        sdB = 10*np.log10(s)
        return(sdB)

    #função para calcular transformada de fourier
    def calcFFT(self, audio):
        # # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(audio)
        W = window.hamming(N)
        T  = 1/self.fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(audio*W)
        return(xf, np.abs(yf[0:N//2]))


    def plotFFT(self, audio):
        x,y = self.calcFFT(audio)
        plt.figure(figsize=(25,10))
        plt.plot(x, y)
        plt.axvline(x=2500, ymin=0, ymax=4, color='r')
        plt.axvline(x=10500, ymin=0, ymax=4, color='r')
        plt.axvline(x=15500, ymin=0, ymax=4, color='r')
        plt.title(f'Fourier Transform')
        plt.xlabel('Frequencies')
        plt.ylabel('Amplitude')
        #plt.xlim(0,1500)
        #plt.axis([0, 1500, 0, 0.0001])
        plt.show()

    def filtro(y, samplerate, cutoff_hz):
      # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
      nyq_rate = samplerate/2
      width = 5.0/nyq_rate
      ripple_db = 60.0 #dB
      N , beta = sg.kaiserord(ripple_db, width)
      taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
      yFiltrado = sg.lfilter(taps, 1.0, y)
      return yFiltrado

    def LPF(self, signal, cutoff_hz):
        #####################
        # Filtro
        #####################
        # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
        nyq_rate = self.fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        return(sg.lfilter(taps, 1.0, signal))

    def normalizeSignal(self, audio):
      amplitude = 0
      for i in np.abs(audio):
        if i > amplitude:
          amplitude = i
      audioNormalizado = audio/amplitude
      return audioNormalizado
      

