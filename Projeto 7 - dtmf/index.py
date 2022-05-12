
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.fftpack import fft, fftshift
from scipy import signal as window
import sys


class Signal:
    def __init__(self):
        self.signal = []
        self.button = ''
        self.fs = 44100
        self.time = 7
        self.n = self.time*self.fs # número de pontos
        self.t = np.linspace(0.0, self.time, self.n) # eixo do tempo
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

        self.uniqueTons = [1206, 1339, 1477, 1633, 697, 770, 852, 941]
        self.tecla = ''

     #* METÓDOS

    #função para gerar senos
    def generateSin(self):
        self.signal = (
                  np.sin(self.DTMF[self.button][0]*self.t*2*np.pi), 
                  np.sin(self.DTMF[self.button][1]*self.t*2*np.pi)
                  )

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
        plt.title(f'Fourier Transform (tecla = {self.tecla})')
        plt.xlabel('Frequencies')
        plt.ylabel('Amplitude')
        #plt.xlim(0,1500)
        #plt.axis([0, 1500, 0, 0.0001])
        plt.show()

    def closerFrequency(self,peaks):
        uniqueTons = [1206, 1339, 1477, 1633, 697, 770, 852, 941]
        menorDelta = 20
        segundoMenorDelta = 20
        tonCerto = 0
        segundoTonCerto = 0
        for peak in peaks:
            for ton in uniqueTons:
                delta = abs(peak - ton)
                if delta <= menorDelta:
                    menorDelta = delta
                    segundoTonCerto = tonCerto
                    tonCerto = ton

                elif delta <= segundoMenorDelta:
                    segundoMenorDelta = delta
                    segundoTonCerto = ton

        ton = [tonCerto, segundoTonCerto]
        print(ton)
        list_of_key = list(self.DTMF.keys())
        list_of_value = list(self.DTMF.values())

        for tecla in self.DTMF.values():
            if sorted(ton) == sorted(list(tecla)):
                position = list_of_value.index(tecla)
                self.tecla = list_of_key[position]
                return f"A tecla apertada foi a {list_of_key[position]}"

    #função para interromper programa
    def signal_handler(signal, frame):
            print('You pressed Ctrl+C!')
            sys.exit(0)

    #Converte intensidade em Db
    def todB(s):
        sdB = 10*np.log10(s)
        return(sdB)

