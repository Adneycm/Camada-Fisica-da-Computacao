
#importe as bibliotecas
from index import Signal
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

def main():

    print("----- Inicializando encoder -----\n")
    encoder = Signal()
    encoder.button = input("Digite um número de entre 0 e 9, ou A, B, C, D, X, #: ")
    print(f"O botão '{encoder.button}' possui as seguintes freqências na tabela DTMF: {encoder.DTMF[encoder.button]}\n")
    encoder.generateSin()
    print(f"Tocando tom referente a tecla '{encoder.button}'")
    audio = encoder.signal[0] + encoder.signal[1]
    sd.play(encoder.signal[0] + encoder.signal[1], encoder.fs)
    sd.wait()

    # Exibe gráficos
    plt.figure(figsize=(25,10))
    plt.plot(encoder.t, encoder.signal[0], label=f"Senoide de f={encoder.DTMF[encoder.button][0]}")
    plt.plot(encoder.t, encoder.signal[1], label=f"Senoide de f={encoder.DTMF[encoder.button][1]}")
    plt.plot(encoder.t, audio, label="Soma das senoides")
    plt.title(f"Tecla {encoder.button}")
    plt.xlabel("Tempo (s)", fontsize = 18)
    plt.ylabel("Amplitude", fontsize = 18)
    plt.legend(loc='upper right', fontsize=18)
    plt.axis([1, 1.01, -2, 2])
    plt.show()

if __name__ == "__main__":
    main()
