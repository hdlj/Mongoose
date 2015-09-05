
/* ===============================================================================
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>



Date: 2015


based on this source code written by Mika Tuupola:
https://github.com/tuupola/avr_demo/tree/master/blog/simple_usart

and this post:
http://www.appelsiini.net/2011/simple-usart-with-avr-libc

===============================================================================*/

#include "serial.h"


void HOSUartPutchar(char c, FILE *stream);
char HOSUartGetChar(FILE *stream);
void HOSUartInit(void);


FILE uart_output = FDEV_SETUP_STREAM(HOSUartPutchar, NULL, _FDEV_SETUP_WRITE);
FILE uart_input = FDEV_SETUP_STREAM(NULL, HOSUartGetChar, _FDEV_SETUP_READ);

void HOSUartInit(void) {
    UBRR0H = UBRRH_VALUE;
    UBRR0L = UBRRL_VALUE;
    
#if USE_2X
    UCSR0A |= _BV(U2X0);
#else
    UCSR0A &= ~(_BV(U2X0));
#endif

    UCSR0C = _BV(UCSZ01) | _BV(UCSZ00); /* 8-bit data */ 
    UCSR0B = _BV(RXEN0) | _BV(TXEN0);   /* Enable RX and TX */    
}

void HOSUartPutchar(char c, FILE *stream) {
    if (c == '\n') {
        HOSUartPutchar('\r', stream);
    }
    loop_until_bit_is_set(UCSR0A, UDRE0);
    UDR0 = c;
}

char HOSUartGetChar(FILE *stream) {
    loop_until_bit_is_set(UCSR0A, RXC0);
    return UDR0;
}

void HOSSerialSetup(){
    HOSUartInit();
    stdout = &uart_output;
    stdin  = &uart_input;
}


void HOSSafePrintInt(uint16_t data){
    // atomic operation
    MOSAtomicEnter();
    char buf[6];
    itoa(data, buf, 10);
    printf("%s\n", buf);
    MOSAtomicExit();
}

void HOSSafePrint(string input){
    // atomic operation 
    MOSAtomicEnter();
    printf("%s\n",input);
    MOSAtomicExit();
}



