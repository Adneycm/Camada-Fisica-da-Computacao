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

        # ! Organização da transmissão
        """Nós iremos transmitir uma imagem 32x32 medido em pixels, o que é equivalente
           a 2048 bytes. Nós iremos portanto, fracionar essa imagem em pacotes de envio
           que serão compostos pelo HEAD, PayLoad e EOP (End Of Package). A organização
           do tamanho do pacote será feita da seguinte maneira:
           --> HEAD: 10 bytes
           --> PayLoad: 114 bytes
           --> EOP: 4 bytes
           Totalizando assim 128 bytes. Dividindo 2048 bytes por 128 bytes, nós teremos
           16 pacotes para serem enviados para o server."""

        print("Vamos iniciar o envio da imagem pacote por pacote!\n")
        # Pegando o caminho da imagem a ser transmitida
        imageTx = "image.png"
    


           
        

        

        

        
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