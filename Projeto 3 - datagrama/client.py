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
import random
import time
import sys
import math

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta


#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411"  # Mac    (variacao de)
serialName = "COM3"                    # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM3')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")
       
        print("TRANSMISSÃO VAI COMEÇAR\n")

        # * HANDSHAKE
        while True:
            print("Enviando Handshake\n")
            com1.sendData(b'00')
            time.sleep(.05)
            print("Aguardando retorno...\n")
            rxBuffer, nRx = com1.getData(2)
            if rxBuffer == 'S':
                print("Ok, vamos tentar novamente!\n")
                continue
            if rxBuffer == 'N':
                print("Interrompendo comunicação\n")
                break
            else:
                com1.rx.clearBuffer()
                time.sleep(.1)
                print("Handshake recebido!\n")
                break
         
        # * FRAGMENTAÇÃO
        """Nós iremos fragmentar o arquivo em pacotes a ser enviado para 
           melhorar alguns pontos na comunicação:
           1. Não deixar o canal de comunicação ocupado por muito tempo
           2. Evitar problemas relacionados ao Hardware (tamanho do buffer)
           3. Evitar ter que reenviar toda a mensagem caso uma parte seja perdida"""
        
        # * ACKNOWLEDGE / NOT ACKNOWLEDGE
        """Durante a transmissão de mensagens é muito comum a troca de confirmações
           de recebimento de um pacote ou até mesmo sinalizando que um pacote está
           faltando, entretanto, essa robustez na comunicação pode deixá-lá mais
           lenta. Tem-se, portanto um cuidado entre segurança e velocidade da infor-
           mação que precisa ser tomado."""

        # * Organização da transmissão
        """Nós iremos transmitir uma imagem portanto, fracionar essa imagem em pacotes de envio
           que serão compostos pelo HEAD, PayLoad e EOP (End Of Package) é necessário para
           garantir a confiabilidade da mensagem e evitar problemas como descrito no tópico de 
           fragmentação. A organização do tamanho do pacote será feita da seguinte maneira:
           --> HEAD: 10 bytes
           --> PayLoad: 114 bytes
           --> EOP: 4 bytes
           Totalizando assim 128 bytes. Devemos portanto dividir o tamanho da nossa imagem nesses
           pacotese enviá-los sequencialmente."""

        
        # Pegando o caminho da imagem a ser transmitida
        pathImageTx = "Projeto 3 - datagrama/Imagens/txImage.png"
        # Agora vamos abrir o arquivo da imagem e lê-lo com um arquivo binário
        ImageTx = open(pathImageTx, 'rb').read()
        print(ImageTx)
        # Vamos agora saber o tamanho da imagem em número inteiro e em bytes
        lenImage = len(ImageTx)
        lenImageTxBytes = lenImage.to_bytes(2, byteorder="big") 
        # Agora que temos o tamanho da imagem nós podemos saber quantos pacotes serão enviados
        nPacotes = math.ceil(lenImage/114)
        nPacotesBytes = nPacotes.to_bytes(2, byteorder="big")

        # Mandando a quantidade de pacotes que serão enviados para o server
        print(f"Enviando quantidade de pacotes que serão enviados {nPacotes}\n")
        com1.sendData(nPacotesBytes)

        # Criando lista de payloads para serem enviados
        payloads = [ImageTx[i:i + 114] for i in range(0, len(ImageTx), 114)]
        lenPayloads = []
        for i in payloads:
            lenPayloads.append(len(i))
        print(lenPayloads)
            

        # ! Vamos criar um LOOP para enviarmos sequencialmente o Head, PayLoad e EOP de cada pacote
        contPacotes = 0
        while contPacotes < nPacotes:
            print(f"Enviando informações do {contPacotes+1} do pacote")

            # * Enviando HEAD
            numPacote = (contPacotes+1).to_bytes(5, byteorder="big") # Número do pacote
            tamPacote = (len(payloads[contPacotes])).to_bytes(5, byteorder="big") # Tamanho do pacote
            com1.sendData(numPacote + tamPacote)
            print((contPacotes+1), len(payloads[contPacotes]))
            time.sleep(1)

            # * Enviando PayLoad
            com1.sendData(payloads[contPacotes]) # Pacote
            time.sleep(1)


            contPacotes += 1

        
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