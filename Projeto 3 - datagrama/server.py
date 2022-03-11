#####################################################
# Camada Física da Computação
#Carareto
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


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
        rxBuffer, nRx = com1.getData(2)
        time.sleep(.1)
        print("Enviando retorno...\n")
        com1.sendData(rxBuffer)
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
            print(f"Recebendo informações do {contPacotes+1} do pacote")

            # * Recebendo HEAD
            HeadBytes, HeadBytes_len = com1.getData(10)
            nPacote = int.from_bytes(HeadBytes[0:5], "big") # Número do pacote
            lenPacote = int.from_bytes(HeadBytes[5:10], "big") # Tamanho do pacote
            print(f"número do pacote: {nPacote}\ntamanho do pacote {lenPacote}\n")

            if nPacote == contPacotes+1:
                # * Recebendo PayLoad
                pacote, lenPacote = com1.getData(lenPacote) # Pacote
                ImageRx += pacote
                contPacotes +=1
                # Enviando confirmação de que está tudo certo com o pacote
                
            else:
                print(f"A ordem do pacote está errada! Por favor envie o pacote {contPacotes+1}")
                # Enviando mensagem pedindo o reenvio do pacote correto


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

