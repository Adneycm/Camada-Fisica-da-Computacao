#importe as bibliotecas
from index import Signal
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time
import soundfile as sf

def main():

    print("----- Inicializando decoder -----\n")
    decoder = Signal()

    sd.default.samplerate = decoder.fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = decoder.time - 2 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    #contagem para inicio da gravção
    # cont = 5
    # while cont > 0:
    #     print(f"Captura do aúdio irá iniciar em {cont} segundos")
    #     cont -= 1
    #     time.sleep(1)
    # print("\nGravação Iniciada\n")

    # #gravação do áudio
    # audio = sd.rec(int(duration*decoder.fs), decoder.fs, channels=1)
    # sd.wait()
    # print("Gravação concluída\n")

    # decoder.plotFFT(audio[:,0])

    #lendo arquivo de áudio gerado pelo encode
    audio, samplerate = sf.read('signalTransmition.wav')

    #emitindo som áudio gerado pelo encode
    print("Emitindo som do áudio modulado")
    sd.play(audio, decoder.fs)
    sd.wait()

    #demodulando áudio com transmissora de 13.000Hz
    print("Demodulando áudio\n")
    audioDemodulado = decoder.signalPortadora*audio
    decoder.plotFFT(audioDemodulado, 'demodulado')

    #filtrando frequências superiores a 2.500Hz
    print("Filtrando frequências acima de 2.500Hz\n")
    audioFiltrado = decoder.LPF(audioDemodulado, 2500)
    decoder.plotFFT(audioFiltrado, 'demodulado e filtrado')

    print("Reproduzindo som do áudio demodulado e filtrado")
    sd.play(audioFiltrado, decoder.fs)
    sd.wait()





if __name__ == "__main__":
    main()