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

# Definindo os comandos a serem enviados
cmd1 = 0x00FF00FF.to_bytes(4,byteorder="big")  #(comando de 4 bytes)
cmd2 = 0x00FFFF00.to_bytes(4,byteorder="big")  #(comando de 4 bytes)
cmd3 = 0xFF00.to_bytes(2,byteorder="big")      #(comando de 2 bytes)
cmd4 = 0x00FF.to_bytes(2,byteorder="big")      #(comando de 2 bytes) 
cmd5 = 0xFF.to_bytes(1,byteorder="big")        #(comando de 1 byte)
cmd6 = 0x00.to_bytes(1,byteorder="big")        #(comando de 1 byte)

comandos = [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6]
cmdTr = []

nCmd = random.randint(10, 30)

while len(cmdTr) < nCmd:
    cmdTr.append(random.choice(comandos))

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

        time.sleep(.2)
        print("enviando byte de sacrifício")
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO\n")

        print("TRANSMISSÃO VAI COMEÇAR\n")

        # Enviando a quantidade de comandos que será enviado
        print(f"Serão enviados {nCmd} pacotes de comandos\n")
        nPacotes = nCmd.to_bytes(2, byteorder="big")
        com1.sendData(nPacotes)
        time.sleep(0.05)

        for i in cmdTr:
            # Tamanho do pacote a ser enviado
            txBufferLen = len(i)

            # Pacote a ser enviado 
            txBuffer = i        

            # Transformando o tamanho do pacote a ser enviado em bytes
            txBufferHeader = txBufferLen.to_bytes(2, byteorder="big") 

            # Enviando o tamanho do pacote em bytes
            com1.sendData(txBufferHeader)

            time.sleep(.05)

            # Enviando o pacote
            com1.sendData(txBuffer)

            time.sleep(.05)
            
        print("Pacotes enviados!\n")  

        print("Esperando confirmação da quantidade de pacotes recebidos pelo server...\n")
        try:
            nCmdConfirmacao, t = com1.getData(2)
            nCmdConfirmacaoInt = int.from_bytes(nCmdConfirmacao, "big") 

            if nCmdConfirmacaoInt == nCmd:
                print("Quantidade de pacotes recebidos é IGUAL a enviada :)")
            else:
                print("Quantidade de pacotes recebidos é DIVERGENTE da enviada :(")  
        except:
            print("Time Out: mensagem de confirmação não recebida!")     

        
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