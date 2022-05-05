// ARQUIVO PARA REALIZAR O PROCESSO COM AS VARIÁVEIS E FUNÇÕES

#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 2);
}

void loop() {
 send_byte();
 delay(3000);
}

void send_byte() {
  char msg[6] = {'a', 'd', 'n', 'e', 'y',' '};
  for (int i =0; i< sizeof(msg) / sizeof(msg[0]); i++){
    char letter = msg[i];
    sw_uart_send_byte(&uart, letter);
    delay(2000);
  }
  Serial.println("MENSAGEM ENVIADA");
}
