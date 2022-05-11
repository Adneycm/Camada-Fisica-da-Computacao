#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from index import Signal
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils


def main():
 
    print("----- Inicializando decoder -----\n")
    decoder = Signal()
    
    sd.default.samplerate = decoder.fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = decoder.time - 2  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    #contagem para inicio da gravção
    cont = 5
    while cont > 0:
        print(f"Captura do aúdio irá iniciar em {cont} segundos")
        cont -= 1
        time.sleep(1)

    print("\nGravação iniciada\n")
      
    #gravação do áudio
    audio = sd.rec(int(duration*decoder.fs), decoder.fs, channels=1)
    sd.wait()
    print("Gravação concluída\n")
    plt.figure(figsize=(25,10))
    x = np.linspace(0.0, duration, duration*decoder.fs)
    plt.plot(x, audio)
    plt.title('Áudio Gravado')
    plt.xlabel('Tempo')
    plt.ylabel('Amplitude')
    #plt.xlim(0,1500)
    plt.show()
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)

    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = decoder.plotFFT(audio)
    
    cb = np.array([d[0] for d in np.abs(yf)])
  
    peaks = peakutils.indexes(cb,thres=0.8, min_dist=300)
    peaks_x = peakutils.interpolate(xf, cb, ind=peaks)
    print(f"picos em x:{peaks_x}, quantidade:{len(peaks_x)}")

    ton1, ton2 = decoder.closerFrequency(peaks_x)
    print(ton1, ton2)
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    #plt.show()

if __name__ == "__main__":
    main()
