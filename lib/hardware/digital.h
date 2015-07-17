#ifndef DIGITAL_H
#define DIGITAL_H
#include <stdint.h>
#include <avr/io.h>


void MOSDigitalSetup(uint8_t pin);
void MOSDigitalOn(uint8_t pin);
void MOSDigitalOff(uint8_t pin);
//void MOSDigitalNotifyWhenOn(uint8_t pin);


#endif