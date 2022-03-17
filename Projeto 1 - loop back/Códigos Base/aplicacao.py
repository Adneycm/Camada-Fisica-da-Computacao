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
serialName = "COM5"                    # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace('COM5')
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação aberta com sucesso")
        
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Essa sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
    
        imageR = "Projeto 1 - loop back/Códigos Base/imgs/insper.png"
        imageW = "Projeto 1 - loop back/Códigos Base/imgs/insperCopia.png"
        
        txBuffer = open(imageR, 'rb').read()


        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        #print(f"Tamanho da imagem a ser transmitida em bytes: {txBuffer.getsize()}")

            
        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        print("TRANSMISSÃO VAI COMEÇAR")
        
        print("----- Tempo de transmissão iniciado -----")
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
          
          
  
        #txBuffer = #dados
        tempoTi = time.time()
        com1.sendData(np.asarray(txBuffer))
        tempoTf= time.time()
        print(f"O tempo de transmissão foi de {tempoTf - tempoTi}")
        print("")
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        txSize = com1.tx.getStatus()
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
       
        print("RECEPÇÃO VAI COMEÇAR")
        
        print("----- Tempo de recepção iniciado -----")
        #print("Transformando a imagem em bits para a recepção")
        #print(" - {}".format(imgRecebida))
        #print("---------------------------")
        
        #Será que todos os bytes enviados estão realmente guardados? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        tempoRi= time.time()
        rxBuffer, nRx = com1.getData(txLen)
        tempoRf= time.time()
        print(f"O tempo de recepção foi de {tempoRf - tempoRi}")
        print("")
            
        f = open(imageW, 'wb')
        f.write(rxBuffer)
        f.close()
        # Encerra comunicação
        
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

