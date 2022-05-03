// ARQUIVO PARA REALIZAR O PROCESSO COM AS VARIÁVEIS E FUNÇÕES

#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 4);
}

void loop() {
 send_byte();
 delay(5);
}

void send_byte() {
  sw_uart_send_byte(&uart,'a');
  Serial.println("MENSAGEM ENVIADA");
}
