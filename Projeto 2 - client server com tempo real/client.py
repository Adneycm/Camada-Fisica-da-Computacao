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
print(f"Serão enviados {nCmd} comandos")

while len(cmdTr) < nCmd:
    cmdTr.append(random.choice(comandos))

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411"  # Mac    (variacao de)
serialName = "COM5"                    # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM5')
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        time.sleep(.2)
        print("enviando byte de sacrifício")
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("COMUNICAÇÃO ABERTA COM SUCESSO")

        print("TRANSMISSÃO VAI COMEÇAR")

        # Enviando a quantidade de comandos que será enviado
        print("Enviando quantidade de comandos que serão transmitidos")
        #com1.sendData(nCmd) # Qtd de comandos

        contCmd = 0
        for i in cmdTr:
            # Enviando o len do comando seguinte
            com1.sendData(np.asarray(len(i)))
            print(np.asarray(len(i)))

            time.sleep(0.05)
            
            # Enviando o comando
            com1.sendData(i)
            print(i)

            contCmd += 1
            print(f"{contCmd} comandos enviados")
  
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

