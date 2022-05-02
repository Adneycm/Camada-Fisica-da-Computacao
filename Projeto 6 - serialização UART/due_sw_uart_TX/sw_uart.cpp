// ARQUIVO PARA CRIAÇÃO DE FUNÇÕES

// importando as variáveis
#include "sw_uart.h"
// importação para melhorar compilamento do computador
#pragma GCC optimize ("-O3")

void sw_uart_setup(due_sw_uart *uart, int tx) {
  uart->pin_tx     = tx;
  pinMode(tx, INPUT); 
}


int calc_even_parity(char data) {
  int ones = 0;
  for(int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }
  return ones % 2;
}

void sw_uart_send_byte(due_sw_uart *uart) {
  
  // Primeiro vamos deixar o sinal em alto por 5 vezes o período de um bit
  for(int i = 0; i < 1093*10; i++) {
    digitalWrite(4, HIGH);
    asm("NOP");
  }
  
  // Agora vamos baixar o sinal para mandar o "start bit"
  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);
  
  // Agora o server está esperando a mensagem, então vamos enviá-la
  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, LOW);
  _sw_uart_wait_T(uart);

  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);
  

  // Enviada a mensagem é necessário agora enviar o bit de paridade
  // a = 01100001 --> em hexadecimal = 0x61
  char data = 0x61;
  int bitParidade = calc_even_parity(data);
  digitalWrite(uart->pin_tx, bitParidade);
  _sw_uart_wait_T(uart);

  // Feito isso já teremos enviado todo o necessário, faltando apenas o stopbit
  digitalWrite(uart->pin_tx, HIGH);
  _sw_uart_wait_T(uart);
  
  // Mensagem enviada!!
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
