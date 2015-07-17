#include <stdio.h>
#include <stdarg.h>
#include <avr/pgmspace.h>
#define F_CPU 16000000UL
#define BAUD 9600
#include <util/setbaud.h>

void MOSSerialSetup();
void MOSSerialPrint(char * input);



