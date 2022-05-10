#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from signal import Signal
import numpy as np
import sounddevice as sd
#import matplotlib.pyplot as plt
import time
import peakutils


def main():
 
    print("----- Inicializando decoder -----\n")
    decoder = Signal()
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = decoder.fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = decoder.time - 2  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    cont = 5
    while cont > 0:
        print(f"Captura do aúdio irá iniciar em {cont} segundos")
        cont -= 1
        time.sleep(1)

    print("\nGravação iniciada")
      
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    audio = sd.rec(int(duration*decoder.fs), decoder.fs, channels=1)
    sd.wait()
    print("...     FIM")
    print(audio)
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0,7,decoder.time*decoder.fs)

    #grávico  áudio vs tempo!
    # plt.figure("F(y)")
    # plt.plot(t,audio)
    # plt.grid()
    # plt.title('Fourier audio')
    
    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    from scipy.fftpack import fft, fftshift
    def calcFFT(signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        #y  = np.append(signal, np.zeros(len(signal)*fs))
        N  = len(signal)
        T  = 1/fs
        xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
        yf = fft(signal)
        return(xf, fftshift(yf))

    xf, yf = calcFFT(audio, decoder.fs)
    #decoder.plotFFT()

    # plt.figure("F(y)")
    # plt.plot(xf,yf)
    # plt.grid()
    # plt.title('Fourier audio')
    
    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
  
    cb = np.array([d[0] for d in np.abs(yf)])
    print('\n\n')
    print(cb)
    peaks = peakutils.indexes(cb,thres=0.8, min_dist=300)

    peaks_x = peakutils.interpolate(xf, cb, ind=peaks)
    print(peaks_x)

    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    #plt.show()

if __name__ == "__main__":
    main()
