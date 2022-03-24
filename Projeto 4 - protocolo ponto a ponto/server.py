#####################################################
# Camada Física da Computação
#Carareto
####################################################

from tracemalloc import stop
from urllib import response
from xmlrpc import server

from pandas import array
from enlace import *
import time
import numpy as np
import time

#   python -m serial.tools.list_ports

class Server:
    def __init__(self, serialName):
        self.serialName = serialName
        
    def startServer(self):
        self.serverCom = enlace(self.serialName)
        self.serverCom.enable()

    def closeServer(self):
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.serverCom.disable()
        exit()

    def receiveData(self,n):
        return self.serverCom.getDataServer(n)

    def sendData(self, data):
        self.serverCom.sendData(data)

    def receiveHandShake(self,n):
        pacote, lenPacote = self.serverCom.getDataServer(n)
        pacote = list(pacote)
        pacote = list(map(int, pacote))
        pacote[0] = 2
        responseHandShake = b''
        for i in pacote:
            i = (i).to_bytes(1, byteorder="big")
            responseHandShake += i
        return responseHandShake, lenPacote


    # fraciona o head para identificar cada componente presente
    def fracionaHead(self, pacote):
        head = pacote[0:10]
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

    def checkMsgreliability(self, pacote, numPacote):
        h0, h1, h2, h3, h4, h5, h6, h7, h8, h9 = self.fracionaHead(pacote)
        # Checando se o número do pacote enviado está correto
        #h4 = int.from_bytes(h4, "big")
        if h4 != numPacote:
            print(f"O número do pacote está errado! Por favor reenvie o pacote {numPacote}")
            return numPacote

        # Checando se o EOP está no local correto
        eop = pacote[len(pacote)-4:len(pacote)+1]
        if eop != 0x00000000.to_bytes(4, byteorder="big"):
            print(f"O eop está no local errado! Por favor reenvie o pacote {numPacote}")
            return numPacote
        
        print("Está tudo certo com a mensagem! Vamos enviar uma mensagem de confirmação.")
        h0 = 4
        h7 = numPacote
        confirmacao = [h0, h1, h2, h3, h4, h5, h6, h7, h8, h9]
        responseCorrectMsg = b''
        for i in confirmacao:
            i = (i).to_bytes(1, byteorder="big")
            responseCorrectMsg += i
        print(responseCorrectMsg)
        self.serverCom.sendData(responseCorrectMsg + b'\x00' + 0x00000000.to_bytes(4, byteorder="big"))
        return h4, h3


        
        

serialName = "COM4"     

### MENSAGENS IMPORTANTES ###
responseHandShake = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
responseCorrectMsg = b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def main():
    try:
        
        # * INICIALIZANDO SERVER
        server = Server('COM4')
        server.startServer()

        # * HANDSHAKE
        print("Esperando HandShake\n")
        pacote, lenPacote = server.receiveHandShake(15)
        print("Handshake recebido com sucesso! Enviando reposta de estabilidade.")
        server.sendData(pacote)
        time.sleep(.5)

        # * RECEBIMENTO DOS PACOTES
        # Variável para armazenar as informações recolhidas
        data = b''
        numPacote = 1
        while True:
            print(f"Recebendo informações do pacote {numPacote}")
            # Recebendo o head
            head, lenHead = server.receiveData(10)
            print(head, head[5])
            #lenPayload = int.from_bytes(head[5], byteorder="big")
            lenPayload = head[5]
            payload_EOP, lenPayload_EOP = server.receiveData(lenPayload + 4)
            numPacoteConfirmacao, h3 = server.checkMsgreliability(head + payload_EOP, numPacote)
            if numPacote == numPacoteConfirmacao:
                numPacote += 1
                data += payload_EOP[0:len(payload_EOP) - 4]
                print(len(data))
            if numPacote == h3 + 1:
                data += payload_EOP[0:len(payload_EOP) - 4]
                break
            


        pathImageRx = "Imagens/rxImage.png"
        print(len(data))
        print(data[0:len(data)])
        f = open(pathImageRx, 'wb')
        f.write(data)
        f.close()

        # * FECHANDO CLIENT
        server.closeServer()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        server.closeServer()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

