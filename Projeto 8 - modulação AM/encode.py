
#importe as bibliotecas
from index import Signal
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time

def main():

    print("----- Inicializando encoder -----\n")
    encoder = Signal()

    sd.default.samplerate = encoder.fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = encoder.time  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    #contagem para inicio da gravção
    cont = 5
    while cont > 0:
        print(f"Captura do aúdio irá iniciar em {cont} segundos")
        cont -= 1
        time.sleep(1)
    print("\nGravação Iniciada\n")

    #gravação do áudio
    audio = sd.rec(int(duration*encoder.fs), encoder.fs, channels=1)
    sd.wait()
    print("Gravação concluída\n")

    #filtro do áudio
    print("Iniciando tratamento do áudio\n")

    encoder.plotFFT(audio[:,0])

    audioFiltrado = encoder.LPF(audio[:,0], 2500)
    encoder.plotFFT(audioFiltrado)

    #áudio filtrado
    sd.play(audioFiltrado, encoder.fs)
    sd.wait()

    #modulando áudio com transmissora de 13.000Hz
    audioModulado = encoder.signalPortadora*audioFiltrado

    #normalizando áudio (dividir pela amplitude)
    audioNormalizado = encoder.normalizeSignal(audioModulado)
    encoder.plotFFT(audioNormalizado)

if __name__ == "__main__":
    main()