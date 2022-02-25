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
while len(cmdTr) < 23:
    cmdTr.append(random.choice(comandos))
#print(cmdTr)


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
        print("COMUNICAÇÃO ABERTA COM SUCESSO")

        print("TRANSMISSÃO VAI COMEÇAR")
        
        cmdInt = 'Insper'.encode(encoding='utf-8', errors='strict')
    
        for i in cmdTr:

            # qtdBytes = sys.getsizeof(i)
            # if qtdBytes == 4:
            #     com1.sendData(np.asarray(qtdBytes))
            # if qtdBytes == 2:
            #     com1.sendData(np.asarray(qtdBytes))
            # if qtdBytes == 1:
            #     com1.sendData(np.asarray(qtdBytes))
            # ----------------------------------------- #

            
            com1.sendData(np.asarray(cmdInt))
            com1.sendData(np.asarray(i))
  
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.  
        
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

