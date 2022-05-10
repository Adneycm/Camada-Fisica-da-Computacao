
#importe as bibliotecas
from signal import Signal
import numpy as np
import sounddevice as sd
#import matplotlib.pyplot as plt


def main():
    
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("----- Inicializando encoder -----\n")
    encoder = Signal()
    encoder.button = input("Digite um número de entre 0 e 9, ou A, B, C, D, X, #: ")
    print(f"O botão '{encoder.button}' possui as seguintes freqências na tabela DTMF: {encoder.DTMF[encoder.button]}\n")
    encoder.generateSin()
    print(f"Tocando tom referente a tecla '{encoder.button}'")
    sd.play(encoder.s[0], encoder.fs)
    sd.play(encoder.s[1], encoder.fs)
    #plt.show()
    sd.wait()


    # Exibe gráficos
    # plt.show()
    # # aguarda fim do audio
    # sd.wait()
    # plotFFT(self, signal, fs)
    

if __name__ == "__main__":
    main()
