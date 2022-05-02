// ARQUIVO PARA REALIZAR O PROCESSO COM AS VARIÁVEIS E FUNÇÕES

#include "sw_uart.h"
#include "sw_uart.cpp"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 4, 1, 8, SW_UART_EVEN_PARITY);
}

void loop() {
 send_byte();
 delay(5);
}

void send_byte() {
  sw_uart_send_byte(&uart);
}
