
import numpy as np
import sounddevice as sd
#import matplotlib.pyplot as plt
from scipy.fftpack import fft
#from scipy import signal as window
import sys


class Signal:
    def __init__(self):
        self.signal = []
        self.button = ''
        self.fs = 44100
        self.time = 3
        self.x = []
        self.s = []
        self.DTMF = {'0': (1339, 941),
                     '1': (1206, 697),
                     '2': (1339, 697),
                     '3': (1477, 697),
                     '4': (770, 1206),
                     '5': (770, 1339),
                     '6': (770, 1477),
                     '7': (852, 1206),
                     '8': (852, 1339),
                     '9': (852, 1477),
                     'A': (1633, 697),
                     'B': (1633, 770),
                     'C': (1633, 852),
                     'D': (1633, 941),
                     'X': (1206, 941),
                     '#': (1477, 941)}

     #* METÓDOS

    #função para gerar senos
    def generateSin(self):
        n = self.time*self.fs #numero de pontos
        self.x = np.linspace(0.0, self.time, n)  # eixo do tempo
        self.s = (
                  np.sin(self.DTMF[self.button][0]*self.x*2*np.pi), 
                  np.sin(self.DTMF[self.button][1]*self.x*2*np.pi)
                  )

    #função para calcular transformada de fourier
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    # def plotFFT(self, signal, fs):
    #     x,y = self.calcFFT(signal, fs)
    #     plt.figure()
    #     plt.plot(x, np.abs(y))
    #     plt.title('Fourier')

    #função para interromper programa
    def signal_handler(signal, frame):
            print('You pressed Ctrl+C!')
            sys.exit(0)

    #Converte intensidade em Db
    def todB(s):
        sdB = 10*np.log10(s)
        return(sdB)

