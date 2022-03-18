#####################################################
# Camada Física da Computação
#Carareto
####################################################

from tracemalloc import stop
from enlace import *
import time
import numpy as np
import sys
import math

#   python -m serial.tools.list_ports

com1 = enlace('COM3')

class Client:

    def __init__(self, file):
        self.head = None
        self.file = file
        self.eop = 0xAA + 0xBB + 0xCC + 0xDD
        self.payloads = None
        self.h0 = None # tipo de mensagem
        self.h1 = b'0' # livre
        self.h2 = b'0' # livre
        self.h3 = None # número total de pacotes do arquivo
        self.h4 = None # número do pacote sendo enviado
        self.h5 = None # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
        self.h6 = b'0' # pacote solicitado para recomeço quando a erro no envio.
        self.h7 = None # último pacote recebido com sucesso.
        self.h8 = b'0' # CRC
        self.h9 = b'0' # CRC

    # Quebra a imagem nos payloads
    def createPayloads(self):
        self.payloads = [self.file[i:i + 114] for i in range(0, len(self.file), 114)]
        return self.payloads

    # Define o tipo da mensagem
    def defTypeMsg(self, n):
        self.h0 = (n).to_bytes(1, byteorder="big")
        # Mensagem do tipo Handshake
        if n == 1:
            self.h5 = b'0' # ? o que é o id do arquivo
            self.handshake()
        # Mensagem do tipo dados
        elif n == 3:
            self.h5 = len(self.payload)
            self.h5 = (self.h5).to_bytes(1, byteorder="big")

    def defNumMsg(self,n):
        self.h4 = (n).to_bytes(1, byteorder="big")

    # Define a quantidade de pacotes que serão enviados
    def qtdPacotes(self, file):
        lenImage = len(file)
        h3 = math.ceil(lenImage/114)
        self.h3 = (h3).to_bytes(2, byteorder="big")

    # Cria a composição do head
    def createHead(self):
        self.head = self.h1+self.h2+self.h3+self.h4+self.h5+self.h6+self.h7+self.h8+self.h9

    # Cria pacote
    def createPacote(self):
        return self.head + self.payloads[self.h4] + self.eop

    # Realiza o handshake
    def handshake(self):
        self.createHead()
        payload = (114).to_bytes(114, byteorder="big")
        pacote = self.createHead() + payload + self.eop
        cont = 0
        while True: 
            com1.senData(pacote)
            time.sleep(.5)
            confirmacao, lenConfimacao = com1.getData(128)
            cont += 1
            if type(confirmacao) == str:
                continue
            elif cont == 4:
                return "Servidor não respondeu após quarta tentativa. Cancelando comunicação."
            else:
                return confirmacao
                break
            



            


serialName = "COM3"     
file = "Projeto 4 - protocolo ponto a ponto/Imagens/txImage.png"              

def main():
    try:
      
        com1 = enlace('COM3')
        
        com1.enable()

        cliente = Client(file)
        payloads = cliente.createPayloads()
        cliente.handshake()
        #for payload in payloads:




        

        
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