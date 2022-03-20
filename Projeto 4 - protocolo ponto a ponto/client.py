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

    def __init__(self, file, serialName):
        #self.clientCom = None
        self.serialName = serialName
        self.head = 0
        self.file = file
        self.eop = 0x00000000.to_bytes(4, byteorder="big")
        self.payloads = 0
        self.h0 = 0 # tipo de mensagem
        self.h1 = b'\x00' # livre
        self.h2 = b'\x00' # livre
        self.h3 = 0 # número total de pacotes do arquivo
        self.h4 = 0 # número do pacote sendo enviado
        self.h5 = 0 # se tipo for handshake:id do arquivo; se tipo for dados: tamanho do payload
        self.h6 = b'\x00' # pacote solicitado para recomeço quando a erro no envio.
        self.h7 = 0 # último pacote recebido com sucesso.
        self.h8 = b'\x00' # CRC
        self.h9 = b'\x00' # CRC


    def startClient(self):
        self.clientCom = enlace(self.serialName)
        self.clientCom.enable()


    def closeClient(self):
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.clientCom.disable()
        exit()


    # Quebra a imagem nos payloads
    def createPayloads(self):
        self.payloads = [self.file[i:i + 114] for i in range(0, len(self.file), 114)]
        return self.payloads

    # Define o tipo da mensagem
    def defTypeMsg(self, n):
        self.h0 = (n).to_bytes(1, byteorder="big")
        # Mensagem do tipo Handshake
        if n == 1:
            self.h5 = b'\x00' # ? o que é o id do arquivo
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
        self.head = self.h0+self.h1+self.h2+self.h3+self.h4+self.h5+self.h6+self.h7+self.h8+self.h9

    # Cria pacote
    def createPacote(self):
        return self.head + self.payloads[self.h4] + self.eop

    # Realiza o handshake
    def handshake(self):
        payload = b'\x00'
        self.defTypeMsg(1)
        self.h3 = b'\x00'
        self.h4 = b'\x00'
        self.h7 = b'\x00'
        self.createHead()
        pacote = self.head + payload + self.eop
        print(pacote)
        print(len(pacote))
        timeMax = time.time()
        while True: 
            self.clientCom.sendData(pacote)
            time.sleep(1)
            confirmacao, lenConfimacao = self.clientCom.getData(15)
            print(type(confirmacao))
            timeF = time.time()
            if timeF - timeMax >= 25:
                print("Servidor não respondeu após quarta tentativa. Cancelando comunicação.")
                break

            elif type(confirmacao) == str:
                print('oi')
                print(confirmacao)

            else:
                print('oioi')
                return confirmacao
                
            

serialName = "COM3"     
file = "Projeto 4 - protocolo ponto a ponto/Imagens/txImage.png"              

def main():
    try:
        
        
        # com1 = enlace('COM3')
        # com1.enable()

        cliente = Client(file, 'COM3')
        cliente.startClient()


        # * HANDSHAKE
        print("Iniciando HandShake\n")
        if cliente.handshake() is None:
            cliente.closeClient()
        
        print("Handshake realizado com sucesso! Servidor está pronto para o recebimento da mensagem.")






        cliente.closeClient()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()