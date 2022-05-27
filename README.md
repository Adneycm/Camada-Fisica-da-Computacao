# Camada Física da Computação

### Autores:
* [Adney Costa Moura](https://github.com/Adneycm)
* [Lister Ogusuku Ribeiro](https://github.com/listerogusuku)

#### Objetivo de aprendizado da matéria:
* *Eletrônica*: introdução à física dos semicondutores; construção e modelos matemáticos de diodos, transistores de junção e de efeito de campo; análise de circuitos eletrônicos simples; 
* *Eletrotécnica*: introdução aos sistemas de geração, transmissão e distribuição de energia; fluxo de potência; demanda energética em bairros residenciais, indústrias e data-centers. 
* *Telecomunicações*: noções de sinal, ruído, canal de transmissão, modulação analógica e digital.

#### Descrição de cada projeto:
* Projeto 1 - loop back

  Neste projeto o objetivo foi construir um código em Python para transmissão e recepção serial simultâneas. Para realizar o projeto foi necessário conectar um       jumper entre os pinos RX e TX para que o microcontrolador fosse um "espelho" para os bytes enviados. Foi necessário também conectar o arduino ao computador por     meio de um cabo USB. A transmissão funcioanava portanto da seguinte maneira: primeiro o computador enviava uma série de bytes, via cabo USB, para o pino RX do       arduino que por sua vez transmitia para o pino TX, via jumper conectado; ao chegar no pino TX os bytes eram enviados novamente para o computador. Para realizar o   teste foi enviado uma imagem de 100x100 pixels. Segue abaixo foto da montagem correta do circuito:

* Projeto 2 - client server com tempo real
* Projeto 3 - datagrama
* Projeto 4 - protocolo ponto a ponto
* Projeto 5 - crc
* Projeto 6 - serialização UART
* Projeto 7 - dtmf
* Projeto 8 - modulação AM



#### Bibliografia básica do curso:
* *ALEXANDER, C.; SADIKU, M., Fundamentos de Circuitos Elétricos, 5ª ed., McGraw-Hill, 2013, ISBN 9788580551  Livro Impresso*
* *MEDEIROS, J., Princípios de Telecomunicações. Teoria e Prática, 5ª ed., Érica, 2015, ISBN 65874125  Livro Impresso*
* *SCHERZ, P.; MONK, S., Practical Electronics For Inventors, 3ª ed., Mc Graw Hill, 2013, ISBN 74158745  Livro Impresso*

#### Bibliografia complementar:
* *MALVINO, A.; BATES, D, Eletrônica - Vol. 2, 7ª ed., McGraw-Hill, 2008*
* *AQUINO, I. S., Como escrever artigos científicos - Sem arrodeiro e sem medo da ABNT, 8ª ed., SARAIVA, 2012*
* *MALVINO, A.; BATES, D, Eletrônica - Vol.1., 7ª ed., McGraw-Hill, 2008*
* *LATHI, B. P., Sistemas de Comunicações Analógicos e Digitais Modernos, 4ª ed., LTC, 2012*
* *HAMBLEY, A. R., Engenharia Elétrica: Princípios e Aplicações, 6ª ed., LTC, 2017*
