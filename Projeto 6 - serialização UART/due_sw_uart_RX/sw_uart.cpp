// ARQUIVO PARA CRIAÇÃO DE FUNÇÕES

// importando as variáveis
#include "sw_uart.h"
// importação para melhorar compilamento do computador
#pragma GCC optimize ("-O3")

// função "sw_uart_setup" que não retorna nada. A função efetua 
void sw_uart_setup(due_sw_uart *uart, int rx, int stopbits, int databits, int paritybit) {
	
	uart->pin_rx     = rx;
	uart->stopbits   = stopbits;
	uart->paritybit  = paritybit;
  uart->databits   = databits;
  pinMode(rx, INPUT); 
}


// função "calc_even_parity" que retorna um inteiro. Um byte é composto por 8 bits, a
int calc_even_parity(char data) {
  int ones = 0;
  // for para contar
  // Esse for está realizando uma operação lógica AND com cada bit da mensagem e o valor 1, ou seja, se o bit também for 1 o resultado da operação será 1, caso 
  // contrário será 0, com isso conseguimos contar a quantidade de 1´s na mensagem.
  for(int i = 0; i < 8; i++) {
    // Operação >> desloca N bits para direita. Exemplo: A = 00010001; A >> 2 --> A = 00000100
    // Operação & é igual ao AND
    // (0x01)16 = (1)2
    ones += (data >> i) & 0x01;
  }
  // Ao retornar o resto da divisão por 2 nós saberemos se existe um número par(resto=0) ou ímpar(resto=1) de 1´s.
  return ones % 2;
}

// função "sw_uart_receive_byte" que retorna um inteiro. A função efetua o recebimento dos bytes que serão enviados
int sw_uart_receive_byte(due_sw_uart *uart, char* data) {
  // wait start bit
  // Visto que antes da msg ser enviada o sinal permanece alto(=1), logo esse while permanece rodando até que o sinal vire baixo(=0) sinalizando que a msg vai começar
  while(digitalRead(uart->pin_rx) == HIGH)
  {
    //Serial.println("esperando byte");
  }
  // Saindo do while no sabemos que a msg vai chegar, entretanto é preciso esperar meio periodo para confirmar se o "start bit" é realmente 0 ou se houve um erro
  // Após esperar esse meio periodo de bit e confirmado que o sinal é 0, é preciso esperar mais um período completo de bit para medirmos exatamente no meio do próximo
  // bit(que já será o primeiro bit da mensagem) e evitar a medição de tensões erradas na subida ou descida do sinal.
  Serial.println("\nchegou byte");
  // confirm start bit
  _sw_uart_wait_half_T(uart);
  // HIGH = invalid
  if(digitalRead(uart->pin_rx) == HIGH) {
    return SW_UART_ERROR_FRAMING;
  }

  _sw_uart_wait_T(uart);
  
  // start getting data 
  // Confirmado o "start bit" e esperado um período e meio(T + T/2), nós podemos começar a receber a mensagem.
  
  char aux = 0x00;
  // Esse for está realizando uma operação lógica OR com cada bit da mensagem e o valor 0, ou seja, se o bit for 1 o resultado da operação será 1, caso 
  // contrário será 0.
  
  for(int i = 0; i < uart->databits; i++) {
    // A função digitalRead(pino) recebe o pino do arduino como argumento e retorna HIGH ou LOW
    // A operação |= equivale ao OR atribuindo o valor do resultado a variável. Exemplo: x = 1100; x|=1010 --> x = x OR 1010; x = 1000
    // Operação << desloca N bits para esquerda. Exemplo: A = 00010001; A << 2 --> A = 01000100
    aux |= digitalRead(uart->pin_rx) << i;
    _sw_uart_wait_T(uart);
  }
  
  // parity
  int rx_parity = 0;
  if(uart->paritybit != SW_UART_NO_PARITY) {
    rx_parity = digitalRead(uart->pin_rx);
    _sw_uart_wait_T(uart);
  }

  // get stop bit
  for(int i = 0; i < uart->stopbits; i++) {
    if(digitalRead(uart->pin_rx) == LOW) {
      return SW_UART_ERROR_FRAMING;
    }
    _sw_uart_wait_T(uart);
  }
  
  int parity = 0;
  if(uart->paritybit == SW_UART_EVEN_PARITY) {
     parity = calc_even_parity(aux);
  } else if(uart->paritybit == SW_UART_ODD_PARITY) {
     parity = !calc_even_parity(aux);
  }

  if(parity != rx_parity) {
    return SW_UART_ERROR_PARITY;
  }
  
  *data = aux;
  return SW_UART_SUCCESS;
}


// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart) {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart) {
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}
