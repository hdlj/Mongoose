#include "led.h"
void MOSLedOn(){
    PORTB |= _BV(PORTB5);
}

void MOSLedOff(){
    PORTB &= ~_BV(PORTB5);
}

void MOSLedSetup(){
    DDRB |= _BV(DDB5);
    MOSLedOff();
}