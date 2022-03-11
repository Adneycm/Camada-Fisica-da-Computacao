#####################################################
# Camada Física da Computação
#Carareto
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from re import X
from tracemalloc import stop


from enlace import *
import time
import numpy as np

import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411"  # Mac    (variacao de)
serialName = "COM4"                    # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM4')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("RECEPÇÃO VAI COMEÇAR\n")

        # * HANDSHAKE
        print("Esperando Handshake...\n")
        handShake, lenHS = com1.getData(2)
        print("Enviando retorno...\n")
        com1.sendData(handShake)
        time.sleep(.05)
        print("Handshake enviado!\n")
        

        # Recebendo a quantidade de pacotes que serão enviados pelo client
        nPacotesBytes, nPacotesBytes_len = com1.getData(2)
        nPacotes = int.from_bytes(nPacotesBytes, "big")
        print(f"Serão enviados {nPacotes} pacotes\n")

        # ! Vamos criar um LOOP para recebermos sequencialmente o Head, PayLoad e EOP de cada pacote
        contPacotes = 0
        ImageRx = b'00'
        while contPacotes < nPacotes:
            print(f"Recebendo informações do pacote {contPacotes+1}")

            # * Recebendo Tamanho do pacote
            pacoteBytes, pacoteLenBytes = com1.getData(2)
            tamanhoPacote = int.from_bytes(pacoteBytes, "big")

            # * Recebendo pacote
            pacote, lenPacote = com1.getData(tamanhoPacote)
            # HEAD
            nPacote = int.from_bytes(pacote[0:5], "big")
            tamPayload = int.from_bytes(pacote[5:10], "big")
            # PayLoad
            payload = pacote[10:tamPayload + 10]
            # EOP
            EOP = pacote[tamPayload + 10:len(pacote)]


            if nPacote == contPacotes+1:
                # * Recebendo PayLoad
                ImageRx += payload
                # Enviando confirmação de que está tudo certo com o pacote
                com1.sendData(b'00')
                time.sleep(1)
                contPacotes +=1
            else:
                print(f"A ordem do pacote está errada! Por favor envie o pacote {contPacotes+1}\n")
                # Enviando mensagem pedindo o reenvio do pacote correto
                pacoteCerto = (contPacotes+1).to_bytes(2, byteorder="big")
                com1.sendData(pacoteCerto)
                time.sleep(1)


        pathImageRx = "Imagens/rxImage.png"
        print(ImageRx[2:len(ImageRx)])
        f = open(pathImageRx, 'wb')
        f.write(ImageRx[2:len(ImageRx)+1])
        f.close()

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

