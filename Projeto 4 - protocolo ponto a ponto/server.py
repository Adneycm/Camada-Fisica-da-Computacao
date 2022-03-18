#####################################################
# Camada Física da Computação
#Carareto
####################################################

from re import X
from tracemalloc import stop
from enlace import *
import time
import numpy as np
import time

#   python -m serial.tools.list_ports

class Server:
    def __init__(self, pacote, lenPacote):
        self.pacote = pacote
        self.lenPacote = lenPacote

    def fracionaHead(self):
        head = self.pacote[0:10]
        h0 = head[0] # tipo de mensagem
        h1 = head[1] # livre
        h2 = head[2] # livre
        h3 = head[3] # número total de pacotes do arquivo
        h4 = head[4] # número do pacote sendo enviado
        h5 = head[5] # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
        h6 = head[6] # pacote solicitado para recomeço quando a erro no envio.
        h7 = head[7] # último pacote recebido com sucesso.
        h8 = head[8] # CRC
        h9 = head[9] # CRC
        return h0, h1, h2, h3, h4, h5, h6, h7, h8, h9
        

serialName = "COM4"         

def main():
    try:
        
        com1 = enlace('COM4')
        
    
        com1.enable()

        
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

